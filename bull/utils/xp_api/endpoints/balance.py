from decimal import Decimal

from bull.utils.pydantic_types import Money
from bull.utils.xp_api.endpoints.base import XpApiEndpoint
from pydantic import BaseModel


class BalanceResponse(BaseModel):
    __root___: Money


class Balance(XpApiEndpoint):
    model = BalanceResponse
    # not sensitive
    subscription_key = "".join(["5ba198fffff4", "4b858a575a", "6d95fc6242"])

    @classmethod
    def get_path(cls, xp_account):
        return f"/rede-fixedIncome/v1/customers/{xp_account}/balance"

    @classmethod
    def parse_response(cls, response):
        return Decimal(response.json()).quantize(Decimal("0.00"))
