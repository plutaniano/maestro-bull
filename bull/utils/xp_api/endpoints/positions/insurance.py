from pydantic import BaseModel, Field, validator
from django.db.models import TextChoices

from bull.utils.pydantic_types import Date, Money
from bull.utils.enums import Insurers


class InsuranceTypes(TextChoices):
    LIFE = "life", "Vida"


class InsuranceStatus(TextChoices):
    ACTIVE = "active", "Ativa"


class Insurance(BaseModel):
    insured_capital: Money = Field(alias="capitalInsured")
    coverage_type: int = Field(alias="coveraype")
    type: InsuranceTypes = Field(alias="field")
    insurer: Insurers = Field(alias="insurance")
    premium: Money = Field(alias="premium")
    product: str = Field(alias="product")
    status: InsuranceStatus = Field(alias="status")
    contract_date: Date = Field(alias="tradeDate")

    @validator("type", pre=True)
    def normalize_field(cls, v):
        match v:
            case "VIDA":
                return InsuranceTypes.LIFE

    @validator("status", pre=True)
    def normalize_status(cls, v):
        match v:
            case "Ativa":
                return InsuranceStatus.ACTIVE

    @validator("insurer", pre=True)
    def normalize_insurer(cls, v):
        return Insurers[v.replace(" ", "_")]


class InsuranceResponse(BaseModel):
    value: Money
    details: list[Insurance]
