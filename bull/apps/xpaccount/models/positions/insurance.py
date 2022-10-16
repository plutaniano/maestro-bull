from django.db import models
from bull.utils.xp_api.endpoints.positions.insurance import (
    InsuranceStatus,
    InsuranceTypes,
)

from bull.apps.xpaccount.models.positions.base import BaseQuerySet, BaseManager


class InsuranceQuerySet(BaseQuerySet):
    pass


class InsuranceManager(BaseManager):
    queryset = InsuranceQuerySet

    def create_from_model(self, parent, model):
        for insurance in model.details:
            self.create(parent=parent, **insurance.dict())


class Insurance(models.Model):
    "Seguros"

    parent = models.ForeignKey(
        to="xpaccount.Positions",
        on_delete=models.CASCADE,
        related_name="insurance",
    )
    type = models.CharField(
        verbose_name="Tipo de cobertura",
        max_length=128,
        choices=InsuranceTypes.choices,
    )
    status = models.CharField(
        verbose_name="Status",
        max_length=128,
        choices=InsuranceStatus.choices,
    )
    premium = models.DecimalField(
        verbose_name="Prêmio",
        max_digits=12,
        decimal_places=2,
    )
    product = models.CharField(
        verbose_name="Tipo de produto",
        max_length=256,
    )
    contract_date = models.DateField(
        verbose_name="Data de Contrato",
    )
    insurer = models.CharField(
        verbose_name="Seguradora",
        max_length=128,
    )
    insured_capital = models.FloatField(
        verbose_name="Capital segurado",
    )
    coverage_type = models.IntegerField(
        verbose_name="Tipo de cobertura",
    )

    objects = InsuranceManager.from_queryset(InsuranceQuerySet)()
