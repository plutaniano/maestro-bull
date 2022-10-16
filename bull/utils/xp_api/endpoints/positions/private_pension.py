from decimal import Decimal
from django.db.models import TextChoices
from pydantic import BaseModel, Field, validator
from bull.utils.pydantic_types import Date, Money


class PrivatePensionPlan(TextChoices):
    PGBL = "pgbl", "PGBL"
    VGBL = "vgbl", "VGBL"


class PrivatePensionStatus(TextChoices):
    ACTIVE = "active", "Ativo"
    BLOCKED = "blocked", "Bloqueado"
    CANCELED = "cancelled", "Cancelado"
    PENDING = "pending", "Pendente"


class PrivatePensionContribution(TextChoices):
    ESPORADIC = "sporadic", "Esporádica"
    MONTHLY = "monthly", "Mensal"


class PrivatePensionTaxation(TextChoices):
    REGRESSIVE = "regressive", "Regressivo"
    PROGRESSIVE = "progressive", "Progressive"


class PrivatePensionPayment(TextChoices):
    BOLETO = "boleto", "Boleto"
    DEBIT = "debit", "Débito em Conta Corrente"
    DEBIT_FROM_XP_ACCOUNT = "debit_from_xp_account", "Débito em Conta XP"
    UNIDENTIFIED = "unidentified", "Não Identificado"


class PrivatePension(BaseModel):
    asset: str = Field(alias="active")
    balance: Money = Field(alias="balance")
    certificate: str = Field(alias="certificate")
    cnpj: str = Field(alias="cnpj")
    contribution: PrivatePensionContribution = Field(alias="contribution")
    gross_income: Money = Field(alias="grossIncome")
    insured: str = Field(alias="insured")
    insurer: str = Field(alias="insurer")
    payment: PrivatePensionPayment = Field(alias="payment")
    plan: PrivatePensionPlan = Field(alias="plan")
    position: Money = Field(alias="position")
    proposal_code: int = Field(alias="proposalCode")
    quota_date: Date = Field(alias="quotaDate")
    quota_value: float = Field(alias="quotaValue")
    quotas: float = Field(alias="quotas")
    start_date: Date = Field(alias="startDate")
    status: PrivatePensionStatus = Field(alias="status")
    susep: str = Field(alias="susep")
    taxation: PrivatePensionTaxation = Field(alias="taxation")
    total_invested: Money = Field(alias="totalApplied")
    total_rescue: Money = Field(alias="totalRescue")

    @validator("contribution", pre=True)
    def normalize_contribution(cls, v):
        match v:
            case "Esporádica":
                return PrivatePensionContribution.ESPORADIC
            case "Mensal":
                return PrivatePensionContribution.MONTHLY

    @validator("payment", pre=True)
    def normalize_payment(cls, v):
        match v:
            case "Boleto":
                return PrivatePensionPayment.BOLETO
            case "Débito em Conta Corrente":
                return PrivatePensionPayment.DEBIT
            case "Débito em Conta XP":
                return PrivatePensionPayment.DEBIT_FROM_XP_ACCOUNT
            case "Não Identificado":
                return PrivatePensionPayment.UNIDENTIFIED

    @validator("plan", pre=True)
    def normalize_plan(cls, v):
        return PrivatePensionPlan[v.upper()]

    @validator("status", pre=True)
    def normalize_status(cls, v):
        match v:
            case "Ativo":
                return PrivatePensionStatus.ACTIVE
            case "Bloqueado":
                return PrivatePensionStatus.BLOCKED
            case "Cancelado":
                return PrivatePensionStatus.CANCELED
            case "Pendente":
                return PrivatePensionStatus.PENDING

    @validator("taxation", pre=True)
    def normalize_taxation(cls, v):
        match v:
            case "Regressivo":
                return PrivatePensionTaxation.REGRESSIVE
            case "Progressivo":
                return PrivatePensionTaxation.PROGRESSIVE


class PrivatePensionResponse(BaseModel):
    details: list[PrivatePension] = Field(alias="details")
    percent: float = Field(alias="percent")
    percent_detail: float = Field(alias="percentDetail")
    value: Money = Field(alias="value")
    yield_: Decimal = Field(alias="yield")
