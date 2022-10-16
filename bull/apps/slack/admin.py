from django.contrib import admin
from bull.apps.slack.models import SlackUser


@admin.register(SlackUser)
class SlackUserAdmin(admin.ModelAdmin):
    pass
