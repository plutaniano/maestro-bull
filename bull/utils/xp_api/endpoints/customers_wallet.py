from datetime import datetime

from pydantic import BaseModel, EmailStr, Field, validator
from bull.utils.enums import State
from bull.utils.pydantic_types import CNPJ, CPF, Advisor, Date, Force, Money, Phone
from bull.utils.xp_api.endpoints.base import XpApiEndpoint
from bull.utils.xp_api.enums import Suitability, InvestorQualification


class Customer(BaseModel):
    # id: str = Field(alias='id') # id inútil que a XP envia
    xp_updated_at: datetime = Field(alias="dtInsert")
    advisor: Advisor = Field(alias="advisorId")
    id: int = Field(alias="xpAccount")  # Número da Conta XP
    cpf: CPF | Force("") = Field(alias="socialSecurity")
    cnpj: CNPJ | Force("") = Field(alias="socialSecurity")
    name: str = Field(alias="name")
    cellphone: Phone | Force("") = Field(alias="cellphone")
    phone: Phone | Force("") = Field(alias="phone")
    email: EmailStr | Force("") = Field(alias="email")
    income: Money = Field(alias="income")
    occupation: str = Field(alias="occupation")
    state: State = Field(alias="state")
    suitability: Suitability = Field(alias="suitability")
    investor_qualification: InvestorQualification = Field(alias="investorQualification")
    # treasury_bond: list[str] = Field(alias="treasuryBond") # Inútil
    # certificate_deposit: list[str] = Field(alias="certificateDeposit") # Inútil
    # corporate_bond: list[str] = Field(alias="corporateBond")  # Inútil
    # alternative: list[str] # Inútil
    # fund: list[str] # Inútil
    # equities: list[str] # Inútil
    # future: list[str] # Inútil
    amount: Money = Field(alias="amount")
    patrimony: Money = Field(alias="patrimony")
    birth_date: Date = Field(alias="birthDate")
    # birth_date_day: int = Field(alias="birthDateDay") # Inútil
    # birth_date_month: int = Field(alias="birthDateMonth") # Inútil
    suitability_due: Date | None = Field(alias="dueDateSuitability")

    @validator("name")
    def validate_name(cls, v):
        return v.title().replace("Ltda", "LTDA").replace("Eireli", "EIRELI")

    @validator("email")
    def validate_email(cls, v):
        return v.lower()

    @validator("state", pre=True)
    def validate_state(cls, v):
        return v.lower()

    @validator("investor_qualification", pre=True)
    def validate_investor_qualification(cls, v):
        match v:
            case "qualify":
                return InvestorQualification.QUALIFIED
            case "regular":
                return InvestorQualification.REGULAR
            case "professional":
                return InvestorQualification.PROFESSIONAL
        raise ValueError(f"{v} is not a valid InvestorQualification value")

    @validator("suitability", pre=True)
    def validate_suitability(cls, v):
        match v:
            case "d":
                return Suitability.OUT_OF_DATE
            case "a":
                return Suitability.AGGRESSIVE
            case "m":
                return Suitability.MODERATE
            case "c":
                return Suitability.CONSERVATIVE
            case "n":
                return Suitability.NOT_FILLED
        raise ValueError(f"{v} is not a valid Suitability value")


class CustomersWalletResponse(BaseModel):
    customers_wallet: list[Customer] = Field(alias="customersWallet")


class CustomersWallet(XpApiEndpoint):
    path = "/rede-advisors/v1/advisors/customer-wallets"
    model = CustomersWalletResponse

    @classmethod
    def get_query_params(cls, limit=1000, offset=0):
        return {
            "limit": limit,
            "offset": offset,
        }

    @classmethod
    def get_all(cls, step=1000):
        offset = 0
        customers = []
        while True:
            output = cls.get(step, offset)
            if output.customers_wallet:
                customers += output.customers_wallet
                offset += step
            else:
                break
        return customers
