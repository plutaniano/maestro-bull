from decimal import Decimal

import numpy as np
from bull.apps.reports.models.base import Parser
from bull.apps.xpaccount.models import XPAccount
from bull.utils.pydantic_types import Advisor, Date, Money
from django.conf import settings
from django.db import models
from django.db.models import Q, Sum
from django.db.models.functions import Coalesce
from django.utils import timezone
from pydantic import Field, validator


class CaptacaoType(models.TextChoices):
    CBX = "cbx", "CBX"
    CEX = "cex", "CEX"
    COE = "coe", "COE"
    CPJ = "cpj", "CPJ"
    FIXED_INCOME = "fixed_income", "Renda Fixa"
    OTA = "ota", "OTA"
    PCO_FUNDS = "pco_funds", "Fundos PCO"
    PRIVATE_PENSION = "private_pension", "Previdência"
    PRIVATE_PENSION_INTERNAL = "private_pension_internal", "Previdência Interna"
    ST = "st", "ST"
    STVM = "stvm", "STVM"
    TED = "ted", "TED"
    TREASURE = "treasure", "TD"


class CaptacaoAux(models.TextChoices):
    DEPOSIT = "deposit", "Entrada"
    WITHDRAWAL = "withdrawal", "Saída"


class CaptacaoParser(Parser):
    office: str = Field(alias="Escritório")
    date: Date = Field(alias="Data")
    advisor: Advisor = Field(alias="Assessor")
    xp_account: XPAccount = Field(alias="Cód do Cliente")
    type: CaptacaoType = Field(alias="Tipo de Captação")
    aux: CaptacaoAux = Field(alias="Aux")
    amount: Money = Field(alias="Captação")

    @validator("type", pre=True)
    def map_type(cls, v):
        match v:
            case "CBX":
                return CaptacaoType.CBX
            case "CEX":
                return CaptacaoType.CEX
            case "COE":
                return CaptacaoType.COE
            case "RF":
                return CaptacaoType.FIXED_INCOME
            case "OTA":
                return CaptacaoType.OTA
            case "FUNDOS PCO":
                return CaptacaoType.PCO_FUNDS
            case "PREV":
                return CaptacaoType.PRIVATE_PENSION
            case "PREV INTERNA":
                return CaptacaoType.PRIVATE_PENSION_INTERNAL
            case "STVM":
                return CaptacaoType.STVM
            case "TED":
                return CaptacaoType.TED
            case "TD":
                return CaptacaoType.TREASURE
            case "ST":
                return CaptacaoType.ST
            case "CPJ":
                return CaptacaoType.CPJ

    @validator("aux", pre=True)
    def map_aux(cls, v):
        match v:
            case "C":
                return CaptacaoAux.DEPOSIT
            case "D":
                return CaptacaoAux.WITHDRAWAL

    @classmethod
    def clean_excel_dataframe(cls, df):
        df.columns = df.iloc[1]  # renomeia colunas
        df = df.iloc[2:]  # remove as linhas em branco no topo da planilha
        df = df.replace({np.nan: None})
        return df


class CaptacaoQuerySet(models.QuerySet):
    def month(self, date=None):
        date = date or timezone.localdate()
        return self.filter(date__month=date.month, date__year=date.year)

    def deposits(self):
        return self.aggregate(
            withdrawals=Coalesce(
                Sum("amount", filter=Q(aux="withdrawal")), Decimal("0.00")
            ),
            deposits=Coalesce(Sum("amount", filter=Q(aux="deposit")), Decimal("0.00")),
            liquid=Coalesce(Sum("amount"), Decimal("0.00")),
        )


class CaptacaoManager(models.Manager):
    def update_from_excel(self, *args, delete_old=True, **kwargs):
        deposits = CaptacaoParser.read_excel(*args, **kwargs)
        if len(deposits) == 0:
            return
        if delete_old:
            self.filter(
                date__month=deposits[0].date.month,
                date__year=deposits[0].date.year,
            ).delete()
        for deposit in deposits:
            self.create(**deposit.dict())


class Captacao(models.Model):
    office = models.CharField(
        verbose_name="Escritório",
        max_length=128,
    )
    date = models.DateField(
        verbose_name="Data",
    )
    advisor = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        verbose_name="Assessor",
        related_name="captacao_set",
    )
    xp_account = models.ForeignKey(
        to="xpaccount.XPAccount",
        on_delete=models.PROTECT,
        verbose_name="Conta XP",
        related_name="captacao_set",
    )
    type = models.CharField(
        verbose_name="Tipo de Captação",
        max_length=32,
        choices=CaptacaoType.choices,
    )
    aux = models.CharField(
        verbose_name="Aux",
        max_length=16,
        choices=CaptacaoAux.choices,
    )
    amount = models.DecimalField(
        verbose_name="Captação",
        max_digits=12,
        decimal_places=2,
    )

    objects = CaptacaoManager.from_queryset(CaptacaoQuerySet)()

    class Meta:
        verbose_name = "Captação"
        verbose_name_plural = "Captações"
