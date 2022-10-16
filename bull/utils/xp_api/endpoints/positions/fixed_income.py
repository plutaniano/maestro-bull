from django.db.models import TextChoices
from pydantic import BaseModel, Field, validator

from bull.utils.pydantic_types import Date, Money


class Interest(TextChoices):
    AT_EXPIRY = "at_expiry", "Vencimento"
    ANNUALY = "annualy", "Anual"
    BIANNUALLY = "biannualy", "Semestral"
    QUARTERLY = "quarterly", "Trimestral"
    MONTHLY = "monthly", "Mensal"


class Liquidity(TextChoices):
    NO_LIQUIDITY = "no_liquidity", "Sem Liquidez"
    DAILY = "daily", "Diária"


class Product(TextChoices):
    CDB = "cdb", "CDB"
    CRA = "cra", "CRA"
    CRI = "cri", "CRI"
    DEB = "deb", "DEB"
    FND = "fnd", "FND"
    LC = "lc", "LC"
    LCA = "lca", "LCA"
    LCI = "lci", "LCI"
    LF = "lf", "LF"
    LFSN = "lfsn", "LFSN"
    LFT = "lft", "LFT"
    LTN = "ltn", "LTN"
    NTNB = "ntn-b", "NTN-B"
    NTNF = "ntn-f", "NTN-F"


class SubGroupName(TextChoices):
    FIXED = "fixed", "Prefixada"
    POST_FIXED = "post_fixed", "Pós-fixada"
    INFLATION = "inflation", "Inflação"


class FixedIncomeSide(BaseModel):
    amount: int = Field(alias="amount")
    pu_date: Date = Field(alias="datePu")
    gross_income: Money = Field(alias="grossIncome")
    gross_value: Money = Field(alias="grossValue")
    interest: str | None = Field(alias="interest")
    iof: Money = Field(alias="iof")
    ir: Money = Field(alias="ir")
    last_deposit_at: Date = Field(alias="lastApply")
    liquid_income: Money = Field(alias="liquidIncome")
    liquid_value: Money = Field(alias="liquidValue")
    liquidity: Liquidity = Field(alias="liquidity")
    paper: str = Field(alias="paper")
    pu_price: Money = Field(alias="pricePu")
    rating: str = Field(alias="rating")

    @validator("liquidity", pre=True)
    def map_liquidity(cls, v):
        match v:
            case "Sem Liquidez":
                return Liquidity.NO_LIQUIDITY
            case "Diária":
                return Liquidity.DAILY

    @validator("interest", pre=True)
    def map_interest(cls, v):
        match v:
            case "Vencimento":
                return Interest.AT_EXPIRY
            case "Anual":
                return Interest.ANNUALY
            case "Semestral":
                return Interest.BIANNUALLY
            case "Trimestral":
                return Interest.QUARTERLY
            case "Mensal":
                return Interest.MONTHLY


class FixedIncome(BaseModel):
    asset: str = Field(alias="ativo")
    available: int = Field(alias="avaiable")  # Erro de grafia da XP
    issuer: str = Field(alias="emitter")
    lack: Date | None = Field(alias="lack")
    maturity: Date = Field(alias="maturity")
    position: Money = Field(alias="position")
    product_id: int = Field(alias="productId")
    product: Product = Field(alias="product")
    side: FixedIncomeSide = Field(alias="side")
    start: Date = Field(alias="start")
    tax: str = Field(alias="tax")
    type_code: int = Field(alias="typeCode")
    applied_value: Money = Field(alias="value")
    warranty: int = Field(alias="warranty")

    @validator("product", pre=True)
    def map_product(cls, v):
        v = v.replace("-", "")
        return Product[v]


class FixedIncomeGroup(BaseModel):
    items: list[FixedIncome]
    name: SubGroupName
    percent: float
    category_id: list[int] = Field(alias="categoriesId")

    @validator("name", pre=True)
    def map_name(cls, v):
        match v:
            case "Inflação":
                return SubGroupName.INFLATION
            case "Pós-Fixada":
                return SubGroupName.POST_FIXED
            case "Prefixada":
                return SubGroupName.FIXED


class FixedIncomeResponse(BaseModel):
    sub_groups: list[FixedIncomeGroup] = Field(alias="subGroups")
    percent: float
    value: Money
