from pydantic import BaseModel, Field, validator
from django.db.models import TextChoices

from bull.utils.pydantic_types import Date, Money


class CoeIssuers(TextChoices):
    BNP_PARIBAS = "bnp_paribas", "BNP Paribas"
    CITIBANK = "citibank", "Citibank"
    CREDIT_SUISSE = "credit_suisse", "Credit Suisse"
    GOLDMAN_SACHS = "goldman_sachs", "Goldman Sachs"
    JP_MORGAN = "jp_morgan", "JP Morgan"
    MORGAN_STANLEY = "morgan_stanley", "Morgan Stanley"
    XP = "xp", "XP"


class Coe(BaseModel):
    application_date: Date = Field(alias="applicationDate")
    applied_value: Money = Field(alias="appliedValue")
    due_date: Date = Field(alias="due")
    issuer: CoeIssuers = Field(alias="emitter")
    gross_value: Money = Field(alias="grossValue")
    name: str = Field(alias="name")
    product_id: int = Field(alias="productId")
    quantity: int = Field(alias="quantity")
    unit_price: Money = Field(alias="unitPrice")

    @validator("issuer", pre=True)
    def normalize_issuer(cls, v):
        match v:
            case "BANCO BNP PARIBAS BR":
                return CoeIssuers.BNP_PARIBAS
            case "BANCO XP S.A.":
                return CoeIssuers.XP
            case "GOLDMAN SACHS DO BRASIL BANCO MULTIPLO S.A.":
                return CoeIssuers.GOLDMAN_SACHS
            case "BANCO MORGAN STANLEY SA":
                return CoeIssuers.MORGAN_STANLEY
            case "BANCO JP MORGAN":
                return CoeIssuers.JP_MORGAN
            case "BANCO CITIBANK S/A":
                return CoeIssuers.CITIBANK
            case "BANCO CREDIT SUISSE SA":
                return CoeIssuers.CREDIT_SUISSE


class CoeResponse(BaseModel):
    details: list[Coe] = Field(alias="details")
    percent: float = Field(alias="percent")
    percent_detail: float = Field(alias="percentDetail")
    value: Money = Field(alias="value")
