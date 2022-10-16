import json
from datetime import date, datetime
from decimal import Decimal

from bull.utils.xp_api.endpoints.base import XpApiEndpoint
from bull.utils.xp_api.exceptions import TreasureNotEnabled, XpApiException
from django.utils import timezone
from pydantic import BaseModel, Field, validator


class Protocol(BaseModel):
    code: int
    protocol: int
    name: str
    operation: str
    status: str
    cancellable: bool
    type_cancellable: None = Field(alias="typeCancelable")
    quantity: Decimal
    value: Decimal
    pu_value: Decimal = Field(alias="puValue")
    scheduled_at: datetime = Field(alias="dateSchedule")
    effective_date: datetime | None

    @validator("quantity", pre=True)
    def quantity_validator(cls, v):
        return v.replace(",", ".")


class ProtocolResponse(BaseModel):
    __root__: list[Protocol]


class Protocol(XpApiEndpoint):
    model = ProtocolResponse

    @classmethod
    def get_path(cls, xp_account, start, end):
        return f"/rede-treasury/v1/customers/{xp_account}/orders/protocol"

    @classmethod
    def get_query_params(cls, xp_account, start=None, end=None):
        start = start or date(2000, 1, 1)
        end = end or timezone.localdate()
        return {"startDate": start, "endDate": end, "xp_account": xp_account}

    @classmethod
    def parse_response(cls, response):
        match response.status_code:
            case 200:
                return super().parse_response(response)
            case 400:
                content = json.loads(response.content)
                raise TreasureNotEnabled(content["message"])
            case _:
                raise XpApiException("Unknown error")
