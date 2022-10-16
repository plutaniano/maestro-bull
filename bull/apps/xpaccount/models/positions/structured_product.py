from bull.apps.xpaccount.models.positions.base import BaseManager, BaseQuerySet
from bull.utils.xp_api.endpoints.positions.structured_product import (
    StructuredProductFixingTypes,
    StructuredProductOptionTypes,
    StructuredProductStatus,
)
from django.db import models
from django.db.models import F, Value
from django.db.models.functions import Concat


class StructuredProductQuerySet(BaseQuerySet):
    excel_sheet_name = "Produtos Estruturados"
    excel_exclude_fields = ["parent", "id", "legs", "structuredproductleg"]


class StructuredProductManager(BaseManager):
    queryset = StructuredProductQuerySet

    def create_from_model(self, parent, model):
        for sp in model.details:
            struct = self.create(parent=parent, **sp.dict(exclude={"legs"}))
            for leg in sp.legs:
                StructuredProductLeg.objects.create_from_model(struct, leg)


class StructuredProduct(models.Model):
    "Produtos estruturados"

    parent = models.ForeignKey(
        to="xpaccount.Positions",
        on_delete=models.CASCADE,
        related_name="structured_product",
    )
    cost = models.DecimalField(
        verbose_name="Custo",
        max_digits=12,
        decimal_places=2,
    )
    name = models.CharField(
        verbose_name="Nome da Estrutura",
        max_length=256,
    )
    end_date = models.DateField(
        verbose_name="Data de Encerramento",
    )
    percent = models.FloatField(
        verbose_name="Porcento",
    )

    objects = StructuredProductManager.from_queryset(StructuredProductQuerySet)()

    def __str__(self):
        return f"'{self.name}' XP:{self.parent.xp_account} ({self.id})"


class StructuredProductLegQuerySet(BaseQuerySet):
    excel_sheet_name = "Prod. Strut. - Pernas"
    excel_exclude_fields = ["id", "structure"]
    excel_default_fields = [
        ("xp_account", "Conta XP", F("structure__parent__xp_account_id")),
        ("client_name", "Cliente", F("structure__parent__xp_account__name")),
        (
            "advisor_id",
            "Código A",
            F("structure__parent__xp_account__advisor__advisor_id"),
        ),
        (
            "advisor_name",
            "Assessor",
            Concat(
                F("structure__parent__xp_account__advisor__first_name"),
                Value(" "),
                F("structure__parent__xp_account__advisor__last_name"),
            ),
        ),
    ]

    def fresh(self):
        return self.filter(structure__parent__fresh=True)


class StructuredProductLegManager(BaseManager):
    def get_queryset(self):
        return StructuredProductLegQuerySet(self.model, using=self._db).annotate(
            xp_account_id=F("structure__parent__xp_account"),
            advisor_id=F("structure__parent__xp_account__advisor__advisor_id"),
        )

    def create_from_model(self, structure, leg):
        self.create(structure=structure, **leg.dict())


class StructuredProductLeg(models.Model):
    "Perna de produto estruturado"

    structure = models.ForeignKey(
        to="xpaccount.StructuredProduct",
        on_delete=models.CASCADE,
        verbose_name="Estrutura",
        related_name="legs",
    )
    asset = models.CharField(
        verbose_name="Ativo",
        max_length=12,
    )
    contracted_quantity_position = models.IntegerField(
        verbose_name="quantidadeContratadaPosicao",
    )
    contracted_quantity = models.IntegerField(
        verbose_name="Quantidade contratada",
    )
    description = models.CharField(
        verbose_name="Descrição",
        max_length=256,
        blank=True,
    )
    end_date = models.DateField(
        verbose_name="Data de encerramento",
        null=True,
        blank=True,
    )
    financial = models.DecimalField(
        verbose_name="Financeiro",
        max_digits=12,
        decimal_places=2,
    )
    fixing_date = models.DateField(
        verbose_name="Data de fixing",
        null=True,
        blank=True,
    )
    fixing_type = models.CharField(
        verbose_name="Tipo Fixing",
        max_length=64,
        choices=StructuredProductFixingTypes.choices,
        null=True,
        blank=True,
    )
    liquidation_date = models.DateField(
        verbose_name="Data de liquidação",
        null=True,
        blank=True,
    )
    option_type = models.CharField(
        verbose_name="Tipo",
        max_length=64,
        choices=StructuredProductOptionTypes.choices,
    )
    position_quantity = models.IntegerField(
        verbose_name="Quantidade contratada",
    )
    strike = models.DecimalField(
        verbose_name="Preço de exercício",
        max_digits=12,
        decimal_places=2,
        null=True,
        blank=True,
    )
    quantity = models.IntegerField(
        verbose_name="Quantidade",
    )
    status = models.CharField(
        verbose_name="Status",
        max_length=64,
        choices=StructuredProductStatus.choices,
    )

    objects = StructuredProductLegManager.from_queryset(StructuredProductLegQuerySet)()
