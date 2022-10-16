from bull.apps.slack.boletabot import BoletaBot
from bull.core.auth_backends import SlackBackend
from django.contrib.auth import login
from django.http import HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from slack_bolt.adapter.django import SlackRequestHandler

handler = SlackRequestHandler(app=BoletaBot)


@csrf_exempt
def slack_handler(request):
    "Handle events, interactions and load_menu requests from Slack"
    return handler.handle(request)


def oauth_authorize(request):
    try:
        code = request.GET.get("code")
        user = SlackBackend().authenticate(request, code)
        login(request, user, backend="bull.core.auth_backends.SlackBackend")
        return request

    except Exception:
        return HttpResponseBadRequest()
