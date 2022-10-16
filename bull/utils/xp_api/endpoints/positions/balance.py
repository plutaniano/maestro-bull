from pydantic import BaseModel, Field
from bull.utils.pydantic_types import Money, Date


class Balance(BaseModel):
    percent: float = Field(alias="percent")
    available_balance: Money = Field(alias="availableCash")
    warranty: Money = Field(alias="warranty")
    pending_withdrawal_funds: Money = Field(alias="pendingFunds")
    pending_withdrawal_clubs: Money = Field(alias="rescuePendingClub")
    expiring_terms: Money = Field(alias="expireTerms")
    margin_account: Money = Field(alias="marginAccount")
    future_releases: Money = Field(alias="futureReleases")
    projected_balance_1: Money = Field(alias="projectedBalanced1")
    projected_balance_1_date: Date = Field(alias="projectedBalancedDate1")
    projected_balance_2: Money = Field(alias="projectedBalanced2")
    projected_balance_2_date: Date = Field(alias="projectedBalancedDate2")
    projected_balance_3: Money = Field(alias="projectedBalanced3")
    projected_balance_3_date: Date = Field(alias="projectedBalancedDate3")
    projected_balance_over: Money = Field(alias="projectedBalancedOver")
    total_projected_balance: Money = Field(alias="projectedTotal")
    warranty_bmf: Money = Field(alias="warrantyBmf")
    warranty_bovespa: Money = Field(alias="warrantyBovespa")
    withdraw_balance: Money = Field(alias="withdrawBalance")
