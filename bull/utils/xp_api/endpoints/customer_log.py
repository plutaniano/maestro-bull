from bull.apps.xpaccount.models import XPAccount
from bull.utils.pydantic_types import Date
from bull.utils.xp_api.endpoints.base import XpApiEndpoint
from pydantic import BaseModel, Field


class Log(BaseModel):
    name: str = Field(alias="clienteName")
    date: Date = Field(alias="dateStatus")
    observation: str | None = Field(alias="observation")
    responsable: None = Field(alias="responsable")
    sequence_code: int = Field(alias="sequenceCode")
    status_code: int = Field(alias="statusCode")
    status_description: str = Field(alias="statusDescription")


class Result(BaseModel):
    result: list[Log]


class CustomerLogResponse(BaseModel):
    data: Result
    success: bool
    error: None


class CustomerLog(XpApiEndpoint):
    model = CustomerLogResponse
    # not sensitive
    subscription_key = "".join(["aaa32b63cff", "04fc2aa6c", "4324fcd06583"])

    @classmethod
    def get_path(cls, xp_account):
        xp_account = XPAccount.objects.get(pk=xp_account)
        return f"/onboarding-rede-customers/api/v1/rede/customer/log/document/{xp_account.cpf or xp_account.cnpj}"

    @classmethod
    def get(cls, *args, **kwargs):
        response = super().get(*args, **kwargs)
        return response.data.result
