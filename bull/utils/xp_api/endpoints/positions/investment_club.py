from decimal import Decimal
from pydantic import BaseModel


class InvestmentClub(BaseModel):
    pass


class InvestmentClubResponse(BaseModel):
    value: Decimal
    percent: Decimal
    details: list[InvestmentClub]
