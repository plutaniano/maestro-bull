from datetime import datetime

from django.db import IntegrityError
from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from pydantic import BaseModel, constr
from rest_framework.status import *
from bull.utils.pydantic_types import Advisor

from bull.apps.xpaccount.models import HubCookie


class HubCookieParams(BaseModel):
    access_token: constr(regex="^[a-f0-9]{64}$")
    advisor: Advisor
    expires_at: datetime
    auth_time: datetime


@method_decorator(csrf_exempt, name="dispatch")
class AccessTokenView(View):
    def post(self, request):
        try:
            data = HubCookieParams.parse_raw(request.body)
            HubCookie.objects.create(**data.dict())
            msg = "Cookie adicionado com sucesso"
            status = HTTP_201_CREATED

        except IntegrityError:
            msg = "Ocorreu um erro ao adicionar o cookie"
            status = HTTP_400_BAD_REQUEST

        except Exception as e:
            msg = str(e)
            status = HTTP_500_INTERNAL_SERVER_ERROR

        return HttpResponse(msg, status=status)
