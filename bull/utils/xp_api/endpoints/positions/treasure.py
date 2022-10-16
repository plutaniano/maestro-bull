from django.db.models import TextChoices
from pydantic import BaseModel, Field, validator
from bull.utils.pydantic_types import Date, Money


class TreasureType(TextChoices):
    LFT = "lft", "LFT"
    LTN = "ltn", "LTN"
    NTNB = "ntnb", "NTN-B"
    NTNB_PRINCIPAL = "ntnb_principal", "NTN-B Principal"
    NTNC = "ntnc", "NTN-C"
    NTNF = "ntnf", "NTN-F"


class Treasure(BaseModel):
    available: float = Field(alias="avaiable")  # erro de grafia da XP
    due_date: Date = Field(alias="due")
    last_quote: Money = Field(alias="lastQuote")
    position: Money = Field(alias="position")
    product_id: int = Field(alias="productId")
    quantity: float = Field(alias="quantity")
    title: TreasureType = Field(alias="title")
    type: TreasureType = Field(alias="type")
    type_code: int = Field(alias="typeCode")
    warranty: float = Field(alias="warranty")

    @validator("type", "title", pre=True)
    def normalize_treasure_type(cls, v):
        match v:
            case "NTNB PRINC":
                return TreasureType.NTNB_PRINCIPAL
        return TreasureType[v.upper().replace("-", "")]


class TreasureGroup(BaseModel):
    categories_id: list[int] = Field(alias="categoriesId")
    items: list[Treasure] = Field(alias="items")
    name: str = Field(alias="name")
    percent: float = Field(alias="percent")


class TreasureResponse(BaseModel):
    percent: float = Field(alias="percent")
    value: Money = Field(alias="value")
    sub_groups: list[TreasureGroup] = Field(alias="subGroups")
