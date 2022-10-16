from bull.apps.xpaccount.models.positions.base import BaseQuerySet
from bull.utils.xp_api.endpoints.positions.coe import CoeIssuers
from django.db import models


class CoeQuerySet(BaseQuerySet):
    excel_sheet_name = "COE"


class CoeManager(models.Manager):
    def create_from_model(self, parent, model):
        for coe in model.details:
            return self.create(parent=parent, **coe.dict())


class Coe(models.Model):
    "COE"

    parent = models.ForeignKey(
        to="xpaccount.Positions",
        on_delete=models.CASCADE,
        related_name="coe",
    )
    application_date = models.DateField(
        verbose_name="Data da aplicação",
    )
    applied_value = models.FloatField(
        verbose_name="Valor aplicado",
    )
    due_date = models.DateField(
        verbose_name="Data de vencimento",
    )
    issuer = models.CharField(
        verbose_name="Emissor",
        max_length=256,
        choices=CoeIssuers.choices,
    )
    gross_value = models.DecimalField(
        verbose_name="Valor bruto",
        max_digits=12,
        decimal_places=2,
    )
    name = models.CharField(
        verbose_name="Nome",
        max_length=256,
    )
    product_id = models.BigIntegerField(
        verbose_name="ID do Produto",
    )
    quantity = models.IntegerField(
        verbose_name="Quantidade",
    )
    unit_price = models.FloatField(
        verbose_name="Preço unitário",
    )

    objects = CoeManager.from_queryset(CoeQuerySet)()
