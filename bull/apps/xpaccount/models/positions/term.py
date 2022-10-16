from bull.apps.xpaccount.models.positions.base import BaseManager, BaseQuerySet
from django.db import models


class TermQuerySet(BaseQuerySet):
    excel_sheet_name = "Termos"


class TermManager(BaseManager):
    queryset = TermQuerySet

    def create_from_model(self, parent, model):
        for term in model.details:
            self.create(parent=parent, **term.dict())


class Term(models.Model):
    "Termo"

    parent = models.ForeignKey(
        to="xpaccount.Positions",
        on_delete=models.CASCADE,
        related_name="term",
    )
    due_date = models.DateField(
        verbose_name="Data de vencimento",
    )
    entry_price = models.DecimalField(
        verbose_name="Preço de entrada",
        max_digits=12,
        decimal_places=2,
    )
    position = models.DecimalField(
        verbose_name="Posição",
        max_digits=12,
        decimal_places=2,
    )
    last_quote = models.DecimalField(
        verbose_name="Última cotação",
        max_digits=12,
        decimal_places=2,
    )
    quantity = models.IntegerField(
        verbose_name="Quantidade",
    )
    roll_date = models.DateField(
        verbose_name="Data de rolagem",
    )
    ticker = models.CharField(
        verbose_name="Ativo",
        max_length=64,
    )

    objects = TermManager.from_queryset(TermQuerySet)()
