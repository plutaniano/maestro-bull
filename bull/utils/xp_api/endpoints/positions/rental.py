from decimal import Decimal
from django.db.models import TextChoices
from pydantic import BaseModel, Field, validator

from bull.utils.pydantic_types import Date, Money


class RentalCounterPartyType(TextChoices):
    LENDER = "lender", "Doador"
    BORROWER = "borrower", "Tomador"


class Rental(BaseModel):
    amount: int = Field(alias="amount")
    average_cost_status: int = Field(alias="averageCostStatus")
    average_cost: Money = Field(alias="averageCost")
    counterparty_type: RentalCounterPartyType = Field(alias="counterPartType")
    last_quote: Money = Field(alias="lastQuotation")
    maturity: Date = Field(alias="maturity")
    performance: float = Field(alias="performance")
    position: Money = Field(alias="position")
    structured_amount: int = Field(alias="structuredAmount")
    ticker: str = Field(alias="paper")
    total_amount: int = Field(alias="totalAmount")

    @validator("counterparty_type", pre=True)
    def normalize_counterparty_type(cls, v):
        match v:
            case "Doador":
                return RentalCounterPartyType.LENDER
            case "Tomador":
                return RentalCounterPartyType.BORROWER


class RentalResponse(BaseModel):
    details: list[Rental]
    percent: Decimal
    value: Money
