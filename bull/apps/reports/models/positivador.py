import os
import re
from datetime import date
from decimal import Decimal

import numpy as np
from bull.apps.reports.models import Parser
from bull.apps.xpaccount.models import XPAccount
from django.conf import settings
from django.db import models
from django.db.models import Sum
from django.db.models.functions import Coalesce
from django.utils import timezone
from pydantic import Field, validator
from bull.utils.enums import Sex
from bull.utils.pydantic_types import Advisor, Bool, Date, Money


class PositivadorSegment(models.TextChoices):
    PRIVATE = "private", "Private"
    EXPRESS = "express", "Express"
    UNIQUE = "unique", "Unique"
    PLUS = "plus", "Plus"
    NOT_AVAILABLE = "not_available", "Não disponível"


PATTERN = re.compile(
    r"positivador_(?P<year>\d{4})(?P<month>\d\d)(?P<day>\d\d)_\d\d-\d\d-\d{4}-\d\d-\d\d-\d\d.xlsx"
)
PATRIMONY_FIELDS = [
    "fund",
    "equity",
    "private_pension",
    "fixed_income",
    "real_estate",
    "balance",
]


class PositivadorParser(Parser):
    date: date
    advisor: Advisor = Field(alias="Assessor")
    xp_account: XPAccount = Field(alias="Cliente")
    occupation: str = Field(alias="Profissão")
    sex: Sex | None = Field(alias="Sexo")
    segment: PositivadorSegment | None = Field(alias="Segmento")
    sign_up_date: Date = Field(alias="Data de Cadastro")
    made_second_deposit: Bool = Field(alias="Fez Segundo Aporte?")
    birth_date: Date = Field(alias="Data de Nascimento")
    is_active: Bool = Field(alias="Status")
    actived: Bool = Field(alias="Ativou em M?")
    evaded: Bool = Field(alias="Evadiu em M?")
    traded_bovespa: Bool = Field(alias="Operou Bolsa?")
    traded_fund: Bool = Field(alias="Operou Fundo?")
    traded_fixed_income: Bool = Field(alias="Operou Renda Fixa?")
    declared_financial_investments: Money = Field(
        alias="Aplicação Financeira Declarada"
    )
    revenue: Money = Field(alias="Receita no Mês")
    revenue_bovespa: Money = Field(alias="Receita Bovespa")
    revenue_future: Money = Field(alias="Receita Bovespa")
    revenue_fixed_income_banking: Money = Field(alias="Receita RF Bancários")
    revenue_fixed_income_private: Money = Field(alias="Receita RF Privados")
    revenue_fixed_income_public: Money = Field(alias="Receita RF Públicos")
    deposits_gross: Money = Field(alias="Captação Bruta em M")
    withdrawals: Money = Field(alias="Resgate em M")
    deposits_liquid: Money = Field(alias="Captação Líquida em M")
    deposits_ted: Money = Field(alias="Captação TED")
    deposits_st: Money = Field(alias="Captação ST")
    deposits_ota: Money = Field(alias="Captação OTA")
    deposits_fixed_income: Money = Field(alias="Captação RF")
    deposits_treasure: Money = Field(alias="Captação TD")
    deposits_private_pension: Money = Field(alias="Captação PREV")
    patrimony_last_month: Money = Field(alias="Net em M-1")
    patrimony: Money = Field(alias="Net Em M")
    patrimony_fixed_income: Money = Field(alias="Net Renda Fixa")
    patrimony_real_estate: Money = Field(alias="Net Fundos Imobiliários")
    patrimony_equity: Money = Field(alias="Net Renda Variável")
    patrimony_fund: Money = Field(alias="Net Fundos")
    patrimony_balance: Money = Field(alias="Net Financeiro")
    patrimony_private_pension: Money = Field(alias="Net Previdência")
    patrimony_other: Money = Field(alias="Net Outros")
    revenue_rental: Money = Field(alias="Receita Aluguel")
    revenue_complement: Money = Field(alias="Receita Complemento/Pacote Corretagem")

    @validator("sex", pre=True)
    def map_sex(cls, v):
        match v:
            case "F":
                return Sex.F
            case "M":
                return Sex.M

    @validator("segment", pre=True)
    def map_segment(cls, v):
        match v:
            case "Private":
                return PositivadorSegment.PRIVATE
            case "Express":
                return PositivadorSegment.EXPRESS
            case "Unique":
                return PositivadorSegment.UNIQUE
            case "Plus":
                return PositivadorSegment.PLUS
            case "NÃO DISPONÍVEL":
                return PositivadorSegment.NOT_AVAILABLE

    @validator("is_active", pre=True)
    def map_is_active(cls, v):
        match v:
            case "INATIVO":
                return False
            case "ATIVO":
                return True

    @classmethod
    def get_excel_dataframe(cls, path, *args, **kwargs):
        _, filename = os.path.split(path)
        match = PATTERN.match(filename)
        report_date = date(*[int(i) for i in match.group("year", "month", "day")])
        df = super().get_excel_dataframe(path, *args, **kwargs)
        df["date"] = [None, "date"] + (len(df) - 2) * [report_date]
        return df

    @classmethod
    def clean_excel_dataframe(cls, df):
        df = df.replace({np.nan: None})
        df.columns = df.iloc[1]
        df = df.iloc[2:]
        return df


class PositivadorQuerySet(models.QuerySet):
    def month(self, date=None):
        date = date or timezone.localdate()
        return self.filter(date__month=date.month, date__year=date.year)

    def patrimony(self):
        aggregators = {
            field: Coalesce(Sum(f"patrimony_{field}"), Decimal("0.00"))
            for field in PATRIMONY_FIELDS
        } | {"total": Coalesce(Sum("patrimony"), Decimal("0.00"))}
        return self.aggregate(**aggregators)

    def current(self):
        try:
            return self.filter(date=self.latest().date)
        except self.model.DoesNotExist:
            return self.none()

    def per_category(self):
        aggregators = {
            field.name: Coalesce(Sum(field.name), Decimal("0.00"))
            for field in self.model._meta.get_fields()
            if isinstance(field, models.DecimalField)
        }
        return self.aggregate(**aggregators)


class PositivadorManager(models.Manager):
    def update_from_excel(self, *args, **kwargs):
        positivador = PositivadorParser.read_excel(*args, **kwargs)
        for line in positivador:
            obj = self.model(**line.dict())
            obj.save()


class Positivador(models.Model):
    date = models.DateField(
        verbose_name="Data",
    )
    advisor = models.ForeignKey(
        verbose_name="Assessor",
        to=settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="positivador_set",
    )
    xp_account = models.ForeignKey(
        verbose_name="Cliente",
        to="xpaccount.XPAccount",
        on_delete=models.PROTECT,
        related_name="positivador_set",
    )
    occupation = models.CharField(
        verbose_name="Profissão",
        max_length=256,
    )
    sex = models.CharField(
        verbose_name="Sexo",
        max_length=1,
        choices=Sex.choices,
        null=True,
        blank=True,
    )
    segment = models.CharField(
        verbose_name="Segmento",
        max_length=64,
        choices=PositivadorSegment.choices,
        null=True,
        blank=True,
    )
    sign_up_date = models.DateField(
        verbose_name="Data de Cadastro",
    )
    made_second_deposit = models.BooleanField(
        verbose_name="Fez segundo aporte?",
    )
    birth_date = models.DateField(
        verbose_name="Data de Nascimento",
    )
    is_active = models.BooleanField(
        verbose_name="Status",
    )
    actived = models.BooleanField(
        verbose_name="Ativou em M?",
    )
    evaded = models.BooleanField(
        verbose_name="Evadiu em M?",
    )
    traded_bovespa = models.BooleanField(
        verbose_name="Operou Bolsa?",
    )
    traded_fund = models.BooleanField(
        verbose_name="Operou Fundo?",
    )
    traded_fixed_income = models.BooleanField(
        verbose_name="Operou Renda Fixa?",
    )
    declared_financial_investments = models.DecimalField(
        verbose_name="Aplicação Financeira Declarada",
        max_digits=36,  # Números absurdos aparecem de vez em quando
        decimal_places=2,
    )
    revenue = models.DecimalField(
        verbose_name="Receita no Mês",
        max_digits=12,
        decimal_places=2,
    )
    revenue_bovespa = models.DecimalField(
        verbose_name="Receita Bovespa",
        max_digits=12,
        decimal_places=2,
    )
    revenue_future = models.DecimalField(
        verbose_name="Receita Futuros",
        max_digits=12,
        decimal_places=2,
    )
    revenue_fixed_income_banking = models.DecimalField(
        verbose_name="Receita RF Bancários",
        max_digits=12,
        decimal_places=2,
    )
    revenue_fixed_income_private = models.DecimalField(
        verbose_name="Receita RF Privados",
        max_digits=12,
        decimal_places=2,
    )
    revenue_fixed_income_public = models.DecimalField(
        verbose_name="Receita RF Públicos",
        max_digits=12,
        decimal_places=2,
    )
    deposits_gross = models.DecimalField(
        verbose_name="Captação Bruta em M",
        max_digits=12,
        decimal_places=2,
    )
    withdrawals = models.DecimalField(
        verbose_name="Resgate em M",
        max_digits=12,
        decimal_places=2,
    )
    deposits_liquid = models.DecimalField(
        verbose_name="Captação Líquida em M",
        max_digits=12,
        decimal_places=2,
    )
    deposits_ted = models.DecimalField(
        verbose_name="Captação TED",
        max_digits=12,
        decimal_places=2,
    )
    deposits_st = models.DecimalField(
        verbose_name="Captação ST",
        max_digits=12,
        decimal_places=2,
    )
    deposits_ota = models.DecimalField(
        verbose_name="Captação OTA",
        max_digits=12,
        decimal_places=2,
    )
    deposits_fixed_income = models.DecimalField(
        verbose_name="Captação OTA",
        max_digits=12,
        decimal_places=2,
    )
    deposits_treasure = models.DecimalField(
        verbose_name="Captação OTA",
        max_digits=12,
        decimal_places=2,
    )
    deposits_private_pension = models.DecimalField(
        verbose_name="Captação OTA",
        max_digits=12,
        decimal_places=2,
    )
    patrimony_last_month = models.DecimalField(
        verbose_name="Net em M-1",
        max_digits=12,
        decimal_places=2,
    )
    patrimony = models.DecimalField(
        verbose_name="Net em M",
        max_digits=12,
        decimal_places=2,
    )
    patrimony_fixed_income = models.DecimalField(
        verbose_name="Net Renda Fixa",
        max_digits=12,
        decimal_places=2,
    )
    patrimony_real_estate = models.DecimalField(
        verbose_name="Net Fundos Imobiliários",
        max_digits=12,
        decimal_places=2,
    )
    patrimony_equity = models.DecimalField(
        verbose_name="Net Renda Váriavel",
        max_digits=12,
        decimal_places=2,
    )
    patrimony_fund = models.DecimalField(
        verbose_name="Net Fundos",
        max_digits=12,
        decimal_places=2,
    )
    patrimony_balance = models.DecimalField(
        verbose_name="Net Financeiro",
        max_digits=12,
        decimal_places=2,
    )
    patrimony_private_pension = models.DecimalField(
        verbose_name="Net Previdência",
        max_digits=12,
        decimal_places=2,
    )
    patrimony_other = models.DecimalField(
        verbose_name="Net Outros",
        max_digits=12,
        decimal_places=2,
    )
    revenue_rental = models.DecimalField(
        verbose_name="Receita Aluguel",
        max_digits=12,
        decimal_places=2,
    )
    revenue_complement = models.DecimalField(
        verbose_name="Receita Complemento/Pacote Corretagem",
        max_digits=12,
        decimal_places=2,
    )

    objects = PositivadorManager.from_queryset(PositivadorQuerySet)()

    class Meta:
        get_latest_by = "date"
        ordering = ["-date"]
        verbose_name = "Positivador"
        verbose_name_plural = "Positivadores"
