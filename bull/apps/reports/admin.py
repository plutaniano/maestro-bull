from bull.apps.reports.models import Captacao, Positivador, RelatorioMensal, Revenue
from django.contrib import admin


@admin.register(Revenue)
class RevenueAdmin(admin.ModelAdmin):
    list_display = ("id", "category", "date", "amount", "xp_account", "name", "advisor")
    raw_id_fields = ("xp_account",)

    def name(self, obj):
        return obj.xp_account.name


@admin.register(Positivador)
class PositivadorAdmin(admin.ModelAdmin):
    list_display = ("id", "xp_account", "name", "sex", "advisor")
    raw_id_fields = ("xp_account",)

    def name(self, obj):
        return obj.xp_account.name


@admin.register(Captacao)
class CaptacaoAdmin(admin.ModelAdmin):
    list_display = ("id", "xp_account", "name", "advisor", "type", "amount")
    raw_id_fields = ("xp_account",)

    def name(self, obj):
        return obj.xp_account.name


@admin.register(RelatorioMensal)
class RelatorioMensalAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "date",
        "xp_account",
        "advisor",
        "comission",
        "category",
        "level_1",
    )
    raw_id_fields = ("xp_account",)
