from decimal import Decimal

from django.contrib import auth
from django.db import models
from django.db.models import Sum, F
from django.db.models.functions import Coalesce

from bull.utils import zero_div
from bull.utils.enums import Branches


class UserQuerySet(models.QuerySet):
    def active(self):
        return self.filter(is_active=True)

    def advisors(self):
        return self.active().exclude(advisor_id=None)


class UserManager(auth.models.UserManager.from_queryset(UserQuerySet)):
    pass


class User(auth.models.AbstractUser):
    branch = models.CharField(
        verbose_name="Filial",
        max_length=128,
        choices=Branches.choices,
        null=True,
        blank=True,
    )
    advisor_id = models.IntegerField(
        verbose_name="Código A",
        unique=True,
        null=True,
        blank=True,
    )
    hubspot_id = models.IntegerField(
        verbose_name="ID HubSpot",
        unique=True,
        default=None,
        null=True,
        blank=True,
    )
    slack = models.OneToOneField(
        to="slack.SlackUser",
        on_delete=models.PROTECT,
        verbose_name="Slack",
        related_name="user",
        null=True,
        blank=True,
    )
    birth_date = models.DateField(
        verbose_name="Data de nascimento",
        null=True,
        blank=True,
    )
    cpf = models.CharField(
        verbose_name="CPF",
        max_length=11,
        default="",
        blank=True,
    )
    extra = models.JSONField(
        verbose_name="Campos extras",
        default=dict,
    )

    objects = UserManager()

    def __str__(self):
        return self.get_full_name()

    class Meta:
        verbose_name = "Usuário"
        verbose_name_plural = "Usuários"
        ordering = ["first_name", "last_name"]

    def get_display_name(self):
        if self.slack and self.slack.profile.get("display_name"):
            return self.slack.profile["display_name"]
        return self.get_full_name()

    def patrimony(self):
        func = lambda field: Sum(Coalesce(F(field), Decimal("0.00")))
        return self.clients.in_base().aggregate(
            balance=func("positions__balance__available_balance"),
            coe=func("positions__coe__gross_value"),
            earning=func("positions__earning__provisioned_value"),
            equity=func("positions__equity__financial"),
            fixed_income=func("positions__fixed_income__gross_value"),
            gold=func("positions__gold__position"),
            fund=func("positions__investment_fund__gross_value"),
            # investment_club=prep("positions__raw_json__investmentClub__value"),
            option=func("positions__option__financial"),
            private_pension=func("positions__private_pension__position"),
            real_estate=func("positions__real_estate__position"),
            rental=func("positions__rental__position"),
            structured_product=func("positions__structured_product__legs__financial"),
            term=func("positions__term__position"),
            treasure=func("positions__treasure__position"),
            total=func("patrimony"),
        )

    @property
    def avatar(self):
        if self.slack:
            profile = self.slack.profile
            return (
                profile["image_512"]
                or profile["image_192"]
                or profile["image_72"]
                or profile["image_48"]
                or profile["image_32"]
                or profile["image_24"]
                or None
            )
        return None

    @property
    def calculadora(self):
        patrimony = self.positivador_set.current().patrimony()
        total = patrimony.pop("total", Decimal("inf"))
        return self.extra.get(
            "calculadora",
            {
                "patrimony": {
                    key: zero_div(100 * value, total, Decimal()).quantize(
                        Decimal("0.00")
                    )
                    for key, value in patrimony.items()
                },
                "roa": {
                    "fixed_income": 0.0,
                    "equity": 0.0,
                    "real_estate": 0,
                    "total": 0.0,
                    "fund": 0.0,
                    "private_pension": 0.0,
                },
            },
        )

    @calculadora.setter
    def calculadora(self, value):
        self.extra["calculadora"] = value
        self.save()

    def is_advisor(self):
        return self in User.objects.advisors()
