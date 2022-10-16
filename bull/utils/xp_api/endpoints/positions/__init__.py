from datetime import datetime

from django.utils import timezone
from pydantic import BaseModel, Field, validator
from bull.utils.pydantic_types import Money

from ..base import XpApiEndpoint
from .assets_warranty import AssetsWarrantyResponse
from .balance import Balance
from .coe import CoeResponse
from .earning import EarningResponse
from .equity import EquityResponse
from .fixed_income import FixedIncomeResponse
from .future import FutureResponse
from .gold import GoldResponse
from .insurance import InsuranceResponse
from .investment_club import InvestmentClubResponse
from .investment_fund import InvestmentFundResponse
from .option import OptionResponse
from .private_pension import PrivatePensionResponse
from .real_estate import RealEstateResponse
from .rental import RentalResponse
from .structured_product import StructuredProductResponse
from .term import TermResponse
from .treasure import TreasureResponse


class Positions(BaseModel):
    amount: Money
    assets_warranty: AssetsWarrantyResponse = Field(alias="assetsWarranty")
    balance: Balance
    coe: CoeResponse
    declared_patrimony: Money = Field(alias="totalWealth")
    earning: EarningResponse
    equity: EquityResponse
    financial_investments: Money = Field(alias="financialInvestments")
    fixed_income: FixedIncomeResponse = Field(alias="fixedIncome")
    future: FutureResponse
    gold: GoldResponse
    insurance: InsuranceResponse
    investment_club: InvestmentClubResponse = Field(alias="investmentClub")
    investment_fund: InvestmentFundResponse = Field(alias="investmentFund")
    margin_account: int = Field(alias="marginAccount")
    option: OptionResponse
    patrimony: Money
    private_pension: PrivatePensionResponse = Field(alias="privatePension")
    real_estate: RealEstateResponse = Field(alias="realEstate")
    rental: RentalResponse
    structured_product: StructuredProductResponse = Field(alias="structuredProduct")
    term: TermResponse
    treasure: TreasureResponse
    updated_formatted: str = Field(alias="updatedFormated")
    updated_at: datetime = Field(alias="updated")
    xp_account_id: int = Field(alias="id")

    # extra
    raw_json: dict = Field(default_factory=dict)

    @validator("updated_at")
    def make_updated_tz_aware(cls, v):
        return timezone.make_aware(v)


class PositionsResponse(BaseModel):
    customer: Positions


class Positions(XpApiEndpoint):
    model = PositionsResponse

    @classmethod
    def get_path(cls, xp_account):
        return f"/rede-customer/v2/customers/{xp_account}/positions?createCache=true"

    @classmethod
    def parse_response(cls, response):
        raw_json = response.json()
        parsed_response = super().parse_response(response).customer
        parsed_response.raw_json = raw_json["customer"]
        return parsed_response

    @classmethod
    def get_query_params(cls, xp_account):
        return {"xp_account": xp_account}
