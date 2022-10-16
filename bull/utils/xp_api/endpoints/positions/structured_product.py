from django.db.models import TextChoices
from pydantic import BaseModel, Field, validator
from bull.utils.pydantic_types import Date, Money


class StructuredProductStatus(TextChoices):
    ACTIVE = "active", "Ativa"
    OUT_OF_SPEC = "out_of_spec", "Desenquadrada"


class StructuredProductFixingTypes(TextChoices):
    CLOSING = "closing", "Fechamento"


class StructuredProductOptionTypes(TextChoices):
    CALL = "call", "Call"
    PUT = "put", "Put"
    SPOT = "spot", "Spot"


class Leg(BaseModel):
    asset: str = Field(alias="ativo")
    contracted_quantity_position: int = Field(alias="quantidadeContratadaPosicao")
    contracted_quantity: int = Field(alias="quantidade")
    description: str = Field(alias="descricao")
    end_date: Date | None = Field(alias="dataEncerramento")
    financial: Money = Field(alias="financeiro")
    fixing_date: Date | None = Field(alias="dataFixing")
    fixing_type: StructuredProductFixingTypes | None = Field(
        alias="tipoFixingDescription"
    )
    liquidation_date: Date | None = Field(alias="dataLiquidacao")
    option_type: StructuredProductOptionTypes = Field(alias="tipoOpcaoDescription")
    position_quantity: int = Field(alias="quantidadePosicao")
    strike: Money | None = Field(alias="preco")
    quantity: int = Field(alias="quantidade")
    status: StructuredProductStatus = Field(alias="status")

    @validator("description", pre=True)
    def normalize_description(cls, v):
        return v.replace("--", "")

    @validator("option_type", pre=True)
    def normalize_option_type(cls, v):
        return StructuredProductOptionTypes[v.upper()]

    @validator("status", pre=True)
    def normalize_status(cls, v):
        match v:
            case "Ativa":
                return StructuredProductStatus.ACTIVE
            case "Desenquadrada":
                return StructuredProductStatus.OUT_OF_SPEC

    @validator("fixing_type", pre=True)
    def normalize_fixing_type(cls, v):
        match v:
            case "--":
                return None
            case "Fechamento":
                return StructuredProductFixingTypes.CLOSING


class StructuredProduct(BaseModel):
    name: str = Field(alias="nomeEstrutura")
    cost: Money = Field(alias="custo")
    end_date: Date = Field(alias="dataEncerramento")
    legs: list[Leg] = Field(alias="legs")
    percent: float = Field(alias="percent")


class StructuredProductResponse(BaseModel):
    details: list[StructuredProduct] = Field(alias="details")
    percent: float = Field(alias="percent")
    percent_detail: float = Field(alias="percentDetail")
    value: Money = Field(alias="value")
