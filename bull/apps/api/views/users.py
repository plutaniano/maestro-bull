from decimal import Decimal

from bull.apps.api.permissions import IsAdminOrSelf
from bull.apps.api.serializers import UserSerializer
from bull.apps.api.validators import DateRangeParams
from bull.apps.user.models import User
from bull.apps.xpaccount.models import XPAccount
from bull.utils import zero_div
from dateutil.relativedelta import relativedelta
from django.db.models import Q, Sum
from django.shortcuts import get_object_or_404
from django_filters import rest_framework as filters
from rest_framework import pagination, permissions, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response


class UserFilter(filters.FilterSet):
    name = filters.CharFilter(label="Nome", method="filter_name")
    is_advisor = filters.BooleanFilter(label="É assessor?", method="filter_is_advisor")
    order_by = filters.OrderingFilter(fields=["first_name", "last_name"])

    def filter_name(self, qs, name, value):
        for term in value.split():
            qs = qs.filter(Q(first_name__icontains=term) | Q(last_name__icontains=term))
        return qs

    def filter_is_advisor(self, qs, name, value):
        match value:
            case True:
                return qs.exclude(advisor_id=None)
            case False:
                return qs.filter(advisor_id=None)
        return qs

    class Meta:
        model = User
        fields = ["advisor_id"]


class UserPagination(pagination.PageNumberPagination):
    page_size = 100
    page_size_query_param = "page_size"
    max_page_size = 200


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserSerializer
    pagination_class = UserPagination
    filterset_class = UserFilter
    queryset = User.objects.active()
    ordering = ["first_name", "last_name"]

    @action(detail=False)
    def self(self, request):
        serializer = self.serializer_class(self.request.user)
        return Response(serializer.data)

    @action(detail=True, permission_classes=[IsAdminOrSelf])
    def pareto(self, request, pk=None):
        user = get_object_or_404(User, pk=pk)
        params = DateRangeParams(**request.query_params.dict())
        months = params.start, params.end
        days = (params.end - params.start).days
        top_clients = (
            user.revenue_set.values_list("xp_account")
            .filter(date__range=months)
            .annotate(revenue=Sum("amount"))
            .exclude(xp_account=None)
            .order_by("-revenue")
        )
        data = []
        for xp_account, _ in top_clients[:20]:
            obj = XPAccount.objects.get(pk=xp_account)
            revenue = obj.revenue_set.filter(date__range=months).per_category()
            patrimony = obj.positivador_set.order_by("-date")[:1].patrimony()
            roa = {
                key: zero_div(
                    Decimal(days / 365) * 100 * revenue[key], patrimony[key], Decimal()
                ).quantize(Decimal("0.000"))
                for key in set(patrimony) & set(revenue)
            }
            data.append(
                {
                    "xp_account": obj.id,
                    "patrimony": patrimony,
                    "revenue": revenue,
                    "roa": roa,
                }
            )
        return Response(
            {
                "revenue": user.revenue_set.filter(date__range=months).per_category(),
                "patrimony": user.positivador_set.current().patrimony(),
                "top_clients": data,
            }
        )

    @action(detail=True, permission_classes=[IsAdminOrSelf])
    def history(self, request, pk=None):
        user = get_object_or_404(User, pk=pk)
        params = DateRangeParams(**request.query_params.dict())
        start, end = params.start, params.end
        data = []
        while start < end:
            deposits = user.captacao_set.month(start).deposits()
            patrimony = user.positivador_set.month(start).patrimony()
            revenue = user.revenue_set.month(start).per_category()
            roa = {
                key: zero_div(
                    12 * 100 * revenue[key], patrimony[key], Decimal()
                ).quantize(Decimal("0.000"))
                for key in set(patrimony) & set(revenue)
            }
            data.append(
                {
                    "month": start,  # 👇 TODO meta de captação (target)
                    "deposits": deposits | {"target": 2_000_000.00},
                    "patrimony": patrimony,
                    "revenue": revenue,
                    "roa": roa,
                }
            )
            start += relativedelta(months=1)
        return Response(data)

    @action(detail=True, permission_classes=[IsAdminOrSelf])
    def latestmonth(self, request, pk=None):
        user = get_object_or_404(User, pk=pk)
        patrimony = user.positivador_set.current().patrimony()
        revenue = user.revenue_set.latest_month().per_category()
        return Response(
            {
                "revenue": revenue,
                "patrimony": {
                    key: zero_div(100 * value, patrimony["total"], Decimal()).quantize(
                        Decimal("0.00")
                    )
                    for key, value in patrimony.items()
                    if key != "total"
                },
                "roa": {
                    key: zero_div(
                        12 * 100 * revenue[key], patrimony[key], Decimal()
                    ).quantize(Decimal("0.000"))
                    for key in set(patrimony) & set(revenue)
                },
            }
        )

    @action(detail=True, permission_classes=[IsAdminOrSelf])
    def calculadora(self, request, pk=None):
        user = get_object_or_404(User, pk=pk)
        return Response(user.calculadora)

    @calculadora.mapping.put
    def calculadora_put(self, request, pk=None):
        user = get_object_or_404(User, pk=pk)
        user.calculadora = request.data
        return Response(request.data)
