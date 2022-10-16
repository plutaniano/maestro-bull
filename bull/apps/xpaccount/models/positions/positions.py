from django.db import models
from django.db.models import Q, F, Value
from django.db.models.functions import Concat
from django.db.models.constraints import UniqueConstraint

from bull.utils import xp_api


class PositionsQuerySet(models.QuerySet):
    def fresh(self):
        return self.filter(fresh=True)

    def to_excel(self, wb):
        ws = wb.create_sheet("Por tipo de ativo")

        fields = {
            "equity": "Ações",
            "coe": "COE",
            "gold": "Ouro",
            "term": "Termos",
            # 'future': 'Futuro',
            "option": "Opções",
            "rental": "Aluguel",
            "treasure": "Tesouro",
            "realEstate": "FII",
            "fixedIncome": "Renda Fixa",
            "investmentFund": "Fundos",
            "privatePension": "Previdência",
            "structuredProduct": "Estruturados",
        }
        qs = self.annotate(
            client_name=F("xp_account__name"),
            advisor_id=F("xp_account__advisor__advisor_id"),
            advisor_name=Concat(
                F("xp_account__advisor__first_name"),
                Value(" "),
                F("xp_account__advisor__last_name"),
            ),
            **{f + "_value": F(f"raw_json__{f}__value") for f in fields},
            **{f + "_percent": F(f"raw_json__{f}__percent") for f in fields},
        )

        ws.append(
            ["Conta XP", "Cliente", "Código A", "Assessor"]
            + [f"{f} ({i})" for f in fields.values() for i in ("R$", "%")]
        )

        for row, position in enumerate(qs, start=2):
            ws.cell(row, 1).value = position.xp_account_id
            ws.cell(row, 2).value = position.client_name
            ws.cell(row, 3).value = position.advisor_id
            ws.cell(row, 4).value = position.advisor_name
            for col, field in enumerate(fields):
                ws.cell(row, 5 + col * 2).value = getattr(position, field + "_value")
                ws.cell(row, 6 + col * 2).value = getattr(position, field + "_percent")


class PositionsManager(models.Manager):
    def get_queryset(self):
        return PositionsQuerySet(self.model, using=self._db)

    def create_default(self):
        self.create()

    def new(cls, xp_account):
        # TODO: Arrumar esses imports horríveis
        # não sei se tem como evitar essa circular dependency
        from . import (
            Balance,
            Coe,
            Earning,
            Equity,
            FixedIncome,
            Future,
            Gold,
            Insurance,
            InvestmentFund,
            Option,
            OTCOption,
            PrivatePension,
            RealEstate,
            Rental,
            RewardedAsset,
            StructuredProduct,
            Term,
            Treasure,
        )

        model = xp_api.positions.get(xp_account)
        obj = cls.create(
            xp_account_id=xp_account,
            **{
                field.name: getattr(model, field.name)
                for field in cls.model._meta.get_fields()
                if field.name in model.__fields__ and not field.remote_field
            },
        )

        Balance.objects.create_from_model(obj, model.balance)
        Coe.objects.create_from_model(obj, model.coe)
        Earning.objects.create_from_model(obj, model.earning)
        Equity.objects.create_from_model(obj, model.equity)
        RewardedAsset.objects.create_from_model(obj, model.equity.rewarded_asset)
        FixedIncome.objects.create_from_model(obj, model.fixed_income)
        Future.objects.create_from_model(obj, model.future)
        Gold.objects.create_from_model(obj, model.gold)
        Insurance.objects.create_from_model(obj, model.insurance)
        InvestmentFund.objects.create_from_model(obj, model.investment_fund)
        Option.objects.create_from_model(obj, model.option)
        OTCOption.objects.create_from_model(obj, model.option)
        PrivatePension.objects.create_from_model(obj, model.private_pension)
        RealEstate.objects.create_from_model(obj, model.real_estate)
        Rental.objects.create_from_model(obj, model.rental)
        StructuredProduct.objects.create_from_model(obj, model.structured_product)
        Term.objects.create_from_model(obj, model.term)
        Treasure.objects.create_from_model(obj, model.treasure)
        return obj


class Positions(models.Model):
    amount = models.FloatField(
        verbose_name="Aplicações na XP",
    )
    financial_investments = models.DecimalField(
        verbose_name="financialInvestments",
        help_text="Não é usado no frontend da XP",
        max_digits=20,
        decimal_places=2,
    )
    margin_account = models.DecimalField(
        verbose_name="marginAccount",
        help_text="Não é usado no frontend da XP",
        max_digits=12,
        decimal_places=2,
    )
    patrimony = models.DecimalField(
        verbose_name="Patrimônio XP",
        max_digits=12,
        decimal_places=2,
    )
    declared_patrimony = models.DecimalField(
        verbose_name="Patrimônio Líquido Declarado",
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
    )
    updated_at = models.DateTimeField(
        verbose_name="Atualizado em",
    )

    # Campos adicionais
    fresh = models.BooleanField(
        verbose_name="Positions mais atualizada",
        default=False,
    )
    xp_account = models.ForeignKey(
        to="xpaccount.XPAccount",
        on_delete=models.PROTECT,
        verbose_name="Conta XP",
        related_name="positions_history",
    )
    queried_at = models.DateTimeField(
        verbose_name="Query na API feita em",
        auto_now_add=True,
    )
    raw_json = models.JSONField(
        verbose_name="JSON cru da API da XP",
    )

    objects = PositionsManager.from_queryset(PositionsQuerySet)()

    class Meta:
        constraints = [
            UniqueConstraint(
                fields=["xp_account"],
                condition=Q(fresh=True),
                name="one_fresh_positions_per_xpaccount",
            ),
        ]

    def save(self, *args, **kwargs):
        qs = self.__class__.objects.filter(xp_account_id=self.xp_account_id)
        qs.update(fresh=False)
        self.fresh = True
        super().save(*args, **kwargs)
