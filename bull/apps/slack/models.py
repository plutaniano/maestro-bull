from datetime import datetime

from django.db import models
from emoji import emojize
from bull.utils import BR_TZ

from bull.apps.slack.boletabot import BoletaBot


class SlackUserQuerySet(models.QuerySet):
    def active(self):
        return self.filter(deleted=False)


class SlackUserManager(models.Manager):
    def get_queryset(self):
        return SlackUserQuerySet(self.model, using=self._db)

    def sync(self):
        new = 0
        for user in BoletaBot.client.users_list()["members"]:
            _, created = self.update_or_create_from_api(user)
            new += created
        return new

    def update_or_create_from_api(self, user):
        return self.update_or_create(
            id=user["id"],
            defaults=user
            | {
                "updated": datetime.fromtimestamp(user["updated"], tz=BR_TZ),
            },
        )


class SlackUser(models.Model):
    id = models.CharField(
        verbose_name="Slack User ID",
        max_length=32,
        primary_key=True,
    )
    team_id = models.CharField(
        verbose_name="Slack Team ID",
        max_length=32,
    )
    name = models.CharField(
        verbose_name="Slack Username",
        max_length=64,
    )
    deleted = models.BooleanField(
        verbose_name="Deletado",
    )
    color = models.CharField(
        verbose_name="Cor",
        max_length=6,
    )
    real_name = models.CharField(
        verbose_name="Nome Completo",
        max_length=128,
    )
    tz = models.CharField(
        verbose_name="Fuso Horário",
        max_length=64,
    )
    tz_label = models.CharField(
        verbose_name="Nome do fuso horário",
        max_length=64,
    )
    tz_offset = models.IntegerField(
        verbose_name="Offset do fuso horário",
        null=True,
        blank=True,
    )
    profile = models.JSONField(
        verbose_name="Slack Profile",
        default=dict,
    )
    is_admin = models.BooleanField(
        verbose_name="Slack Admin",
        null=True,
        blank=True,
    )
    is_owner = models.BooleanField(
        verbose_name="Slack Workspace Owner",
        null=True,
        blank=True,
    )
    is_primary_owner = models.BooleanField(
        verbose_name="Slack Workspace Primary Owner",
        null=True,
        blank=True,
    )
    is_restricted = models.BooleanField(
        verbose_name="Slack Restricted",
        null=True,
        blank=True,
    )
    is_ultra_restricted = models.BooleanField(
        verbose_name="Slack Ultra Restricted",
        null=True,
        blank=True,
    )
    is_bot = models.BooleanField(
        verbose_name="Slack Bot",
        null=True,
        blank=True,
    )
    is_app_user = models.BooleanField(
        verbose_name="Slack App User",
    )
    is_workflow_bot = models.BooleanField(
        verbose_name="É um bot de workflow?",
        default=False,
    )
    updated = models.DateTimeField(
        verbose_name="Atualizado em",
    )
    is_email_confirmed = models.BooleanField(
        verbose_name="Confirmou email no slack?",
        null=True,
        blank=True,
    )
    who_can_share_contact_card = models.CharField(
        verbose_name="Quem pode compartilhar cartão de contato",
        max_length=128,
    )
    is_invited_user = models.BooleanField(
        verbose_name="Usuário convidado",
        null=True,
        blank=True,
    )

    objects = SlackUserManager.from_queryset(SlackUserQuerySet)()

    def __str__(self):
        if self.deleted:
            emoji = emojize(":cross_mark:")
        else:
            emoji = emojize(":check_mark_button:")
        return f"{self.name} {self.id}{emoji}"

    class Meta:
        ordering = ["name"]

    @property
    def mrkdwn(self):
        "String que referência um usuário no Slack utilizando markdown."
        return f"<@{self.id}>"

    @property
    def url(self):
        "Link para o usuário no Slack."
        return f"slack://user?team=T01PL5F7Q3E&id={self.id}"

    def join_channel(self, channel):
        return BoletaBot.client.conversations_join(channel=channel)

    def send_message(self, text=None, blocks=None):
        blocks = blocks or []
        return BoletaBot.client.chat_postMessage(
            channel=self.id,
            text=text,
            blocks=blocks,
        )
