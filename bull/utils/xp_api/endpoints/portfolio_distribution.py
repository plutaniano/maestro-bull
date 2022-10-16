from typing import Any

from django.db import models
from pydantic import BaseModel, Field, color, validator

from bull.utils.xp_api.endpoints.base import XpApiEndpoint


class Category(models.TextChoices):
    COE = "coe", "COE"
    EARNING = "earning", "Proventos"
    EQUITY = "equity", "Ações"
    FIXED_INCOME = "fixed_income", "Renda Fixa"
    FIXED_INCOME_GUARANTEE = "fixed_income_guarantee", "Garantia Renda Fixa"
    FUND = "fund", "Fundos de Investimento"
    GOLD = "gold", "Ouro"
    GUARANTEE = "guarantee", "Garantia"
    INSURANCE = "insurance", "Seguros"
    OPTION = "option", "Opções"
    PRIVATE_PENSION = "private_pension", "Previdência"
    REAL_ESTATE = "real_estate", "Fundos Imobiliários"
    REAL_ESTATE_EARNING = "real_estate_earning", "Proventos de FII"
    STRUCTURED_PRODUCT = "structured_product", "Produtos Estruturados"
    TREASURE = "treasure", "Tesouro Direto"


class PortfolioCategory(BaseModel):
    color: color.Color
    category: Category = Field(alias="name")
    percent: float = Field(alias="y")

    @validator("category", pre=True)
    def map_category(cls, v):
        match v:
            case "Ações":
                return Category.EQUITY
            case "COE":
                return Category.COE
            case "Fundos Imobiliários":
                return Category.REAL_ESTATE
            case "Fundos de Investimento":
                return Category.FUND
            case "Garantia":
                return Category.GUARANTEE
            case "Opções":
                return Category.OPTION
            case "Ouro":
                return Category.GOLD
            case "Previdência":
                return Category.PRIVATE_PENSION
            case "Produtos Estruturados":
                return Category.STRUCTURED_PRODUCT
            case "Proventos":
                return Category.EARNING
            case "Proventos de Fii":
                return Category.REAL_ESTATE_EARNING
            case "Renda Fixa Garantia":
                return Category.FIXED_INCOME_GUARANTEE
            case "Renda fixa":
                return Category.FIXED_INCOME
            case "Seguros":
                return Category.INSURANCE
            case "Tesouro Direto":
                return Category.TREASURE


class PortfolioDistributionResponse(BaseModel):
    id: str
    exception: Any
    success: bool
    message: Any
    output: list[PortfolioCategory]


class PortfolioDistribution(XpApiEndpoint):
    path = "/advisor-dash/api/v1/portfolio-distribution"
    model = PortfolioDistributionResponse

    @classmethod
    def get_query_params(cls, advisor):
        return {"displayAsAdvisor": f"A{advisor}"}
