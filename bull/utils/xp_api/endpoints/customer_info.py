from datetime import date
from decimal import Decimal

from bull.utils.pydantic_types import Money
from bull.utils.xp_api.endpoints.base import XpApiEndpoint
from pydantic import BaseModel, Field, validator


class CustomerInfo(BaseModel):
    id: int
    cpf_cnpj: str = Field(alias="cpfCnpj")
    advisor_id: int = Field(alias="advisorId")
    advisor_name: str = Field(alias="advisorName")
    xp_account: int = Field(alias="xpAccount")
    name: str
    cellphone: str
    phone: str
    email: str
    suitability: str
    suitability_display_name: str = Field(alias="suitabilityDisplayName")
    suitability_expired: bool = Field(alias="suitabilityExpired")
    amount: Money
    patrimony: Money
    expiration_date: date = Field(alias="expirationDate")
    expiration_date_display_name: str = Field(alias="expirationDateDisplayName")
    investor_qualification: str = Field(alias="investorQualification")
    share_of_wallet: Decimal = Field(alias="shareOfWallet")
    total_wealth: Money = Field(alias="totalWealth")
    is_qualified: bool = Field(alias="isQualified")
    has_account: None = Field(alias="hasAccount")
    has_patrimony: None = Field(alias="hasPatrimony")
    description: None
    status: None
    lead_id: None = Field(alias="leadId")
    birth_date: None = Field(alias="birthDate")

    @validator("advisor_id", pre=True)
    def validate_advisor_id(cls, v):
        return v[1:]


class CustomerInfoResponse(BaseModel):
    customer_info: CustomerInfo = Field(alias="customer-info")


class CustomerInfo(XpApiEndpoint):
    model = CustomerInfoResponse

    @classmethod
    def get_path(cls, xp_account):
        return f"/rede-customer/v1/customers/{xp_account}"

    @classmethod
    def get_query_params(cls, xp_account):
        return {"xp_account": xp_account}
