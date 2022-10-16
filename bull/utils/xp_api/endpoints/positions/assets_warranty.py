from bull.utils.pydantic_types import Money, Date
from pydantic import BaseModel, Field


class EquityWarranty(BaseModel):
    financial_bov: Money = Field(alias="financialBov")
    financial_bvmf: Money = Field(alias="financialBvmf")
    ticker: str = Field(alias="paper")
    total_financial: Money = Field(alias="totalFinancial")
    total_quantity: int = Field(alias="totalQuantity")
    unitary_price: Money = Field(alias="unitaryPrice")
    warranty_bov: int = Field(alias="warrantyBov")
    warranty_bvmf: int = Field(alias="warrantyBvmf")


class FixedIncomeWarranty(BaseModel):
    asset: str = Field(alias="asset")
    due_date: Date = Field(alias="due")
    issuer: str = Field(alias="emmiter")
    total_financial: Money = Field(alias="totalFinancial")
    total_quantity: int = Field(alias="totalQuantity")


class TreasureWarranty(BaseModel):
    asset: str = Field(alias="asset")
    due_date: Date = Field(alias="due")
    last_quote: Money = Field(alias="lastQuote")
    total_financial: Money = Field(alias="totalFinancial")
    total_quantity: int = Field(alias="totalQuantity")


class AssetsWarrantyResponse(BaseModel):
    equities: list[EquityWarranty] = Field(alias="equities")
    fixed_incomes: list[FixedIncomeWarranty] = Field(alias="fixedIncomes")
    treasures: list[TreasureWarranty] = Field(alias="treasures")
