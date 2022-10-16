from bull.apps.xpaccount.models.positions.base import BaseManager, BaseQuerySet
from django.db import models


class AssetsWarrantyQuerySet(BaseQuerySet):
    pass


class AssetsWarrantyManager(BaseManager):
    queryset = AssetsWarrantyQuerySet

    def create_from_api(self, parent, aw):
        obj = self.create(parent=parent)

        equity = AssetsWarrantyEquity.objects.create_from_api(parent, aw["equity"])
        obj.equities.set(equity)
        fixed_income = AssetsWarrantyFixedIncome.objects.create(
            parent, aw["fixedIncomes"]
        )
        obj.fixed_incomes.set(fixed_income)
        treasure = AssetsWarrantyTreasure.objects.create(parent, aw["treasures"])
        obj.treasures.set(treasure)

        return obj


class AssetsWarranty(models.Model):
    "Ativos em garantia"

    parent = models.ForeignKey(
        to="xpaccount.Positions",
        on_delete=models.PROTECT,
        related_name="assets_warranty",
    )


class AssetsWarrantyEquityManager(models.Manager):
    def create_from_api(self, equity):
        equity = {
            "financial_bovespa": equity["financialBov"],
            "financial_bvmf": equity["financialBvmf"],
            "ticker": equity["paper"],
            "total_financial": equity["totalFinancial"],
            "unitary_price": equity["unitaryPrice"],
            "warranty_bov": equity["warrantyBov"],
            "warranty_Bvmf": equity["warrantyBvmf"],
        }
        return self.create(**equity)


class AssetsWarrantyEquity(models.Model):
    "Ações em garantia"

    parent = models.OneToOneField(
        to="xpaccount.AssetsWarranty",
        on_delete=models.PROTECT,
        related_name="equities",
    )
    financial_bovespa = models.DecimalField(
        verbose_name="Financeiro Bovespa",
        max_digits=12,
        decimal_places=2,
    )
    financial_bvmf = models.DecimalField(
        verbose_name="Financeiro BVMF",
        max_digits=12,
        decimal_places=2,
    )
    ticker = models.CharField(
        verbose_name="Ativo",
        max_length=128,
    )
    total_financial = models.DecimalField(
        verbose_name="Total Financeiro",
        max_digits=12,
        decimal_places=2,
    )
    total_quantity = models.IntegerField(
        verbose_name="Quantidade Total",
    )
    unitary_price = models.DecimalField(
        verbose_name="Preço unitário",
        max_digits=12,
        decimal_places=2,
    )
    warranty_bov = models.IntegerField(
        verbose_name="Garantia Bov",
    )
    warranty_bvmf = models.IntegerField(
        verbose_name="Garantia BVMF",
    )

    objects = AssetsWarrantyEquityManager()


class AssetsWarrantyFixedIncomeManager(models.Manager):
    def create_from_api(self, data):
        data = {
            "asset": data["asset"],
            "issuer": data["issuer"],
            "total_financial": data["totalFinancial"],
            "total_quantity": data["totalQuantity"],
        }
        return self.create(**data)


class AssetsWarrantyFixedIncome(models.Model):
    "Renda fixa em garantia"

    parent = models.ForeignKey(
        to="xpaccount.AssetsWarranty",
        on_delete=models.PROTECT,
        related_name="fixed_incomes",
    )
    asset = models.CharField(
        verbose_name="Tipo de Produto",
        max_length=128,
    )
    issuer = models.CharField(
        verbose_name="Emissor",
        max_length=128,
    )
    due_date = models.DateField(
        verbose_name="Vencimento",
    )
    total_financial = models.DecimalField(
        verbose_name="Posição",
        max_digits=12,
        decimal_places=2,
    )
    total_quantity = models.IntegerField(
        verbose_name="Quantidade em Garantia",
    )

    objects = AssetsWarrantyFixedIncomeManager()


class AssetsWarrantyTreasureManager(models.Manager):
    def create_from_api(self, data):
        data = {
            "asset": data["asset"],
            "due": data["due"],
            "last_quote": data["lastQuote"],
            "total_financial": data["totalFinancial"],
            "total_quantity": data["totalQuantity"],
        }
        return self.create(**data)


class AssetsWarrantyTreasure(models.Model):
    "Tesouro em garantia"

    parent = models.ForeignKey(
        to="xpaccount.AssetsWarranty",
        on_delete=models.PROTECT,
        related_name="treasures",
    )
    asset = models.CharField(
        verbose_name="Tipo de Produto",
        max_length=128,
    )
    due_date = models.DateField(
        verbose_name="Vencimento",
    )
    last_quote = models.DecimalField(
        verbose_name="Última cotação",
        max_digits=12,
        decimal_places=2,
    )
    total_financial = models.DecimalField(
        verbose_name="Posição",
        max_digits=12,
        decimal_places=2,
    )
    total_quantity = models.IntegerField(
        verbose_name="Quantidade em Garantia",
    )

    objects = AssetsWarrantyTreasureManager()
