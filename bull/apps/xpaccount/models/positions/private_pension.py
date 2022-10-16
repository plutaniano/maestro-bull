from django.db import models
from bull.utils.enums import Insurers
from bull.utils.xp_api.endpoints.positions.private_pension import (
    PrivatePensionContribution,
    PrivatePensionPayment,
    PrivatePensionPlan,
    PrivatePensionStatus,
    PrivatePensionTaxation,
)

from bull.apps.xpaccount.models.positions.base import BaseManager, BaseQuerySet


class PrivatePensionQuerySet(BaseQuerySet):
    excel_sheet_name = "Previdências"


class PrivatePensionManager(BaseManager):
    queryset = PrivatePensionQuerySet

    def create_from_model(self, parent, model):
        for pp in model.details:
            self.create(parent=parent, **pp.dict())


class PrivatePension(models.Model):
    "Previdência privada"

    parent = models.ForeignKey(
        to="xpaccount.Positions",
        on_delete=models.CASCADE,
        related_name="private_pension",
    )
    asset = models.CharField(
        verbose_name="Ativo",
        max_length=256,
    )
    balance = models.DecimalField(
        verbose_name="Saldo",
        max_digits=12,
        decimal_places=2,
    )
    certificate = models.IntegerField(
        verbose_name="Certificado",
    )
    cnpj = models.CharField(
        verbose_name="CNPJ",
        max_length=16,
    )
    contribution = models.CharField(
        verbose_name="Contribuição",
        max_length=64,
        choices=PrivatePensionContribution.choices,
    )
    gross_income = models.DecimalField(
        verbose_name="Rendimento bruto",
        max_digits=12,
        decimal_places=2,
    )
    insured = models.CharField(
        verbose_name="Segurado",
        max_length=256,
    )
    insurer = models.CharField(
        verbose_name="Seguradora",
        max_length=64,
        choices=Insurers.choices,
    )
    payment = models.CharField(
        verbose_name="Forma de pagamento",
        max_length=64,
        choices=PrivatePensionPayment.choices,
    )
    plan = models.CharField(
        verbose_name="Plano",
        max_length=64,
        choices=PrivatePensionPlan.choices,
    )
    position = models.DecimalField(
        verbose_name="Posição",
        max_digits=12,
        decimal_places=2,
    )
    proposal_code = models.BigIntegerField(
        verbose_name="Código da proposta",
    )
    quota_date = models.DateField(
        verbose_name="Data da Cota",
    )
    quota_value = models.FloatField(
        verbose_name="Valor da cota",
    )
    quotas = models.FloatField(
        verbose_name="Quantidade de cotas",
    )
    taxation = models.CharField(
        verbose_name="Tributação",
        max_length=64,
        choices=PrivatePensionTaxation.choices,
    )
    start_date = models.DateField(
        verbose_name="Inicio vigência",
    )
    status = models.CharField(
        verbose_name="Status",
        max_length=64,
        choices=PrivatePensionStatus.choices,
    )
    susep = models.CharField(
        verbose_name="Processo SUSEP",
        max_length=32,
    )
    total_invested = models.DecimalField(
        verbose_name="Total aplicado",
        max_digits=12,
        decimal_places=2,
    )
    total_rescue = models.DecimalField(
        verbose_name="Total de resgates",
        max_digits=12,
        decimal_places=2,
    )

    objects = PrivatePensionManager.from_queryset(PrivatePensionQuerySet)()
