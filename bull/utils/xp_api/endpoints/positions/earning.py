from django.db.models import TextChoices
from pydantic import BaseModel, Field, validator
from bull.utils.pydantic_types import Date, Money


class SubGroupName(TextChoices):
    EQUITY = "equity", "Ações"
    REAL_ESTATE = "real_estate", "Fundos Imobiliários"
    FIXED_INCOME = "fixed_income", "Renda Fixa"


class Equity(BaseModel):
    pass


class RealEstate(BaseModel):
    pass


class Earning(BaseModel):
    payment_date: Date | None = Field(alias="payment")
    product: str = Field(alias="product")
    provisioned_value: Money = Field(alias="provisionedValue")
    quantity: int = Field(alias="quantity")
    # muitos tipos com nomes diferentes mas que são a mesma coisa
    # implementar enum? como? TODO
    type: str = Field(alias="type")

    @validator("payment_date")
    def ignore_absurd_dates(cls, v):
        if v.year >= 2500:
            return None
        return v


class EarningGroup(BaseModel):
    categories_id: None = Field(alias="categoriesId")
    items: list[Earning] = Field(alias="items")
    name: SubGroupName = Field(alias="name")
    percent: float = Field(alias="percent")

    @validator("name", pre=True)
    def normalize_name(cls, v):
        match v:
            case "AÇÕES":
                return SubGroupName.EQUITY
            case "RENDA FIXA":
                return SubGroupName.FIXED_INCOME
            case "FUNDOS IMOBILIÁRIOS":
                return SubGroupName.REAL_ESTATE


class EarningResponse(BaseModel):
    equities: list[Equity] = Field(alias="equities")
    real_estate: list[RealEstate] = Field(alias="realEstateFunds")
    sub_groups: list[EarningGroup] = Field(alias="subGroups")
    value: Money = Field(alias="value")
    percent: float = Field(alias="percent")
