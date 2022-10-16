from decimal import Decimal

from bull.utils.pydantic_types import Bool, Date, Yield
from bull.utils.xp_api.endpoints.base import XpApiEndpoint
from bull.utils.xp_api.enums import Suitability
from django.db import models
from django.utils import timezone
from pydantic import BaseModel, Field, validator


class RatingModel(BaseModel):
    title: str
    values: list[str]


class FlowType(BaseModel):
    title: str
    values: list[str]


class Product(models.TextChoices):
    CDB = "cdb", "CDB"
    LCI = "lci", "LCI"
    LCA = "lca", "LCA"


class Filter(BaseModel):
    assets: list[str] = Field(alias="assets")
    indexers: list[str] = Field(alias="indexers")
    minimum_value_for_application: list[int] = Field(alias="minimumValueForApplication")
    liquid_daily: bool = Field(alias="liquidDaily")
    incentivised: list[str] = Field(alias="incentivada")
    ratings: list[RatingModel] = Field(alias="ratings")
    flow_types: list[FlowType] = Field(alias="flowTypes")
    grace_day: list[int] = Field(alias="graceDay")


class Eligibility(BaseModel):
    code: int
    eligibility_type: int = Field(alias="eligibilityType")


class Liquidity(models.TextChoices):
    DAILY = "daily", "Diária"
    AT_EXPIRY = "at_expiry", "No Vencimento"


class Amortization(models.TextChoices):
    EXPIRY = "expiry", "Vencimento"


class Indexer(models.TextChoices):
    INFLATION = "inflation", "Inflação"
    FIXED = "fixed", "Pré-fixado"
    POST_FIXED = "post_fixed", "Pós-fixado"


class Agency(models.TextChoices):
    FITCH = "fitch", "Fitch"
    MOODYS = "moodys", "Moody's"
    SP = "sp", "S&P"


class Rating(models.TextChoices):
    AAA = "aaa"
    AA_PLUS = "aa+", "AA+"
    AA = "aa", "AA"
    AA_MINUS = "aa-"
    A_PLUS = "a+", "A+"
    A = "a", "A"
    A_MINUS = "a-", "A-"
    BBB_PLUS = "bbb+", "BBB+"
    BBB = "bbb", "BBB"
    BBB_MINUS = "bbb-", "BBB-"
    BB_PLUS = "bb+", "BB+"
    BB = "bb", "BB"
    B = "b", "B"
    CCC = "ccc", "CCC"
    CC = "cc", "CC"
    C = "c", "C"
    D = "d", "D"


class InterestPayments(models.TextChoices):
    MONTHLY = "monthly", "Mensal"
    AT_EXPIRY = "at_expiry", "Vencimento"


class Asset(BaseModel):
    agency: Agency | None = Field(alias="agencyName")
    amortization: Amortization | None = Field(alias="amortization")
    asset_id: str = Field(alias="assetId")  # Inútil, sempre o mesmo id
    comission: float = Field(alias="comission")
    continued_offering: Bool = Field(alias="continuedOffering")
    description_comission: Yield = Field(alias="descriptionComission")
    description_term: None = Field(alias="descriptionTerm")
    edspu_code: int = Field(alias="edspuCode")
    # eligibility_list: list[Eligibility] = Field(alias="eligibilitylist")
    # end_trading_hours: time = Field(alias="endTradingHours")
    fee_max: Yield = Field(alias="feeMax")
    fee_min: Yield = Field(alias="feeMin")
    grace_days: int = Field(alias="graceDays")
    # inactive_date: None = Field(alias="inactiveDate")
    is_incentivised: Bool = Field(alias="incentive")
    indexer: Indexer = Field(alias="indexers")
    interest_payments: InterestPayments | None = Field(alias="interestRates")
    liquidity: Liquidity | None = Field(alias="liquidType")
    maturity_date: Date = Field(alias="maturityDate")
    max_quantity_for_application: int = Field(alias="maximumQuantityForApplication")
    min_quantity_for_application: int = Field(alias="minimumQuantityForApplication")
    title: str | None = Field(alias="nickName")
    # origin_code: int = Field(alias="originCode")
    plataform_id: int = Field(alias="plataformId")
    pre_registration: Bool = Field(alias="preRegistration")
    product: Product = Field(alias="product")
    pu: float = Field(alias="puMinValue")
    qualified_investor: Bool = Field(alias="qualifiedInvestor")
    available_quantity: int = Field(alias="quantityAvailable")
    rating: Rating | None = Field(alias="ratingName")
    risk_score: int | None = Field(alias="riskScore")
    scheduler_date: Date = Field(
        alias="schedulerDate"
    )  # Inútil, é sempre igual a 0001-01-01T00:00:00
    # scheduling: Bool = Field(alias="scheduling")
    # start_trading_hours: time = Field(alias="startTradingHours")
    suitability: Suitability = Field(alias="suitability")
    ticker: str = Field(alias="ticker")

    @validator("indexer", pre=True)
    def map_indexer(cls, v):
        match v:
            case "Pré-fixado":
                return Indexer.FIXED
            case "Pós-fixado":
                return Indexer.POST_FIXED
            case "Inflação":
                return Indexer.INFLATION

    @validator("suitability", pre=True)
    def map_suitability(cls, v):
        match v:
            case "Conservador":
                return Suitability.CONSERVATIVE
            case "Moderado":
                return Suitability.MODERATE
            case "Agressivo":
                return Suitability.AGGRESSIVE

    @validator("liquidity", pre=True)
    def map_liquid_type(cls, v):
        match v:
            case "Diária":
                return Liquidity.DAILY
            case "No Vencimento":
                return Liquidity.AT_EXPIRY

    @validator("interest_payments", pre=True)
    def map_interest_rates(cls, v):
        match v:
            case "Vencimento":
                return InterestPayments.AT_EXPIRY
            case "Mensal":
                return InterestPayments.MONTHLY

    @validator("amortization", pre=True)
    def map_amortization(cls, v):
        match v:
            case "Vencimento":
                return Amortization.EXPIRY

    @validator("agency", pre=True)
    def map_agency(cls, v):
        match v:
            case "Fitch":
                return Agency.FITCH
            case "Moody´s":
                return Agency.MOODYS
            case "S&P":
                return Agency.SP

    @validator("product", pre=True)
    def map_product(cls, v):
        match v:
            case "CDB":
                return Product.CDB
            case "LCI":
                return Product.LCI
            case "LCA":
                return Product.LCA

    @validator("rating", pre=True)
    def map_rating(cls, v):
        v = str(v).replace(".", "").replace("br", "")
        match v:
            case "AAA":
                return Rating.AAA
            case "AA+":
                return Rating.AA_PLUS
            case "AA":
                return Rating.AA
            case "AA-":
                return Rating.AA_MINUS
            case "A+":
                return Rating.A_PLUS
            case "A":
                return Rating.A
            case "A-":
                return Rating.A_MINUS
            case "BBB+":
                return Rating.BBB_PLUS
            case "BBB":
                return Rating.BBB
            case "BBB-":
                return Rating.BBB_MINUS
            case "BB+":
                return Rating.BB_PLUS
            case "BB":
                return Rating.BB
            case "B":
                return Rating.B
            case "CCC":
                return Rating.CCC
            case "CC":
                return Rating.CC
            case "C":
                return Rating.C
            case "D":
                return Rating.D

    @validator("comission")
    def map_comission(cls, v):
        return v / 2

    def tax(self):
        days = (self.maturity_date - timezone.localdate()).days
        if days < 180:
            return 0.225
        if days < 360:
            return 0.2
        if days < 720:
            return 0.175
        return 0.15

    def gross_fee(self, adjustment=None):
        fee = self.fee_min
        if self.is_incentivised:
            match self.indexer:
                case Indexer.POST_FIXED | Indexer.FIXED:
                    fee /= 1 - self.tax()
                case Indexer.INFLATION:
                    fee += float(adjustment)
        return Decimal(fee).quantize(Decimal("0.00"))

    def liquid_fee(self, adjustment=None):
        fee = self.fee_min
        if not self.is_incentivised:
            match self.indexer:
                case Indexer.POST_FIXED | Indexer.FIXED:
                    fee *= 1 - self.tax()
                case Indexer.INFLATION:
                    fee -= float(adjustment)
        return Decimal(fee).quantize(Decimal("0.00"))

    def short_dict(self, adjustment=None):
        return {
            "indexer": self.indexer.label,
            "year": self.maturity_date.year,
            "title": self.title,
            "gross_fee": self.gross_fee(adjustment),
            "liquid_fee": self.liquid_fee(adjustment),
            "comission": self.comission,
        }


class AvailableAssetsResponse(BaseModel):
    data: list[Asset]
    filter: Filter

    def get(self, edspu_code):
        for asset in self.data:
            if asset.edspu_code == edspu_code:
                return asset
        raise ValueError("Could not find edspu code")

    def best_fee(self, indexer, year):
        try:
            assets = [
                asset
                for asset in self.data
                if asset.maturity_date.year == year and asset.indexer == indexer
            ]
            return max(assets, key=lambda i: (i.liquid_fee(0), i.comission))
        except ValueError:
            return None

    def best_comission(self, indexer, year):
        try:
            assets = [
                asset
                for asset in self.data
                if asset.maturity_date.year == year
                and asset.indexer == indexer
                and asset.liquidity != Liquidity.DAILY
            ]
            return max(assets, key=lambda i: (i.comission, i.liquid_fee(0)))
        except ValueError:
            return None


class AvailableAssets(XpApiEndpoint):
    model = AvailableAssetsResponse
    path = "/rede-fixedIncome/v1/available-assets"
    # not sensitive
    subscription_key = "".join(["5ba198fff", "ff44b858a", "575a6d95fc6242"])

    @classmethod
    def get_query_params(cls, category="BANCARIO"):
        return {
            "category": category,
            "brand": "XP",
            # "customerCode": None,
            # "nickNameOrTicker": "",
        }

    @classmethod
    def best_fees(cls):
        response = cls.get()
        years = sorted(set(i.maturity_date.year for i in response.data))
        fixeds, post_fixeds, inflations = [], [], []
        for year in years:
            post_fixed = response.best_fee(Indexer.POST_FIXED, year)
            fixed = response.best_fee(Indexer.FIXED, year)
            inflation = response.best_fee(Indexer.INFLATION, year)

            if post_fixed:
                post_fixeds.append(post_fixed.short_dict())

            if fixed:
                fixeds.append(fixed.short_dict())

            if inflation and fixed:
                adjustment = fixed.gross_fee() - fixed.liquid_fee()
                inflations.append(inflation.short_dict(adjustment))

        return post_fixeds, fixeds, inflations

    @classmethod
    def best_comissions(cls):
        response = cls.get()
        years = sorted(set(i.maturity_date.year for i in response.data))
        fixeds, post_fixeds, inflations = [], [], []
        for year in years:
            post_fixed = response.best_comission(Indexer.POST_FIXED, year)
            fixed = response.best_comission(Indexer.FIXED, year)
            inflation = response.best_comission(Indexer.INFLATION, year)

            if fixed:
                fixeds.append(fixed.short_dict())

            if post_fixed:
                post_fixeds.append(post_fixed.short_dict())

            if inflation:
                adjustment = fixed.gross_fee() - fixed.liquid_fee()
                inflations.append(inflation.short_dict(adjustment))

        return post_fixeds, fixeds, inflations
