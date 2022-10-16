from pydantic import BaseModel, Field

from bull.utils.pydantic_types import Date, Money


class Term(BaseModel):
    due_date: Date = Field(alias="due")
    entry_price: Money = Field(alias="entranceFee")
    position: Money = Field(alias="financial")
    last_quote: Money = Field(alias="lastQuote")
    quantity: int = Field(alias="quantity")
    roll_date: Date = Field(alias="rollingDate")
    ticker: str = Field(alias="product")


class TermResponse(BaseModel):
    details: list[Term]
    percent: float
    percent_detail: float = Field(alias="percentDetail")
    value: Money
