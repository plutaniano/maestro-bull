from django.conf import settings
from slack_bolt import App
from slack_bolt.authorization.authorize_result import AuthorizeResult


def authorize(enterprise_id, team_id, logger):
    if team_id == settings.SLACK["TEAM_ID"]:
        return AuthorizeResult(
            enterprise_id=enterprise_id,
            team_id=team_id,
            bot_token=settings.SLACK["SECRET_TOKEN"],
            bot_id=settings.SLACK["BOT_ID"],
            bot_user_id=settings.SLACK["BOT_USER_ID"],
        )


BoletaBot = App(
    signing_secret=settings.SLACK["SIGNING_SECRET"],
    token=settings.SLACK["SECRET_TOKEN"],
    authorize=authorize,
)


@BoletaBot.action("ack")
def acknowledge(ack):
    "Uma action que só executa ack(). Utilizada para testes."
    ack()
