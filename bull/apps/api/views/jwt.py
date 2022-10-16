import jwt

from bull.apps.api.views.users import UserSerializer
from bull.apps.user.models import User
from bull.core.auth_backends import SlackBackend
from django.conf import settings
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken


class JWTViewSet(viewsets.ViewSet):
    def list(self, request):
        try:
            code = request.query_params.get("code")
            user = SlackBackend().authenticate(request, code)
            refresh_token = RefreshToken.for_user(user)
            access = refresh_token.access_token
            response = Response(
                {
                    "access": str(access),
                    "user": UserSerializer(user).data,
                }
            )
            response.set_cookie(
                key="refreshToken",
                value=str(refresh_token),
                max_age=7 * 24 * 3600,
                httponly=True,
            )
            return response
        except Exception:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

    @action(methods=["GET"], detail=False)
    def refresh(self, request):
        try:
            cookie = request.COOKIES.get("refreshToken")
            refresh = jwt.decode(
                jwt=cookie, key=settings.SECRET_KEY, algorithms=["HS256"]
            )
            user = User.objects.get(pk=refresh["user_id"])
            new_refresh = RefreshToken.for_user(user)
            access_token = new_refresh.access_token
            return Response(
                {
                    "access": str(access_token),
                    "user": UserSerializer(user).data,
                }
            )
        except Exception:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

    @action(methods=["GET"], detail=False)
    def logout(self, request):
        response = Response()
        response.set_cookie(
            key="refreshToken",
            value="",
            max_age=-1,
            httponly=True,
        )
        return response
