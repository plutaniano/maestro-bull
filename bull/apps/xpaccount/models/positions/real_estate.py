from bull.apps.xpaccount.models.positions.base import BaseManager, BaseQuerySet
from django.db import models


class RealEstateQuerySet(BaseQuerySet):
    excel_sheet_name = "FIIs"


class RealEstateManager(BaseManager):
    queryset = RealEstateQuerySet

    def create_from_model(self, parent, model):
        for fii in model.details:
            self.create(parent=parent, **fii.dict())


class RealEstate(models.Model):
    "Fundos imobiliários"

    parent = models.ForeignKey(
        to="xpaccount.Positions",
        on_delete=models.CASCADE,
        related_name="real_estate",
    )
    average_cost = models.DecimalField(
        verbose_name="Preço médio",
        max_digits=12,
        decimal_places=2,
    )
    average_cost_status = models.IntegerField(
        verbose_name="averageCostStatus",
    )
    last_quote = models.DecimalField(
        verbose_name="Última cotação",
        max_digits=12,
        decimal_places=2,
    )
    performance = models.FloatField(
        verbose_name="Rentabilidade",
    )
    position = models.DecimalField(
        verbose_name="Posição",
        max_digits=12,
        decimal_places=2,
    )
    quantity_available = models.IntegerField(
        verbose_name="Quantidade disponível",
    )
    quantity_blocked = models.IntegerField(
        verbose_name="Quantidade bloqueada",
    )
    quantity_day = models.IntegerField(
        verbose_name="Quantidade do dia",
    )
    quantity_projected = models.IntegerField(
        verbose_name="Quantidade projetada",
    )
    quantity_total = models.IntegerField(
        verbose_name="Quantidade total",
    )
    ticker = models.CharField(
        verbose_name="Ativo",
        max_length=64,
    )

    objects = RealEstateManager.from_queryset(RealEstateQuerySet)()
