from django.db import models
from bull.utils.xp_api.endpoints.positions.earning import SubGroupName

from bull.apps.xpaccount.models.positions.base import BaseQuerySet


class EarningQuerySet(BaseQuerySet):
    excel_sheet_name = "Proventos"


class EarningManager(models.Manager):
    def create_from_model(self, parent, model):
        for group in model.sub_groups:
            for earning in group.items:
                self.create(parent=parent, sub_group=group.name, **earning.dict())


class Earning(models.Model):
    "Proventos"

    parent = models.ForeignKey(
        to="xpaccount.Positions",
        on_delete=models.CASCADE,
        related_name="earning",
    )
    sub_group = models.CharField(
        verbose_name="Sub Grupo",
        max_length=128,
        choices=SubGroupName.choices,
    )
    payment_date = models.DateField(
        verbose_name="Data de Pagamento",
        null=True,
        blank=True,
    )
    type = models.CharField(
        verbose_name="Tipo",
        max_length=128,
    )
    product = models.CharField(
        verbose_name="Produto",
        max_length=128,
    )
    provisioned_value = models.DecimalField(
        verbose_name="Valor provisionado",
        max_digits=12,
        decimal_places=2,
    )
    quantity = models.IntegerField(
        verbose_name="Quantidade",
    )

    objects = EarningManager.from_queryset(EarningQuerySet)()
