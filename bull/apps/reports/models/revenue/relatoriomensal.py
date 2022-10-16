import numpy as np
from bull.apps.reports.models import Parser
from bull.apps.reports.models.revenue.base import Revenue, RevenueCategories
from bull.apps.xpaccount.models import XPAccount
from bull.utils.enums import Classification
from bull.utils.pydantic_types import Advisor, Date, Money
from django.conf import settings
from django.db import models
from pydantic import Field, validator


class RelatorioMensalCategory(models.TextChoices):
    # Fundos
    FUNDS_ADMIN_FEE = "funds_admin_fee", "Fundos - Taxa de Administração"
    FUNDS_CAMPAIGN = "funds_campaign", "Campanha Fundos"
    FUNDS_PERFORMANCE_FEE = "funds_performance_fee", "Fundos - Taxa de Performance"
    EXCLUSIVE_FUNDS = "exclusive_funds", "Fundos Exclusivos"

    # COE
    COE = "coe", "COE"
    COE_CAMPAIGN = "coe_campaign", "Campanha COE"

    # Renda Fixa
    FIXED_FEE = "fixed_fee", "Fee Fixo"
    FIXED_INCOME = "fixed_income", "Renda Fixa"
    FIXED_INCOME_CAMPAIGN = "fixed_income_campaign", "Campanha Renda Fixa"
    FIXED_INCOME_IPO_FEE = "fixed_income_ipo_fee", "IPO Fee Renda Fixa"

    # FII
    REAL_ESTATE_CAMPAIGN = "real_estate_campaign", "Campanha Fundos Imobiliários"
    REAL_ESTATE_OFFERING = "real_estate_offering", "FII - Oferta"

    # RV
    BMF = "bmf", "BM&F"
    BMF_MINI = "bmf_mini", "BM&F Mini"
    BMF_SELF_SERVICE = "bmf_self_service", "BMF Self Service"
    BOVESPA = "bovespa", "Bovespa"
    BOVESPA_SELF_SERVICE = "bovespa_self_service", "Bovespa Self Service"
    BTC = "btc", "BTC"
    CLUBS = "clubs", "Clubes"
    CLUBS_DEBIT = "clubs_debit", "Clubes (débito)"
    CUSTOMER_REFERRAL = "customer_referral", "Indicação de Clientes"
    CUSTOMER_TRANSFER_PENALTY = (
        "customer_transfer_penalty",
        "Desconto de Transferência de Clientes",
    )
    EQUITY_OFFERING = "equity_offering", "Oferta RV"
    MANAGED_PORTFOLIO = "managed_portfolio", "Carteira Administrada"
    OPERATIONAL_ERROR = "operational_error", "Erro Operacional"
    PRIMARY_DISTRIBUTION_OF_FUNDS = (
        "primary_funds_distribution",
        "Distribuição Primária de Fundos",
    )
    RLP_ADJUSTMENT = "rlp_adjustment", "Enquadramento RLP"
    STRUCTURED_CAMPAIGN = "structured_campaign", "Campanhas Estruturadas"

    # Outros
    PRE_APPROVED_INCENTIVES = "pre_approved_incentives", "Incentivos Pré-Aprovados"
    RECEIPT_DIFFERENCE = "receipt_difference", "Diferença de Nota Fiscal"
    OTHER_ADJUSTMENTS = "other_adjustments", "Outros Ajustes"

    def main_category(self):
        match self.value:
            # Fundos
            case (
                RelatorioMensalCategory.FUNDS_ADMIN_FEE
                | RelatorioMensalCategory.FUNDS_CAMPAIGN
                | RelatorioMensalCategory.FUNDS_PERFORMANCE_FEE
                | RelatorioMensalCategory.EXCLUSIVE_FUNDS
            ):
                return RevenueCategories.FUND

            # COE
            case (RelatorioMensalCategory.COE | RelatorioMensalCategory.COE_CAMPAIGN):
                return RevenueCategories.COE

            # Renda Fixa
            case (
                RelatorioMensalCategory.FIXED_FEE
                | RelatorioMensalCategory.FIXED_INCOME
                | RelatorioMensalCategory.FIXED_INCOME_CAMPAIGN
                | RelatorioMensalCategory.FIXED_INCOME_IPO_FEE
            ):
                return RevenueCategories.FIXED_INCOME

            # FII
            case (
                RelatorioMensalCategory.REAL_ESTATE_CAMPAIGN
                | RelatorioMensalCategory.REAL_ESTATE_OFFERING
            ):
                return RevenueCategories.REAL_ESTATE

            # Renda Variável
            case (
                RelatorioMensalCategory.BMF
                | RelatorioMensalCategory.BMF_MINI
                | RelatorioMensalCategory.BMF_SELF_SERVICE
                | RelatorioMensalCategory.BOVESPA
                | RelatorioMensalCategory.BOVESPA_SELF_SERVICE
                | RelatorioMensalCategory.BTC
                | RelatorioMensalCategory.CLUBS
                | RelatorioMensalCategory.CLUBS_DEBIT
                | RelatorioMensalCategory.CUSTOMER_REFERRAL
                | RelatorioMensalCategory.CUSTOMER_TRANSFER_PENALTY
                | RelatorioMensalCategory.EQUITY_OFFERING
                | RelatorioMensalCategory.MANAGED_PORTFOLIO
                | RelatorioMensalCategory.OPERATIONAL_ERROR
                | RelatorioMensalCategory.PRIMARY_DISTRIBUTION_OF_FUNDS
                | RelatorioMensalCategory.RLP_ADJUSTMENT
                | RelatorioMensalCategory.STRUCTURED_CAMPAIGN
            ):
                return RevenueCategories.EQUITY

            # Outros
            case (
                RelatorioMensalCategory.PRE_APPROVED_INCENTIVES
                | RelatorioMensalCategory.RECEIPT_DIFFERENCE
                | RelatorioMensalCategory.OTHER_ADJUSTMENTS
            ):
                return RevenueCategories.OTHER

            case _:
                raise ValueError("Category does not have a main category")


class RelatorioMensalParser(Parser):
    classification: Classification = Field(alias="Classificação")
    category: RelatorioMensalCategory = Field(alias="Produto/Categoria")
    level_1: str | None = Field(alias="Nível 1")
    level_2: str | None = Field(alias="Nível 2")
    level_3: str | None = Field(alias="Nível 3")
    xp_account: XPAccount | None = Field(alias="Código Cliente")
    master: Advisor = Field(alias="Código Master")
    date: Date = Field(alias="Data")
    gross_revenue: Money = Field(alias="Receita Bruta R$")
    liquid_revenue: Money = Field(alias="Receita Liquida R$")
    comission_pct: float = Field(alias="Comissão(%) Escritório")
    comission: Money = Field(alias="Comissão (R$) Escritório")
    liquid_revenue: Money = Field(alias="Receita Líquida R$")
    comission_pct: float = Field(alias="Comissão (%) Escritório")
    advisor: Advisor | None = Field(alias="Código Assessor")

    @validator("comission_pct", pre=True)
    def comma_to_dot(cls, v):
        if isinstance(v, str):
            v = v.replace(",", ".")
        return v

    @validator("classification", pre=True)
    def fix_classification(cls, v):
        mapping = {
            "RECEITAS": Classification.REVENUE,
            "AJUSTES": Classification.ADJUSTMENT,
        }
        return mapping[v]

    @validator("category", pre=True)
    def fix_category(cls, v):
        mapping = {
            # Renda Variável
            "BM&F": RelatorioMensalCategory.BMF,
            "BMF MINI": RelatorioMensalCategory.BMF_MINI,
            "BMF SELF SERVICE": RelatorioMensalCategory.BMF_SELF_SERVICE,
            "BOVESPA SELF SERVICE": RelatorioMensalCategory.BOVESPA_SELF_SERVICE,
            "BOVESPA": RelatorioMensalCategory.BOVESPA,
            "BTC": RelatorioMensalCategory.BTC,
            "OFERTA RV": RelatorioMensalCategory.EQUITY_OFFERING,
            "Campanha Estruturadas": RelatorioMensalCategory.STRUCTURED_CAMPAIGN,
            "Carteira ADM": RelatorioMensalCategory.MANAGED_PORTFOLIO,
            "Clubes (debito)": RelatorioMensalCategory.CLUBS_DEBIT,
            "CLUBES": RelatorioMensalCategory.CLUBS,
            "Desconto de Transferência de Clientes": RelatorioMensalCategory.CUSTOMER_TRANSFER_PENALTY,
            "DISTRIBUIÇÃO PRIMÁRIA DE FUNDOS": RelatorioMensalCategory.PRIMARY_DISTRIBUTION_OF_FUNDS,
            "Enquadramento RLP": RelatorioMensalCategory.RLP_ADJUSTMENT,
            "Erro Operacional": RelatorioMensalCategory.OPERATIONAL_ERROR,
            "INDICAÇÃO DE CLIENTES": RelatorioMensalCategory.CUSTOMER_REFERRAL,
            # Renda Fixa
            "FEE FIXO": RelatorioMensalCategory.FIXED_FEE,
            "RENDA FIXA": RelatorioMensalCategory.FIXED_INCOME,
            "Campanha Renda Fixa": RelatorioMensalCategory.FIXED_INCOME_CAMPAIGN,
            "IPO FEE RENDA FIXA": RelatorioMensalCategory.FIXED_INCOME_IPO_FEE,
            # FII
            "Campanha Fundos Imobiliários": RelatorioMensalCategory.REAL_ESTATE_CAMPAIGN,
            "OFERTA FII": RelatorioMensalCategory.REAL_ESTATE_OFFERING,
            # COE
            "COE": RelatorioMensalCategory.COE,
            "Campanha COE": RelatorioMensalCategory.COE_CAMPAIGN,
            # Fundos
            "Campanha Fundos": RelatorioMensalCategory.FUNDS_CAMPAIGN,
            "FUNDOS - TX ADM": RelatorioMensalCategory.FUNDS_ADMIN_FEE,
            "FUNDOS - TX PERF": RelatorioMensalCategory.FUNDS_PERFORMANCE_FEE,
            "Fundos Exclusivos": RelatorioMensalCategory.EXCLUSIVE_FUNDS,
            # Outros
            "Diferenca de NF": RelatorioMensalCategory.RECEIPT_DIFFERENCE,
            "Incentivos Pré-Aprovados": RelatorioMensalCategory.PRE_APPROVED_INCENTIVES,
            "Outros Ajustes": RelatorioMensalCategory.OTHER_ADJUSTMENTS,
        }
        return mapping[v]

    @classmethod
    def clean_excel_dataframe(cls, df):
        df = df.replace({np.nan: None})
        df.columns = df.iloc[1]  # renomeia colunas
        df = df.iloc[2:]  # remove linhas em branco no topo da planilha
        df = df.iloc[
            :, [i for i in range(14) if i != 12]
        ]  # remove colunas desnecessarias
        return df


class RelatorioMensalQuerySet(models.QuerySet):
    pass


class RelatorioMensalManager(models.Manager):
    def update_from_excel(self, *args, **kwargs):
        revenues = RelatorioMensalParser.from_excel(*args, **kwargs)
        for r in revenues:
            self.create(**r.dict())


class RelatorioMensal(models.Model):
    revenue = models.OneToOneField(
        to="reports.Revenue",
        on_delete=models.PROTECT,
        verbose_name="Receita",
        related_name="relatorio_mensal",
        editable=False,
    )
    classification = models.CharField(
        verbose_name="Classificação",
        max_length=32,
        choices=Classification.choices,
    )
    category = models.CharField(
        verbose_name="Categoria",
        max_length=32,
        choices=RelatorioMensalCategory.choices,
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
        default="",
    )
    level_3 = models.CharField(
        verbose_name="Nível 3",
        max_length=128,
        null=True,
        blank=True,
    )
    xp_account = models.ForeignKey(
        to="xpaccount.XPAccount",
        on_delete=models.PROTECT,
        verbose_name="Conta XP",
        related_name="relatoriomensal_set",
        null=True,
        blank=True,
    )
    master = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name="Master",
        related_name="master_set",
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
    advisor = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name="Assessor",
        related_name="relatoriomensal_set",
        null=True,
        blank=True,
    )

    objects = RelatorioMensalManager.from_queryset(RelatorioMensalQuerySet)()

    class Meta:
        verbose_name = "Relatório Mensal"
        verbose_name_plural = "Relatórios Mensais"

    def save(self, *args, **kwargs):
        if self._state.adding:
            obj = Revenue.objects.create(
                category=self.category.main_category(),
                date=self.date,
                amount=self.comission,
                xp_account=self.xp_account,
                advisor=self.advisor,
            )
            self.revenue = obj
        super().save(*args, **kwargs)
