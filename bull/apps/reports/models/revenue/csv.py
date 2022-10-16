import numpy as np
from bull.apps.xpaccount.models import XPAccount
from django.conf import settings
from django.db import models
from pydantic import Field, validator
from bull.utils.enums import Classification
from bull.utils.pydantic_types import Advisor, Date, Money

from bull.apps.reports.models.base import Parser
from bull.apps.reports.models.revenue.base import Revenue, RevenueCategories


class CSVRevenueCategory(models.TextChoices):
    ANTICIPATION_REVERSAL = "anticipation_reversal", "Estorno Adiantamento"
    CO_BROKERAGE = "co_brokerage", "Co-corretagem"
    COLLATERALIZED_CREDIT = "Crédito Colateralizado", "Crédito Colateralizado"
    EXPRESS_WITHDRAWAL = "express_withdrawal", "Resgate Express"
    FOREX = "forex", "Câmbio"
    GUARANTEE = "guarantee", "Seguro Garantia"
    LIFE_INSURANCE = "life_insurance", "Vida"
    PRE_APPROVED_INCENTIVES = "pre_approved_incentives", "Incentivos Pré-Aprovados"
    PRIVATE_PENSION = "private_pension", "Previdência"
    PRIVATE_PENSION_ADVANCE = "private_pension_advance", "Adiantamento Previdência"

    def main_category(self):
        match self.value:
            case CSVRevenueCategory.FOREX:
                return RevenueCategories.FOREX
            case (
                CSVRevenueCategory.COLLATERALIZED_CREDIT
                | CSVRevenueCategory.EXPRESS_WITHDRAWAL
            ):
                return RevenueCategories.CREDIT
            case (
                CSVRevenueCategory.LIFE_INSURANCE
                | CSVRevenueCategory.CO_BROKERAGE
                | CSVRevenueCategory.GUARANTEE
            ):
                return RevenueCategories.INSURANCE
            case (
                CSVRevenueCategory.PRIVATE_PENSION
                | CSVRevenueCategory.PRIVATE_PENSION_ADVANCE
                | CSVRevenueCategory.ANTICIPATION_REVERSAL
            ):
                return RevenueCategories.PRIVATE_PENSION
            case CSVRevenueCategory.PRE_APPROVED_INCENTIVES:
                return RevenueCategories.OTHER
            case _:
                raise ValueError("Unknown category")


class CSVRevenueParser(Parser):
    classification: Classification = Field(alias="Classificação")
    category: CSVRevenueCategory = Field(alias="Categoria")
    level_1: str | None = Field(alias="Nível 1")
    level_2: str | None = Field(alias="Nível 2")
    level_3: str | None = Field(alias="Nível 3")
    level_4: str | None = Field(alias="Nível 4")
    xp_account: XPAccount | None = Field(alias="Código Cliente")
    advisor: Advisor | None = Field(alias="Código Assessor")
    date: Date = Field(alias="Data")
    gross_revenue: Money | None = Field(alias="Receita Bruta R$")
    liquid_revenue: Money | None = Field(alias="Receita Liquida R$")
    comission_pct: float | None = Field(alias="Comissão (%) Escritório")
    comission: Money = Field(alias="Comissão (R$) Escritório")

    @validator("comission_pct", pre=True)
    def comma_to_dot(cls, v):
        if isinstance(v, str):
            v = v.replace(",", ".")
        return v

    @validator("classification", pre=True)
    def map_classification(cls, v):
        match v:
            case "Receitas":
                return Classification.REVENUE
            case "Ajustes":
                return Classification.ADJUSTMENT

    @validator("category", pre=True)
    def map_category(cls, v):
        match v:
            case "Seguro Garantia":
                return CSVRevenueCategory.GUARANTEE
            case "Estorno Adiantamento":
                return CSVRevenueCategory.ANTICIPATION_REVERSAL
            case "Previdência":
                return CSVRevenueCategory.PRIVATE_PENSION
            case "Vida":
                return CSVRevenueCategory.LIFE_INSURANCE
            case "Adiantamento Previdência":
                return CSVRevenueCategory.PRIVATE_PENSION_ADVANCE
            case "Co-corretagem":
                return CSVRevenueCategory.CO_BROKERAGE
            case "Câmbio":
                return CSVRevenueCategory.FOREX
            case "Crédito Colateralizado":
                return CSVRevenueCategory.COLLATERALIZED_CREDIT
            case "Resgate Express":
                return CSVRevenueCategory.EXPRESS_WITHDRAWAL

    @classmethod
    def clean_csv_dataframe(cls, df):
        df.rename(
            inplace=True,
            columns={
                "Comissão(%) Escritório": "Comissão (%) Escritório",
            },
        )
        return df.replace({np.nan: None})


class CSVRevenueQuerySet(models.QuerySet):
    pass


class CSVRevenueManager(models.Manager):
    def update_from_csv(self, *args, **kwargs):
        revenues = CSVRevenueParser.read_csv(*args, **kwargs)
        for revenue in revenues:
            self.create(**revenue.dict())


class CSVRevenue(models.Model):
    revenue = models.OneToOneField(
        to="reports.Revenue",
        on_delete=models.PROTECT,
        verbose_name="Receita",
        related_name="csv_revenue",
        editable=False,
    )
    classification = models.CharField(
        verbose_name="Classificação",
        max_length=32,
        choices=Classification.choices,
    )
    category = models.CharField(
        verbose_name="Categoria",
        max_length=64,
        choices=CSVRevenueCategory.choices,
    )
    level_1 = models.CharField(
        verbose_name="Nível 1",
        max_length=128,
        null=True,
        blank=True,
    )
    level_2 = models.CharField(
        verbose_name="Nível 2",
        max_length=128,
        null=True,
        blank=True,
    )
    level_3 = models.CharField(
        verbose_name="Nível 3",
        max_length=128,
        null=True,
        blank=True,
    )
    level_4 = models.CharField(
        verbose_name="Nível 4",
        max_length=128,
        null=True,
        blank=True,
    )
    xp_account = models.ForeignKey(
        to="xpaccount.XPAccount",
        on_delete=models.PROTECT,
        related_name="csvrevenue_set",
        null=True,
        blank=True,
    )
    advisor = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="csvrevenue_set",
        null=True,
        blank=True,
    )
    date = models.DateField(
        verbose_name="Data",
    )
    gross_revenue = models.DecimalField(
        verbose_name="Receita Bruta",
        max_digits=12,
        decimal_places=2,
        default=0,
        null=True,
        blank=True,
    )
    liquid_revenue = models.DecimalField(
        verbose_name="Receita Líquida",
        max_digits=12,
        decimal_places=2,
        default=0,
        null=True,
        blank=True,
    )
    comission_pct = models.FloatField(
        verbose_name="Comissão do Escritório (%)",
        default=0.0,
        null=True,
        blank=True,
    )
    comission = models.DecimalField(
        verbose_name="Comissão do Escritório (R$)",
        max_digits=12,
        decimal_places=2,
        default=0,
    )

    objects = CSVRevenueManager.from_queryset(CSVRevenueQuerySet)()

    class Meta:
        get_latest_by = "date"
        verbose_name = "Receita CSV"
        verbose_name_plural = "Receitas CSV"

    def save(self, *args, **kwargs):
        if self._state.adding:
            obj = Revenue.objects.create(
                category=self.category.main_category(),
                amount=self.comission,
                date=self.date,
                advisor=self.advisor,
                xp_account=self.xp_account,
            )
            self.revenue = obj
        return super().save(*args, **kwargs)
