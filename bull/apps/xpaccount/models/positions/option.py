from bull.apps.xpaccount.models.positions.base import BaseManager, BaseQuerySet
from bull.utils.xp_api.endpoints.positions.option import (
    FlexibleOptionFixingTypes,
    FlexibleOptionFramingCategories,
    FlexibleOptionTypes,
    OptionGroupName,
    OptionStyles,
)
from django.db import models
from django.db.models import F, Value
from django.db.models.functions import Concat


class OptionQuerySet(BaseQuerySet):
    excel_sheet_name = "Opções"


class OptionManager(BaseManager):
    queryset = OptionQuerySet

    def create_from_model(self, parent, model):
        for group in model.sub_groups:
            if group.name != OptionGroupName.OPTION:
                continue
            for option in group.items:
                self.create(parent=parent, **option.dict())


class Option(models.Model):
    "Opções"

    parent = models.ForeignKey(
        to="xpaccount.Positions",
        on_delete=models.CASCADE,
        related_name="option",
    )
    available_quantity = models.IntegerField(
        verbose_name="Quantidade disponível",
    )
    day_quantity = models.IntegerField(
        verbose_name="Quantidade do dia",
    )
    due_date = models.DateField(
        verbose_name="Data de vencimento",
        null=True,
        blank=True,
    )
    financial = models.DecimalField(
        verbose_name="Financeiro",
        max_digits=12,
        decimal_places=2,
    )
    quote = models.DecimalField(
        verbose_name="Cotação",
        max_digits=12,
        decimal_places=2,
        null=True,
        blank=True,
    )
    series = models.CharField(
        verbose_name="Série",
        max_length=128,
    )
    strike_price = models.DecimalField(
        verbose_name="Preço do strike",
        max_digits=12,
        decimal_places=2,
    )
    total_quantity = models.IntegerField(
        verbose_name="Quantidade total",
    )
    style = models.CharField(
        verbose_name="Tipo",
        max_length=32,
        choices=OptionStyles.choices,
    )
    underlying = models.CharField(
        verbose_name="Ativo objeto",
        max_length=128,
    )

    objects = OptionManager.from_queryset(OptionQuerySet)()


class OTCOptionQuerySet(BaseQuerySet):
    excel_sheet_name = "Derivativos de Balcão"
    # TODO: Arrumar um jeito de parametrizar melhor quais campos devem ser incluidos
    # na exportação. Como esse modelo tem um campo 'xp_account', ele conflita com o
    # campo 'xp_account' que é adicionado pelo 'excel_default_fields' padrão.
    excel_default_fields = [
        ("client_name", "Cliente", F("parent__xp_account__name")),
        ("advisor_id", "Código A", F("parent__xp_account__advisor__advisor_id")),
        (
            "advisor_name",
            "Assessor",
            Concat(
                F("parent__xp_account__advisor__first_name"),
                Value(" "),
                F("parent__xp_account__advisor__last_name"),
            ),
        ),
    ]


class OTCOptionManager(models.Manager):
    queryset = OTCOptionQuerySet

    def create_from_model(self, parent, model):
        for group in model.sub_groups:
            if group.name != OptionGroupName.OTC:
                continue
            for otc in group.items:
                self.create(parent=parent, **otc.dict())


class OTCOption(models.Model):
    "Derivativos de balcão"

    parent = models.ForeignKey(
        to="xpaccount.Positions",
        on_delete=models.CASCADE,
        related_name="otc_option",
    )
    asset = models.CharField(
        verbose_name="Ativo",
        max_length=64,
    )
    current_factor = models.FloatField(
        verbose_name="Current Factor",
    )
    xp_account = models.ForeignKey(
        verbose_name="Conta XP",
        to="xpaccount.XPAccount",
        on_delete=models.PROTECT,
        related_name="+",
    )
    description = models.CharField(
        verbose_name="Descrição",
        max_length=256,
        blank=True,
    )
    expiration_code = models.IntegerField(
        verbose_name="Código de vencimento",
        null=True,
        blank=True,
    )
    expiry_date = models.DateField(
        verbose_name="Data de vencimento",
    )
    fixing_date = models.DateField(
        verbose_name="Data de fixing",
    )
    fixing_type = models.CharField(
        verbose_name="Tipo de fixing",
        max_length=32,
        choices=FlexibleOptionFixingTypes.choices,
    )
    framing_category = models.IntegerField(
        verbose_name="Framing Category",
        choices=FlexibleOptionFramingCategories.choices,
    )
    opening_margin_max = models.FloatField(
        verbose_name="openingMarginMax",
    )
    opening_unit_price = models.DecimalField(
        verbose_name="Preço de abertura",
        max_digits=12,
        decimal_places=2,
        null=True,
        blank=True,
    )
    position_date = models.DateField(
        verbose_name="Data da posição",
    )
    position = models.DecimalField(
        verbose_name="Posição",
        max_digits=12,
        decimal_places=2,
    )
    settlement_date = models.DateField(
        verbose_name="Data de liquidação",
    )
    opening_amount = models.IntegerField(
        verbose_name="Quantidade/Volume",
    )
    type = models.CharField(
        verbose_name="Tipo",
        max_length=64,
        choices=FlexibleOptionTypes.choices,
    )
    underlying = models.CharField(
        verbose_name="Ativo objeto",
        max_length=64,
    )

    objects = OTCOptionManager.from_queryset(OTCOptionQuerySet)()
