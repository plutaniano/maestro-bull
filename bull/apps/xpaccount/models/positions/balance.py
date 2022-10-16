from django.db import models
from bull.apps.xpaccount.models.positions.base import BaseQuerySet


class BalanceQuerySet(BaseQuerySet):
    excel_sheet_name = "Saldo"


class BalanceManager(models.Manager):
    def create_from_model(self, parent, model):
        return self.create(parent=parent, **model.dict())


class Balance(models.Model):
    "Saldo projetado"

    parent = models.OneToOneField(
        to="xpaccount.Positions",
        on_delete=models.CASCADE,
        related_name="balance",
    )
    percent = models.FloatField(
        verbose_name="Porcento da carteira em saldo",
    )
    available_balance = models.DecimalField(
        verbose_name="Saldo Disponível",
        max_digits=12,
        decimal_places=2,
    )
    warranty = models.DecimalField(
        verbose_name="Garantia",
        max_digits=12,
        decimal_places=2,
    )
    pending_withdrawal_funds = models.DecimalField(
        verbose_name="Resgate de Fundo Pendente",
        max_digits=12,
        decimal_places=2,
    )
    pending_withdrawal_clubs = models.DecimalField(
        verbose_name="Resgate de Clube Pendente",
        max_digits=12,
        decimal_places=2,
    )
    expiring_terms = models.DecimalField(
        verbose_name="Termos a Vencer",
        max_digits=12,
        decimal_places=2,
    )
    margin_account = models.DecimalField(
        verbose_name="Utilização de Conta Margem",
        max_digits=12,
        decimal_places=2,
    )
    future_releases = models.DecimalField(
        verbose_name="Lançamentos Futuros",
        max_digits=12,
        decimal_places=2,
    )
    projected_balance_1 = models.DecimalField(
        verbose_name="Saldo em D+1",
        max_digits=12,
        decimal_places=2,
    )
    projected_balance_1_date = models.DateField(verbose_name="Data D+1")
    projected_balance_2 = models.DecimalField(
        verbose_name="Saldo em D+2",
        max_digits=12,
        decimal_places=2,
    )
    projected_balance_2_date = models.DateField(verbose_name="Data D+2")
    projected_balance_3 = models.DecimalField(
        verbose_name="Saldo em D+3",
        max_digits=12,
        decimal_places=2,
    )
    projected_balance_3_date = models.DateField(verbose_name="Data D+3")
    projected_balance_over = models.DecimalField(
        verbose_name="Saldo em D>3",
        max_digits=12,
        decimal_places=2,
    )
    total_projected_balance = models.DecimalField(
        verbose_name="Saldo Total Projetado",
        max_digits=12,
        decimal_places=2,
    )
    warranty_bmf = models.DecimalField(
        verbose_name="Garantia BM&F",
        max_digits=12,
        decimal_places=2,
    )
    warranty_bovespa = models.DecimalField(
        verbose_name="Garantia Bovespa",
        max_digits=12,
        decimal_places=2,
    )
    withdraw_balance = models.DecimalField(
        verbose_name="Disponível para saque",
        max_digits=12,
        decimal_places=2,
    )

    objects = BalanceManager.from_queryset(BalanceQuerySet)()
