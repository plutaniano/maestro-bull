from pydantic import BaseModel, Field
from bull.utils.pydantic_types import Money
from decimal import Decimal


class Gold(BaseModel):
    weight: Money = Field(alias="weight")
    product: str = Field(alias="product")
    contracts: int = Field(alias="contract")
    unit_price: Decimal = Field(alias="unitPrice")
    position: Money = Field(alias="position")


class GoldResponse(BaseModel):
    value: Money
    details: list[Gold]
