from bull.apps.xpaccount.exceptions import ValidCookieNotAvailable
from django.conf import settings
from django.core.validators import RegexValidator
from django.db import models
from django.utils import timezone as tz


class HubCookieQuerySet(models.QuerySet):
    def valid_cookies(self):
        return self.filter(expires_at__gt=tz.now(), refused=False)

    def valid_cookie(self):
        return self.valid_cookies().order_by("?").first()

    def token(self):
        try:
            return self.valid_cookie().access_token
        except AttributeError:
            raise ValidCookieNotAvailable


class HubCookieManager(models.Manager):
    def get_queryset(self):
        return HubCookieQuerySet(self.model, using=self._db)


class HubCookie(models.Model):
    "Cookie de acesso ao Hub XP."

    advisor = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        verbose_name="Assessor",
        on_delete=models.PROTECT,
    )
    auth_time = models.DateTimeField(
        verbose_name="Autenticado em",
    )
    expires_at = models.DateTimeField(
        verbose_name="Expira em",
    )
    access_token = models.CharField(
        verbose_name="Token de acesso",
        max_length=64,
        unique=True,
        validators=[RegexValidator("^[a-z0-9]{64}$")],
    )
    refused = models.BooleanField(
        verbose_name="Recusado",
        default=False,
    )

    objects = HubCookieManager.from_queryset(HubCookieQuerySet)()

    def __str__(self):
        return self.access_token

    class Meta:
        verbose_name = "HUB Cookie"
        verbose_name_plural = "HUB Cookies"
        ordering = ["-expires_at"]

    @property
    def is_valid(self):
        "Retorna `True` se o cookie for válido, caso contrário retorna `False`."
        return (tz.now() < self.expires_at) and not self.refused
