from datetime import date
from decimal import Decimal

from bull.apps.user.models import User
from bull.utils.xp_api.endpoints.base import XpApiEndpoint
from dateutil.parser import parse
from pydantic import BaseModel, Field, validator


class CashFlow(BaseModel):
    date: date
    inbound: Decimal
    outbound: Decimal
    delta: Decimal = Field(alias="net")
    xp_account_id: int = Field(alias="customerCode")
    name: str
    outbound_requested_by: None = Field(alias="outboundRequestedBy")

    @validator("date", pre=True)
    def validate_date(cls, v):
        return parse(v)


class Summary(BaseModel):
    inbound: Decimal
    outbound: Decimal
    net: Decimal


class RootCashFlow(BaseModel):
    id: str
    summary: Summary
    historical_data: list[CashFlow] = Field(alias="historicalData")


class CashFlowResponse(BaseModel):
    cash_flow: RootCashFlow = Field(alias="cashFlow")


class CashFlow(XpApiEndpoint):
    path = "/rede-advisors/v1/advisors/financial-transaction/cash-flow"
    model = CashFlowResponse

    @classmethod
    def get_query_params(cls, start, end, advisors=None, limit=1_000_000, offset=0):
        advisors = advisors or User.objects.advisors()
        comma_list = ",".join(f"A{i.advisor_id}" for i in advisors)
        return {
            "start": start,
            "end": end,
            "advisors": comma_list,
            "limit": limit,
            "offset": offset,
        }
