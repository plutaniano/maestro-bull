from datetime import date, datetime
from decimal import Decimal

from bull.utils.pydantic_types import Advisor
from bull.utils.xp_api.endpoints.base import XpApiEndpoint
from django.utils import timezone
from pydantic import BaseModel, Field, validator


class Order(BaseModel):
    id: str
    origin: str
    brand: int
    operation_number: int = Field(alias="operationNumber")
    requester: str
    status_type: str = Field(alias="statusType")
    create_date: datetime = Field(alias="createDate")
    create_time: datetime = Field(alias="createTime")
    operation_type: str = Field(alias="operationType")
    last_event_business: int = Field(alias="lastEventBusiness")
    quote_date: datetime = Field(alias="quoteDate")
    process_attempt_count: int = Field(alias="processAttemptCount")
    last_processing_date: datetime | None = Field(alias="lastProcessingDate")
    settlement_date: datetime | None = Field(alias="settlementDate")
    value: Decimal
    iof: Decimal = Field(alias="iofValue")
    income_tax: Decimal = Field(alias="incomeTaxValue")
    settlement: Decimal | None = Field(alias="settlementValue")
    can_cancel: bool = Field(alias="canCancel")
    agency: str | None
    account: str | None
    account_digit: str | None = Field(alias="accountDigit")
    bank_account_type: str | None = Field(alias="bankAccountType")
    bank_code: str | None = Field(alias="bankCode")
    bank_name: str | None = Field(alias="bankName")
    can_change_account: bool = Field(alias="canChangeAccount")
    is_investment_note_available: bool = Field(alias="isInvestmentNoteAvailable")


class Fund(BaseModel):
    id: str
    is_fip: bool = Field(alias="isFip")
    name: str
    category_equity: int = Field(alias="categoryEquity")


class Customer(BaseModel):
    email: str
    advisor: Advisor = Field(alias="advisorId")
    cellphone: str
    name: str
    id: int

    @validator("advisor", pre=True)
    def validate_advisor_id(cls, v):
        return v[1:]


class AdvisorOrders(BaseModel):
    order: Order
    fund: Fund
    customer: Customer


class AdvisorOrdersResponse(BaseModel):
    limit: int
    offset: int
    page_count: int = Field(alias="pageCount")
    data: list[AdvisorOrders]


class AdvisorOrders(XpApiEndpoint):
    path = "/investment-funds/yield-rede/v1/advisor-orders"
    model = AdvisorOrdersResponse

    @classmethod
    def get_query_params(
        cls,
        xp_account,
        fund_id,
        start=None,
        end=None,
        limit=10_000,
        offset=1,  # offset tem que ser 1, wtf????
    ):
        start = start or date(2000, 1, 1)
        end = end or timezone.localdate()
        return {
            "customerTradingAccount": xp_account,
            "fundId": fund_id,
            "createdDateStart": start,
            "createdDateEnd": end,
            "limit": limit,
            "offset": offset,
        }
