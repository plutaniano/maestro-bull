import requests
from django.conf import settings
from pydantic import BaseModel


class XpApiEndpoint:
    host = "api.xpi.com.br"
    path = ""
    model = BaseModel
    # not sensitive
    subscription_key = "".join(["b63f9758", "680845afb25d", "bd47a5e95c4a"])

    @classmethod
    def get(cls, *args, raw=False, **kwargs):
        query_params = cls.get_query_params(*args, **kwargs)
        headers = cls.get_headers(*args, **kwargs)
        path = cls.get_path(*args, **kwargs)
        response = requests.get(
            url=f"https://{cls.host}{path}",
            params=query_params,
            headers=headers,
        )
        if not raw:
            response = cls.parse_response(response)
        return response

    @classmethod
    def parse_response(cls, response):
        return cls.model.parse_obj(response.json())

    @classmethod
    def get_query_params(self, *args, **kwargs):
        return kwargs

    @classmethod
    def get_headers(cls, *args, **kwargs):
        return {
            "authorization": f"Bearer {cls.get_token()}",
            "ocp-apim-subscription-key": cls.subscription_key,
            "user-agent": settings.XP["USER_AGENT"],
        }

    @classmethod
    def get_path(cls, *args, **kwargs):
        return cls.path

    @classmethod
    def get_token(cls):
        from bull.apps.xpaccount.models import HubCookie

        return HubCookie.objects.token()
