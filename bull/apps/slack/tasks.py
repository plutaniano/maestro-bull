from io import BytesIO

import requests
from bull.core import CeleryApp
from django.utils import timezone
from django.utils.dateformat import format as date_fmt
from PyPDF2 import PdfFileMerger

from bull.apps.slack.boletabot import BoletaBot


@CeleryApp.task()
def send_newspapers(*, channel):
    day = timezone.localdate().day
    url = f"https://cdn.freedomforum.org/dfp/pdf{day}/"
    journal = [
        (":flag-br: Estadão", "BRA_OE.pdf"),
        (":flag-br: Folha de SP", "BRA_FDSP.pdf"),
        (":flag-us: WSJ", "WSJ.pdf"),
        (":flag-us: NYT", "NY_NYT.pdf"),
        (":flag-gb: The Guardian", "UK_TG.pdf"),
        (":flag-ar: Clarín", "ARG_CLA.pdf"),
    ]

    merger, strings = PdfFileMerger(), []
    for name, filename in journal:
        try:
            r = requests.get(url + filename)
            r.raise_for_status()

            merger.append(BytesIO(r.content))
            strings.append(name)
            print(f"Jornal {name} adicionado.")

        except requests.models.HTTPError:
            print(f"Erro ao obter jornal {name}.")

    file = BytesIO()
    merger.write(file)
    file.seek(0)

    BoletaBot.client.files_upload(
        channels=channel,
        file=file.read(),
        initial_comment=f":rolled_up_newspaper: *Jornais do Dia*\n\t"
        + f"\n\t".join(strings),
        filename=f"Jornais - {date_fmt(timezone.localdate(), 'D, d M Y')}.pdf",
        filetype="pdf",
    )


@CeleryApp.task()
def scheduled_slack_message(*, channel, text=None, blocks=None):
    BoletaBot.client.chat_postMessage(
        channel=channel,
        text=text,
        blocks=blocks or [],
    )
