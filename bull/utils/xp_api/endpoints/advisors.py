from bull.utils.pydantic_types import Advisor
from bull.utils.xp_api.endpoints.base import XpApiEndpoint
from pydantic import BaseModel, Field


class Advisors(BaseModel):
    id: int
    code: str
    name: str
    email: str
    thumbnail: str
    ip: None
    document: int
    office_code: int = Field(alias="officeCode")
    office_name: str = Field(alias="officeName")
    office_manager: Advisor = Field(alias="officeManager")
    office_is_private: bool = Field(alias="officeIsPrivate")
    login: str
    regional: str
    advisor_type: str = Field(alias="advisorType")
    business_type: str = Field(alias="businessType")
    brand_id: int = Field(alias="brandId")
    brand: str
    profiles: list[str]
    mirrored_advisors: list[Advisor] = Field(alias="mirroredAdvisors")


class AdvisorsResponse(BaseModel):
    advisor: Advisors


class Advisors(XpApiEndpoint):
    path = "/rede-advisors/v1/advisors/"
    model = AdvisorsResponse

    @classmethod
    def parse_response(cls, response):
        json = response.json()
        json["advisor"]["mirroredAdvisors"].remove("A8387")  # esse advisor não existe
        return cls.model.parse_obj(json)
