import jwt
from bull.apps.slack.boletabot import BoletaBot
from bull.apps.user.models import User
from django.conf import settings
from django.contrib.auth.backends import BaseBackend
from bull.utils import get_object_or_none


class SlackBackend(BaseBackend):
    def authenticate(self, request, code):
        response = BoletaBot.client.openid_connect_token(
            client_id=settings.SLACK["CLIENT_ID"],
            client_secret=settings.SLACK["CLIENT_SECRET"],
            code=code,
        )
        token = response.data["id_token"]
        jwk_client = jwt.PyJWKClient(settings.SLACK["OPENID_URL"])
        signing_key = jwk_client.get_signing_key_from_jwt(token)
        data = jwt.decode(
            jwt=token,
            key=signing_key.key,
            algorithms=["RS256"],
            audience=settings.SLACK["CLIENT_ID"],
        )
        return get_object_or_none(User, slack_id=data["sub"])

    def get_user(self, pk):
        return get_object_or_none(User, pk=pk)
