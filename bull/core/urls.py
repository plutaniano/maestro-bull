from django.contrib import admin
from django.urls import include, path


urlpatterns = [
    path("admin/", admin.site.urls),
    path("slack/", include("bull.apps.slack.urls")),
    path("xpaccount/", include("bull.apps.xpaccount.urls")),
    path("", include("bull.apps.api.urls")),
]
