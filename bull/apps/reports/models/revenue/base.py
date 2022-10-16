from decimal import Decimal

from django.db import models
from django.conf import settings
from django.db.models import Q, Sum
from django.db.models.functions import Coalesce
from django.utils import timezone


class RevenueCategories(models.TextChoices):
    "Todas as categorias de receita"
    COE = "coe", "COE"
    CREDIT = "credit", "Crédito"
    EQUITY = "equity", "Renda Variável"
    REAL_ESTATE = "real_estate", "Fundos de Investimento Imobiliário"
    FIXED_INCOME = "fixed_income", "Renda Fixa"
    FOREX = "forex", "Câmbio"
    FUND = "fund", "Fundos de Investimento"
    INSURANCE = "insurance", "Seguros"
    PRIVATE_PENSION = "private_pension", "Previdência"
    OTHER = "other", "Outros"


class RevenueQuerySet(models.QuerySet):
    def month(self, date=None):
        date = date or timezone.localdate()
        return self.filter(date__month=date.month, date__year=date.year)

    def latest_month(self):
        try:
            date = self.latest().date
            return self.filter(date__year=date.year, date__month=date.month)
        except self.model.DoesNotExist:
            return self.none()

    def per_category(self):
        aggregators = {
            category: Coalesce(
                Sum("amount", filter=Q(category=category)),
                Decimal("0.00"),
            )
            for category, _ in self.model._meta.get_field("category").choices
        } | {
            "total": Coalesce(Sum("amount"), Decimal("0.00")),
        }
        return self.aggregate(**aggregators)


class RevenueManager(models.Manager):
    pass


class Revenue(models.Model):
    category = models.CharField(
        verbose_name="Categoria",
        max_length=32,
        choices=RevenueCategories.choices,
        null=False,
    )
    date = models.DateField(
        verbose_name="Data",
    )
    amount = models.DecimalField(
        verbose_name="Quantidade",
        max_digits=12,
        decimal_places=2,
    )
    xp_account = models.ForeignKey(
        to="xpaccount.XPAccount",
        on_delete=models.PROTECT,
        verbose_name="Conta XP",
        related_name="revenue_set",
        null=True,
        blank=True,
    )
    advisor = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name="Assessor",
        related_name="revenue_set",
        null=True,
        blank=True,
    )

    objects = RevenueManager.from_queryset(RevenueQuerySet)()

    class Meta:
        verbose_name = "Receita"
        verbose_name_plural = "Receitas"
        get_latest_by = "date"
