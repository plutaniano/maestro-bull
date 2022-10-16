from pydantic import BaseModel, Field

from bull.utils.pydantic_types import Money, Date


class RewardedAsset(BaseModel):
    expiry_date: Date = Field(alias="expiryDate")
    financial: Money = Field(alias="finance")
    ticker: str = Field(alias="productId")
    quantity: int = Field(alias="quantity")
    quote: Money = Field(alias="quote")


class RewardedAssetResponse(BaseModel):
    details: list[RewardedAsset] = Field(alias="details")


class Equity(BaseModel):
    available: int = Field(alias="avaiable")
    average_cost: Money = Field(alias="averageCost")
    average_cost_status: int = Field(alias="averageCostStatus")
    financial: Money = Field(alias="finance")
    performance: float = Field(alias="performance")
    ticker: str = Field(alias="productId")
    quantity: int = Field(alias="quantity")
    quantity_day: int = Field(alias="quantityDay")
    quantity_projected: int = Field(alias="quantityProjected")
    quantity_structured: int = Field(alias="quantityStructured")
    quote: Money = Field(alias="quote")
    warranty_bovespa: int = Field(alias="warrantyBOV")
    warranty_bvmf: int = Field(alias="warrantyBVMF")


class EquityResponse(BaseModel):
    value: Money = Field(alias="value")
    yield_: Money = Field(alias="yield")
    percent: float = Field(alias="percent")
    percent_detail: float = Field(alias="percentDetail")
    details: list[Equity]
    rewarded_asset: RewardedAssetResponse = Field(alias="rewardedAsset")
