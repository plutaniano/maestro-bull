from decimal import Decimal
from pydantic import BaseModel, Field

from bull.utils.pydantic_types import Money


class RealEstate(BaseModel):
    average_cost_status: int = Field(alias="averageCostStatus")
    average_cost: Money = Field(alias="averageCost")
    last_quote: Money = Field(alias="lastQuote")
    performance: int = Field(alias="performance")
    position: Money = Field(alias="financial")
    quantity_available: int = Field(alias="quantityAvailable")
    quantity_blocked: int = Field(alias="quantidadeBloqueada")
    quantity_day: int = Field(alias="quantityDay")
    quantity_projected: int = Field(alias="quantityDesigned")
    quantity_total: int = Field(alias="quantityTotal")
    ticker: str = Field(alias="name")


class RealEstateResponse(BaseModel):
    details: list[RealEstate] = Field(alias="details")
    percent_detail: Decimal = Field(alias="percentDetail")
    percent: Decimal = Field(alias="percent")
    value: Money = Field(alias="value")
