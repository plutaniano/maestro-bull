from bull.apps.xpaccount.models.positions.base import BaseManager, BaseQuerySet
from bull.utils.xp_api.endpoints.positions.rental import RentalCounterPartyType
from django.db import models


class RentalQuerySet(BaseQuerySet):
    excel_sheet_name = "Aluguéis"


class RentalManager(BaseManager):
    queryset = RentalQuerySet

    def create_from_model(self, parent, model):
        for rental in model.details:
            self.create(parent=parent, **rental.dict())


class Rental(models.Model):
    "Aluguéis"

    parent = models.ForeignKey(
        to="xpaccount.Positions",
        on_delete=models.CASCADE,
        related_name="rental",
    )
    amount = models.IntegerField(
        verbose_name="Quantidade",
    )
    average_cost_status = models.IntegerField(
        verbose_name="averageCostStatus",
    )
    average_cost = models.DecimalField(
        verbose_name="Preço médio",
        max_digits=12,
        decimal_places=2,
    )
    counterparty_type = models.CharField(
        verbose_name="Doador/Tomador",
        max_length=64,
        choices=RentalCounterPartyType.choices,
    )
    last_quote = models.DecimalField(
        verbose_name="Última cotação",
        max_digits=12,
        decimal_places=2,
    )
    maturity = models.DateField(
        verbose_name="Data de vencimento",
    )
    performance = models.FloatField(
        verbose_name="Rentabilidade",
    )
    position = models.DecimalField(
        verbose_name="Posição",
        max_digits=12,
        decimal_places=2,
    )
    structured_amount = models.IntegerField(
        verbose_name="Total estruturado",
    )
    ticker = models.CharField(
        verbose_name="Ticker",
        max_length=64,
    )
    total_amount = models.IntegerField(
        verbose_name="Quantidade total",
    )

    objects = RentalManager.from_queryset(RentalQuerySet)()
