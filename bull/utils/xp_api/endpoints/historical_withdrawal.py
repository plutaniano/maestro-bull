from datetime import datetime
from decimal import Decimal

from bull.utils.xp_api.endpoints.base import XpApiEndpoint
from django.db.models import TextChoices
from django.utils import timezone
from pydantic import BaseModel, Field


class HistoricalWithdrawalStatus(TextChoices):
    CANCELED = "Cancelado"
    RETURNED = "Devolvido"
    EXECUTED = "Efetivado"
    PENDING = "Aguardando"
    REFUSED = "Recusado"


class HistoricalWithdrawal(BaseModel):
    id: int
    status: HistoricalWithdrawalStatus
    value: Decimal
    issued_at: datetime = Field(alias="transactionDate")
    scheduled_at: datetime = Field(alias="schedulingDate")
    executed_at: datetime | None = Field(alias="executionDate")

    def is_notable(self):
        "Checa se um saque é 'notável', ou seja, se está pendente ou foi executado recentemente"
        if self.status == HistoricalWithdrawalStatus.PENDING:
            return True
        if self.executed_at is None:
            return False
        return self.executed_at.date() == timezone.localdate()


class HistoricalWithdrawalResponse(BaseModel):
    historical_withdrawal: list[HistoricalWithdrawal] = Field(
        alias="historical-withdrawal"
    )


class HistoricalWithdrawal(XpApiEndpoint):
    model = HistoricalWithdrawalResponse

    @classmethod
    def get_path(cls, xp_account):
        return f"/rede-customer/v1/customers/{xp_account}/historical-withdrawal"

    @classmethod
    def get_query_params(cls, xp_account):
        return {"xp_account": xp_account}
