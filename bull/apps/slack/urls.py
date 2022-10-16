from django.urls import path

from bull.apps.slack.views import slack_handler, oauth_authorize

urlpatterns = [
    path("events", slack_handler),
    path("interactivity", slack_handler),
    path("load_menus", slack_handler),
    path("oauth/authorize", oauth_authorize),
]
