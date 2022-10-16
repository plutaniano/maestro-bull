from bull.apps.api.serializers import PositionsSerializer, XPAccountSerializer
from bull.apps.xpaccount.exceptions import ValidCookieNotAvailable
from bull.apps.xpaccount.models import XPAccount
from django.shortcuts import get_object_or_404
from django_filters import rest_framework as filters
from rest_framework import mixins, permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response


class XPAccountFilter(filters.FilterSet):
    query = filters.CharFilter(label="Nome ou Código", method="filter_query")
    order_by = filters.OrderingFilter(fields=["name", "id", "patrimony", "amount"])

    def filter_query(self, qs, name, value):
        if value.isnumeric():
            qs = qs.filter(pk=value)
        else:
            for term in value.split():
                qs = qs.filter(name__unaccent__icontains=term)
        return qs

    class Meta:
        model = XPAccount
        fields = []


class XPAccountViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet,
):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = XPAccountSerializer
    filterset_class = XPAccountFilter

    def get_queryset(self):
        user = self.request.user
        qs = XPAccount.objects.in_base()
        if user.is_superuser or user.is_staff:
            return qs
        return qs.filter(advisor=user)

    def get_object(self):
        obj = get_object_or_404(self.get_queryset(), pk=self.kwargs["pk"])
        self.check_object_permissions(self.request, obj)
        return obj

    @action(detail=True, url_path="update")
    def update_(self, request, pk=None):
        try:
            xp_account = self.get_object()
            xp_account.update_positions()
            return Response(
                {"detail": "Conta atualizada com sucesso"},
                status=status.HTTP_200_OK,
            )
        except ValidCookieNotAvailable:
            return Response(
                {"detail": "Não existe um cookie válido."},
                status=status.HTTP_503_SERVICE_UNAVAILABLE,
            )

    @action(detail=True)
    def positions(self, request, pk=None):
        xp_account = self.get_object()
        data = PositionsSerializer(xp_account.positions).data
        return Response(data)

    @action(detail=True)
    def raw_json(self, request, pk=None):
        xp_account = self.get_object()
        return Response(xp_account.positions.raw_json)
