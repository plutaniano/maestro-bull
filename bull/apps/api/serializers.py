from rest_framework import serializers

from bull.apps.user.models import User
from bull.apps.xpaccount.models import (
    Equity,
    FixedIncome,
    Positions,
    XPAccount,
    HubCookie,
)


class RelatedUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "avatar", "first_name", "last_name", "advisor_id"]


class UserSerializer(serializers.ModelSerializer):
    is_advisor = serializers.SerializerMethodField()
    avatar = serializers.ReadOnlyField()
    groups = serializers.StringRelatedField(many=True)

    def get_is_advisor(self, obj):
        return obj in User.objects.advisors()

    class Meta:
        model = User
        exclude = [
            "password",
            "extra",
            "date_joined",
            "last_login",
            "birth_date",
        ]


class FixedIncomeSerializer(serializers.ModelSerializer):
    class Meta:
        model = FixedIncome
        exclude = ["parent", "id", "type_code"]


class EquitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Equity
        exclude = [
            "id",
            "parent",
            "average_cost_status",
        ]


class PositionsSerializer(serializers.ModelSerializer):
    fixed_income = FixedIncomeSerializer(many=True, read_only=True)
    equity = EquitySerializer(many=True, read_only=True)

    class Meta:
        model = Positions
        exclude = ["id", "raw_json"]


class XPAccountSerializer(serializers.ModelSerializer):
    advisor = RelatedUserSerializer(read_only=True)

    class Meta:
        model = XPAccount
        exclude = ["positions"]
        read_only_fields = [
            "id",
            "name",
            "cpf",
            "cnpj",
            "cellphone",
            "phone",
            "email",
            "income",
            "occupation",
            "state",
            "birth_date",
            "suitability",
            "suitability_due",
            "investor_qualification",
            "advisor",
            "amount",
            "patrimony",
            "positions",
            "in_base",
            "xp_updated_at",
        ]


class HubCookieSerializer(serializers.ModelSerializer):
    class Meta:
        model = HubCookie
        fields = "__all__"
