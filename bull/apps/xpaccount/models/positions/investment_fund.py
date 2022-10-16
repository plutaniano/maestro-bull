from decimal import Decimal

from django.db import models
from django.db.models import Sum
from django.db.models.functions import Coalesce

from bull.utils.xp_api.endpoints.positions.investment_fund import InvestmentFundSubGroup
from bull.apps.xpaccount.models.positions.base import BaseQuerySet, BaseManager


class InvestmentFundQuerySet(BaseQuerySet):
    excel_sheet_name = "Fundos"

    def trend_di(self):
        return self.filter(fund_code=3246).aggregate(
            sum=Coalesce(
                Sum("position"),
                Decimal("0.00"),
                output_field=models.DecimalField(),
            )
        )["sum"]


class InvestmentFundManager(BaseManager):
    queryset = InvestmentFundQuerySet

    def create_from_model(self, parent, model):
        for group in model.sub_groups:
            for fund in group.items:
                self.create(parent=parent, sub_group=group.name, **fund.dict())


class InvestmentFund(models.Model):
    "Fundos de investimento"

    parent = models.ForeignKey(
        to="xpaccount.Positions",
        on_delete=models.CASCADE,
        related_name="investment_fund",
    )
    sub_group = models.CharField(
        verbose_name="Grupo",
        max_length=64,
        choices=InvestmentFundSubGroup.choices,
    )
    fund_code = models.IntegerField(
        verbose_name="Código do Fundo",
    )
    fund_id = models.IntegerField(
        verbose_name="ID do Fundo",
    )
    gross_income = models.DecimalField(
        verbose_name="Rendimento bruto",
        max_digits=12,
        decimal_places=2,
    )
    gross_value = models.DecimalField(
        verbose_name="grossValue",
        max_digits=12,
        decimal_places=2,
    )
    uuid = models.UUIDField(
        verbose_name="UUID",
    )
    iof = models.DecimalField(
        verbose_name="IOF",
        max_digits=12,
        decimal_places=2,
    )
    ir = models.DecimalField(
        verbose_name="IR",
        max_digits=12,
        decimal_places=2,
    )
    is_processing = models.BooleanField(
        verbose_name="Processando",
    )
    liquid_income = models.FloatField(
        verbose_name="Rendimento líquido",
    )
    liquid_value = models.FloatField(
        verbose_name="Valor líquido",
    )
    position = models.DecimalField(
        verbose_name="Posição",
        max_digits=12,
        decimal_places=2,
    )
    product = models.CharField(
        verbose_name="Produto",
        max_length=256,
    )
    quota_amount = models.FloatField(
        verbose_name="Quantidade de cotas",
    )
    quota_date = models.DateField(
        verbose_name="Data da cota",
    )
    quota_value = models.FloatField(
        verbose_name="Valor da cota",
    )
    quotation_value = models.FloatField(
        verbose_name="quotationValue",
    )
    type_code = models.IntegerField(
        verbose_name="Código do tipo",
    )
    withdrawal_blocked = models.BooleanField(
        verbose_name="Bloqueado",
    )
    withdrawal_liquidation = models.CharField(
        verbose_name="Resgate (liquidação)",
        max_length=256,
    )
    withdrawal_quota = models.CharField(
        verbose_name="Resgate (cotização)",
        max_length=256,
    )

    objects = InvestmentFundManager.from_queryset(InvestmentFundQuerySet)()
