from django.db import models

from bull.apps.xpaccount.models.positions.base import BaseQuerySet, BaseManager


class EquityQuerySet(BaseQuerySet):
    excel_sheet_name = "Ações"


class EquityManager(BaseManager):
    queryset = EquityQuerySet

    def create_from_model(self, parent, model):
        for equity in model.details:
            self.create(parent=parent, **equity.dict())


class Equity(models.Model):
    "Ações"

    parent = models.ForeignKey(
        to="xpaccount.Positions",
        on_delete=models.CASCADE,
        related_name="equity",
    )
    quote = models.DecimalField(
        verbose_name="Cotação",
        max_digits=12,
        decimal_places=2,
    )
    financial = models.DecimalField(
        verbose_name="Financeiro",
        max_digits=12,
        decimal_places=2,
    )
    available = models.IntegerField(
        verbose_name="Quantidade",
    )
    quantity = models.IntegerField(
        verbose_name="Quantidade",
    )
    ticker = models.CharField(
        verbose_name="Ticker",
        max_length=128,
    )
    average_cost = models.FloatField(
        verbose_name="Custo médio",
    )
    performance = models.FloatField(
        verbose_name="Performance",
    )
    quantity_day = models.IntegerField(
        verbose_name="Quantidade do dia",
        null=True,
        blank=True,
    )
    warranty_bovespa = models.IntegerField(
        verbose_name="Garantia bovespa",
    )
    warranty_bvmf = models.IntegerField(
        verbose_name="Garantia BVMF",
    )
    average_cost_status = models.IntegerField(
        verbose_name="Status de custo médio",
    )
    quantity_projected = models.IntegerField(
        verbose_name="Quantidade projetada",
    )
    quantity_structured = models.IntegerField(
        verbose_name="Quantidade estruturado",
    )

    objects = EquityManager.from_queryset(EquityQuerySet)()


class RewardedAssetManager(models.Manager):
    def create_from_model(self, parent, model):
        for ra in model.details:
            self.create(
                parent=parent,
                expiry_date=ra.expiry_date,
                financial=ra.financial,
                quantity=ra.quantity,
                quote=ra.quote,
                ticker=ra.ticker,
            )


class RewardedAsset(models.Model):
    parent = models.ForeignKey(
        to="xpaccount.Positions",
        on_delete=models.CASCADE,
        related_name="rewarded_asset",
    )
    quote = models.DecimalField(
        verbose_name="Cotação",
        max_digits=12,
        decimal_places=2,
    )
    financial = models.DecimalField(
        verbose_name="Financeiro",
        max_digits=12,
        decimal_places=2,
    )
    quantity = models.IntegerField(
        verbose_name="Quantidade",
    )
    ticker = models.CharField(
        verbose_name="Ticker",
        max_length=128,
    )
    expiry_date = models.DateField(
        verbose_name="Data de vencimento",
    )

    objects = RewardedAssetManager.from_queryset(EquityQuerySet)()
