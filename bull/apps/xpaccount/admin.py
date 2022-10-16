from bull.apps.xpaccount.models import HubCookie, XPAccount
from django.contrib import admin
from django.contrib.admin.decorators import display
from django.contrib.humanize.templatetags.humanize import intcomma


@admin.register(XPAccount)
class XPAccountAdmin(admin.ModelAdmin):
    raw_id_fields = ("positions",)
    list_display = ("id", "name", "advisor", "patrimonio")
    search_fields = ("name", "id")
    list_filter = ("advisor",)

    @display(ordering="patrimony")
    def patrimonio(self, obj):
        if not obj.patrimony:
            return "-"
        return intcomma(obj.patrimony)


@admin.register(HubCookie)
class HubCookieAdmin(admin.ModelAdmin):
    list_display = ("id", "advisor", "auth_time", "expires_at", "refused")
