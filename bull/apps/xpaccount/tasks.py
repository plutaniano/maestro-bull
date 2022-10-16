import io
import random
import time
from itertools import accumulate

import pandas as pd
from bull.apps.slack.boletabot import BoletaBot
from bull.apps.slack.elements import Divider, Header, Section
from bull.apps.xpaccount.exceptions import ValidCookieNotAvailable
from bull.apps.xpaccount.models import HubCookie, XPAccount
from bull.core import CeleryApp
from bull.utils import xp_api
from django.utils import timezone


@CeleryApp.task()
def mesa_rv_update(channel, requested_by, delay=4):
    qs = XPAccount.objects.mesa_rv().order_by("name")
    count = qs.count()

    blocks = [
        Header(f"Atualizando a carteira de {count} clientes da mesa rv. :loading:"),
        Divider(),
        Section(text="*Tempo restante*: calculando..."),
        Section(text="*Progresso*: calculando..."),
        Section(text="*Última atualização*: -"),
        Divider(),
    ]

    ts = BoletaBot.client.chat_postMessage(
        text="Iniciando sincronização das posições dos clientes da mesa RV.",
        channel=channel,
        blocks=blocks,
    ).data["ts"]

    for i, acc in enumerate(qs):
        # 1.2 -> 20% para compensar o delay da rede
        mins_left = (count - i) * delay * 1.2 / 60
        time.sleep(delay)

        try:
            acc.update_positions()
            blocks[2] = Section(text=f"*Tempo restante*: {mins_left:.0f} min")
            blocks[3] = Section(text=f"*Progresso*: {i + 1}/{count}")
            blocks[4] = Section(
                text=f"*Última atualização: <{acc.hub_url}|{acc.name}>*"
            )

        except Exception as e:
            if isinstance(e, ValidCookieNotAvailable):
                err = f":warning: Cookie válido não disponível. [xp_account:{acc.pk}]"
            else:
                err = f":warning: erro desconhecido. [xp_account:{acc.pk};error={e}"
            blocks.append(Section(text=err))

        BoletaBot.client.chat_update(channel=channel, blocks=blocks, ts=ts)

        # Por padrão, len(blocks) == 7. Se chegar à 10
        # quer dizer que ocorreram 4 erros.
        if len(blocks) >= 10:
            blocks[0] = Header(":x: Atualização abortada")
            BoletaBot.client.chat_postMessage(
                channel=channel,
                thread_ts=ts,
                text=f"<@{requested_by}> A atualização das carteiras foi abortada",
            )
            return

    else:
        blocks = [
            Header(f":white_check_mark: {i + 1} carteiras atualizadas com sucesso")
        ]

    BoletaBot.client.chat_update(channel=channel, blocks=blocks, ts=ts)

    XPAccount.objects.mesa_rv().full_export(send_to=channel)


@CeleryApp.task
def update_oldest():
    """Seleciona um cliente ativo para realizar a atualização das posições. Prioriza os
    clientes que não possuem nenhum dado de posições. Caso todos tenham, atualiza o
    cliente com os dados mais antigos.

    Task feita para rodar constantemente com o celery_beat, para manter a base
    razoavelmente atualizada.
    """
    if HubCookie.objects.valid_cookie():
        accs = XPAccount.objects.active().least_recently_updated()
        acc = random.choice(accs[:15])

        try:
            acc.update_positions()
            print(f"{acc} updated!", end="")

        except ValidCookieNotAvailable as e:
            print(f"erro {e} ao atualizar {acc}", end="")


@CeleryApp.task()
def sync():
    if HubCookie.objects.valid_cookie():
        XPAccount.objects.sync()


@CeleryApp.task()
def best_available_assets(*, channel):
    while len(all_assets := xp_api.available_assets.get().data) < 100:
        print("sleeping for 60s")
        time.sleep(60)
    fees = xp_api.available_assets.best_fees()
    comissions = xp_api.available_assets.best_comissions()
    buffer = io.BytesIO()
    with pd.ExcelWriter(buffer) as writer:
        pd.DataFrame.from_dict(accumulate(fees)).to_excel(
            writer, sheet_name="Melhores Taxas"
        )
        pd.DataFrame.from_dict(reduce(operator.add, comissions, [])).to_excel(
            writer, sheet_name="Melhores Comissões"
        )
        pd.DataFrame.from_dict([a.dict() for a in all_assets]).to_excel(
            writer, sheet_name="Todos"
        )
    buffer.seek(0)
    BoletaBot.client.files_upload(
        channels=channel,
        text="Planilha de melhores produtos disponíveis",
        file=buffer,
        filetype="xlsx",
        filename=f"available_assets_export_{timezone.localtime():%Y-%m-%d_%Hh%M}.xlsx",
        initial_comment="Planilha dos melhores produtos disponíveis na plataforma",
    )
