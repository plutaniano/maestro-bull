from django.db import models

from bull.apps.xpaccount.models.positions.base import BaseQuerySet, BaseManager


class GoldQuerySet(BaseQuerySet):
    excel_sheet_name = "Ouro"


class GoldManager(BaseManager):
    queryset = GoldQuerySet

    def create_from_model(self, parent, model):
        for gold in model.details:
            self.create(parent=parent, **gold.dict())


class Gold(models.Model):
    "Ouro"

    parent = models.ForeignKey(
        to="xpaccount.Positions",
        on_delete=models.CASCADE,
        related_name="gold",
    )
    weight = models.DecimalField(
        verbose_name="Peso (gramas)",
        max_digits=12,
        decimal_places=2,
    )
    product = models.CharField(
        verbose_name="Ativo",
        max_length=128,
    )
    contracts = models.IntegerField(
        verbose_name="Contratos",
    )
    unit_price = models.DecimalField(
        verbose_name="Preço",
        max_digits=12,
        decimal_places=2,
    )
    position = models.DecimalField(
        verbose_name="Posição",
        max_digits=12,
        decimal_places=2,
    )

    objects = GoldManager.from_queryset(GoldQuerySet)()
