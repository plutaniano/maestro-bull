from django.urls import path
from bull.apps.xpaccount.views import AccessTokenView

urlpatterns = [
    path("access_token", AccessTokenView.as_view(), name="access_token"),
]
