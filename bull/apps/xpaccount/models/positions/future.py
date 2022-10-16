from django.db import models

from bull.apps.xpaccount.models.positions.base import BaseQuerySet, BaseManager


class FutureQuerySet(BaseQuerySet):
    excel_sheet_name = "Futuros"


class FutureManager(BaseManager):
    queryset = FutureQuerySet

    def create_from_model(self, parent, model):
        for future in model.details:
            self.create(parent=parent, **future.dict())


class Future(models.Model):
    "Futuros"

    parent = models.ForeignKey(
        to="xpaccount.Positions",
        on_delete=models.CASCADE,
        related_name="future",
    )
    day_quantity = models.IntegerField(
        verbose_name="Quantidade do dia",
    )
    description = models.CharField(
        verbose_name="Descrição",
        max_length=128,
    )
    due_date = models.DateField(
        verbose_name="Data de vencimento",
    )
    goods = models.CharField(
        verbose_name="Mercadoria",
        max_length=128,
    )
    ticker = models.CharField(
        verbose_name="Instrumento",
        max_length=128,
    )
    market = models.CharField(
        verbose_name="Mercado",
        max_length=128,
    )
    position = models.IntegerField(
        verbose_name="Posição",
    )
    quantity = models.IntegerField(
        verbose_name="Quantidade",
    )

    objects = FutureManager.from_queryset(FutureQuerySet)()
