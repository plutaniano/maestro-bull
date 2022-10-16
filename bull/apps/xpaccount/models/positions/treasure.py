from bull.apps.xpaccount.models.positions.base import BaseManager, BaseQuerySet
from bull.utils.xp_api.endpoints.positions.treasure import TreasureType
from django.db import models


class TreasureQuerySet(BaseQuerySet):
    excel_sheet_name = "Tesouro"


class TreasureManager(BaseManager):
    queryset = TreasureQuerySet

    def create_from_model(self, parent, model):
        for group in model.sub_groups:
            for treasure in group.items:
                self.create(parent=parent, **treasure.dict())


class Treasure(models.Model):
    "Tesouro"

    parent = models.ForeignKey(
        to="xpaccount.Positions",
        on_delete=models.CASCADE,
        related_name="treasure",
    )
    available = models.DecimalField(
        verbose_name="Disponível",
        max_digits=12,
        decimal_places=2,
    )
    due_date = models.DateField(
        verbose_name="Data de vencimento",
    )
    last_quote = models.DecimalField(
        verbose_name="Última cotação",
        max_digits=12,
        decimal_places=2,
    )
    position = models.DecimalField(
        verbose_name="Posição",
        max_digits=12,
        decimal_places=2,
    )
    product_id = models.IntegerField(
        verbose_name="ID do produto",
    )
    quantity = models.IntegerField(
        verbose_name="Quantidade",
    )
    title = models.CharField(
        verbose_name="Título",
        max_length=64,
        choices=TreasureType.choices,
    )
    type = models.CharField(
        verbose_name="Tipo",
        max_length=64,
        choices=TreasureType.choices,
    )
    type_code = models.IntegerField(
        verbose_name="typeCode",
    )
    warranty = models.IntegerField(
        verbose_name="Em garantia",
    )

    objects = TreasureManager.from_queryset(TreasureQuerySet)()
