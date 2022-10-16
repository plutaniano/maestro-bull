from decimal import Decimal
from django.db.models import IntegerChoices, TextChoices
from pydantic import BaseModel, Field, validator
from bull.utils.pydantic_types import Date, Money


class FlexibleOptionTypes(TextChoices):
    SWAP = "swap", "Swap"
    PUT = "put", "Put"
    CALL = "call", "Call"


class FlexibleOptionFixingTypes(TextChoices):
    LAST = "last", "Último"


class FlexibleOptionFramingCategories(IntegerChoices):
    FOUR = 4


class OptionGroupName(TextChoices):
    OTC = "otc", "Derivativos de Balcão"
    OPTION = "option", "Opções"


class OptionStyles(TextChoices):
    AMERICAN = "american", "Americana"
    EUROPEAN = "european", "Européia"


class Option(BaseModel):
    available_quantity: int = Field(alias="quantityAvaliable")  # erro de grafia XP
    day_quantity: int = Field(alias="quantityDay")
    due_date: Date = Field(alias="due")
    financial: Money = Field(alias="financial")
    quote: Money = Field(alias="currentQuote")
    series: str = Field(alias="series")
    strike_price: Money = Field(alias="price")
    total_quantity: int = Field(alias="quantityTotal")
    style: OptionStyles = Field(alias="type")
    underlying: str = Field(alias="paper")

    @validator("style", pre=True)
    def normalize_style(cls, v):
        match v:
            case 1:
                return OptionStyles.AMERICAN
            case 2:
                return OptionStyles.EUROPEAN


class FlexibleOption(BaseModel):
    asset: str = Field(alias="asset")
    current_factor: Decimal = Field(alias="currentFactor")
    xp_account_id: int = Field(alias="customerCode")
    description: str = Field(alias="assetDescription")
    expiration_code: int | None = Field(alias="expirationCode")
    expiry_date: Date = Field(alias="expiryDate")
    fixing_date: Date = Field(alias="fixingDate")
    fixing_type: FlexibleOptionFixingTypes = Field(alias="fixingType")
    framing_category: FlexibleOptionFramingCategories = Field(alias="framingCategory")
    opening_margin_max: Money = Field(alias="openingMarginMax")
    opening_unit_price: Money = Field(alias="openingUnitPrice")
    position_date: Date = Field(alias="positionDate")
    position: Money = Field(alias="position")
    settlement_date: Date = Field(alias="settlementDate")
    opening_amount: int = Field(alias="totalOpeningAmount")
    type: FlexibleOptionTypes = Field(alias="financialInstrument")
    underlying: str = Field(alias="marketIdentifierCode")

    @validator("type", pre=True)
    def normalize_type(cls, v):
        return FlexibleOptionTypes[v.upper()]

    @validator("asset", "description", pre=True)
    def none_to_empty_string(cls, v):
        return "" if v is None else v

    @validator("fixing_type", pre=True)
    def normalize_fixing_type(cls, v):
        match v:
            case 1:
                return FlexibleOptionFixingTypes.LAST


class OptionGroup(BaseModel):
    name: OptionGroupName = Field(alias="name")
    percent: float = Field(alias="percent")
    items: list[FlexibleOption | Option] = Field(alias="items")
    options: list[Option] = Field(alias="optionsDetails")
    flexible_options: list[FlexibleOption] = Field(alias="flexibleOptionsDetails")
    value: Money = Field(alias="value")

    @validator("name", pre=True)
    def normalize_name(cls, v):
        match v:
            case "Derivativos de Balcão":
                return OptionGroupName.OTC
            case "Opções":
                return OptionGroupName.OPTION


class OptionResponse(BaseModel):
    percent: float = Field(alias="percent")
    value: Money = Field(alias="percent")
    sub_groups: list[OptionGroup] = Field(alias="subGroups")
