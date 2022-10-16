from django.db import models
from bull.utils.xp_api.endpoints.positions.fixed_income import Product, SubGroupName

from bull.apps.xpaccount.models.positions.base import BaseQuerySet


class FixedIncomeQuerySet(BaseQuerySet):
    excel_sheet_name = "Renda Fixa"


class FixedIncomeManager(models.Manager):
    queryset = FixedIncomeQuerySet

    def create_from_model(self, parent, model):
        for group in model.sub_groups:
            for fi in group.items:
                fi = fi.dict()
                side = fi.pop("side")
                self.create(parent=parent, sub_group=group.name, **fi, **side)


class FixedIncome(models.Model):
    "Renda fixa"

    parent = models.ForeignKey(
        to="xpaccount.Positions",
        on_delete=models.CASCADE,
        related_name="fixed_income",
    )
    sub_group = models.CharField(
        verbose_name="Grupo",
        max_length=64,
        choices=SubGroupName.choices,
    )
    asset = models.CharField(
        verbose_name="Ativo",
        max_length=128,
    )
    available = models.IntegerField(
        verbose_name="Disponível",
    )
    issuer = models.CharField(
        verbose_name="Emissor",
        max_length=128,
    )
    lack = models.DateField(
        verbose_name="Carência",
        null=True,
        blank=True,
    )
    maturity = models.DateField(
        verbose_name="Vencimento",
    )
    position = models.DecimalField(
        verbose_name="Posição",
        max_digits=12,
        decimal_places=2,
    )
    product_id = models.IntegerField(
        verbose_name="ID do Produto",
    )
    product = models.CharField(
        verbose_name="Produto",
        max_length=64,
        choices=Product.choices,
    )
    start = models.DateField(
        verbose_name="Aplicação",
    )
    tax = models.CharField(
        verbose_name="Taxa",
        max_length=128,
    )
    type_code = models.IntegerField(
        verbose_name="Type Code",
        choices=[(1, 1), (2, 2), (3, 3)],
    )
    applied_value = models.FloatField(
        verbose_name="Valor aplicado",
    )
    warranty = models.FloatField(
        verbose_name="Garantia",
    )

    # side
    amount = models.IntegerField(
        verbose_name="Quantidade",
    )
    pu_date = models.DateField(
        verbose_name="Data Preço",
    )
    gross_income = models.FloatField(
        verbose_name="Rendimento bruto",
    )
    gross_value = models.FloatField(
        verbose_name="Posição",
    )
    interest = models.CharField(
        verbose_name="Juros",
        max_length=128,
        null=True,
        blank=True,
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
    last_deposit_at = models.DateField(
        verbose_name="Aplicação",
    )
    liquid_income = models.FloatField(
        verbose_name="Rendimento líquido",
    )
    liquid_value = models.FloatField(verbose_name="Valor líquido")
    liquidity = models.CharField(
        verbose_name="Liquidez",
        max_length=64,
    )
    paper = models.CharField(
        verbose_name="Papel",
        max_length=128,
    )
    pu_price = models.FloatField(
        verbose_name="Preço",
    )
    rating = models.CharField(
        verbose_name="Rating",
        max_length=128,
    )

    objects = FixedIncomeManager.from_queryset(FixedIncomeQuerySet)()
