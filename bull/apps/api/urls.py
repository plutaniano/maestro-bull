from bull.apps.api.views import (
    HubCookieViewSet,
    JWTViewSet,
    UserViewSet,
    XPAccountViewSet,
)
from django.urls import include, path
from rest_framework import routers

router = routers.DefaultRouter()
router.register("users", UserViewSet, basename="users")
router.register("xpaccounts", XPAccountViewSet, basename="xpaccounts")
router.register("token", JWTViewSet, basename="token")  # TODO: Pluralizar
router.register("hubcookies", HubCookieViewSet, basename="hubcookies")

urlpatterns = [
    path("", include(router.urls)),
]
