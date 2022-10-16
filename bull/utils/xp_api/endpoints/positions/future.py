from pydantic import BaseModel, Field
from bull.utils.pydantic_types import Money, Date


class Future(BaseModel):
    goods: str = Field(alias="goods")
    ticker: str = Field(alias="instrument")
    due_date: Date = Field(alias="due")
    market: str = Field(alias="market")
    position: int = Field(alias="position")
    day_quantity: int = Field(alias="day")
    quantity: int = Field(alias="total")
    description: str = Field(alias="description")


class FutureResponse(BaseModel):
    yield_: Money = Field(alias="yield")
    value: Money = Field(alias="value")
    details: list[Future] = Field(alias="details")
