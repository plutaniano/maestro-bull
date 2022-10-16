from pydantic import BaseModel, Field, validator
from django.db.models import TextChoices

from bull.utils.pydantic_types import Date, Money


class InvestmentFundSubGroup(TextChoices):
    ALTERNATIVE = "alternative", "Alternativo"
    INTERNATIONAL = "international", "Internacional"
    MULTIMARKET = "multimarket", "Multimercado"
    INFLATION = "inflation", "Inflação"
    FIXED = "pre_fixed_income", "Pré-fixado"
    POST_FIXED = "post_fixed_income", "Pós-fixado"
    VARIABLE_INCOME = "variable_income", "Renda Variável"


class InvestmentFund(BaseModel):
    uuid: str = Field(alias="id")
    type_code: int = Field(alias="typeCode")
    fund_code: int = Field(alias="fundCode")
    fund_id: int = Field(alias="fundId")
    product: str = Field(alias="product")
    quota_date: Date = Field(alias="quotaDate")
    quota_value: float = Field(alias="quotaValue")
    quota_amount: float = Field(alias="quotaAmount")
    position: Money = Field(alias="position")
    liquid_value: Money = Field(alias="liquidValue")
    quotation_value: Money = Field(alias="quotationValue")
    gross_value: Money = Field(alias="grossValue")
    gross_income: Money = Field(alias="grossIncome")
    ir: Money = Field(alias="ir")
    iof: Money = Field(alias="iof")
    liquid_income: Money = Field(alias="liquidIncome")
    withdrawal_blocked: bool = Field(alias="withdrawalBlocked")
    withdrawal_quota: str = Field(alias="withdrawalQuota")
    withdrawal_liquidation: str = Field(alias="withdrawalLiquid")
    is_processing: bool = Field(alias="isProcessing")


class InvestmentFundGroup(BaseModel):
    name: InvestmentFundSubGroup = Field(alias="name")
    percent: float = Field(alias="percent")
    category_id: list[int] = Field(alias="categoriesId")
    items: list[InvestmentFund] = Field(alias="items")

    @validator("name", pre=True)
    def normalize_name(cls, v):
        match v:
            case "Fundos Alternativos":
                return InvestmentFundSubGroup.ALTERNATIVE
            case "Fundos Internacionais":
                return InvestmentFundSubGroup.INTERNATIONAL
            case "Fundos Multimercados":
                return InvestmentFundSubGroup.MULTIMARKET
            case "Fundos de Inflação":
                return InvestmentFundSubGroup.INFLATION
            case "Fundos de Renda Fixa Pré-Fixado":
                return InvestmentFundSubGroup.FIXED
            case "Fundos de Renda Fixa Pós-Fixado":
                return InvestmentFundSubGroup.POST_FIXED
            case "Fundos de Renda Variável":
                return InvestmentFundSubGroup.VARIABLE_INCOME


class InvestmentFundResponse(BaseModel):
    percent: float = Field(alias="percent")
    value: Money = Field(alias="value")
    sub_groups: list[InvestmentFundGroup] = Field(alias="subGroups")
