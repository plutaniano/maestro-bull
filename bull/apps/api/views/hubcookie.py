from bull.apps.api.serializers import HubCookieSerializer
from rest_framework.mixins import CreateModelMixin
from rest_framework.viewsets import GenericViewSet


class HubCookieViewSet(CreateModelMixin, GenericViewSet):
    permission_classes = []
    serializer_class = HubCookieSerializer
