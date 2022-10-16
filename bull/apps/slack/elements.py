import json
from typing import Any


# Block elements
def Text(
    text: str,
    type: str = "plain_text",
    emoji: bool = True,
    verbatim: bool = False,
) -> dict[str, str | bool]:
    return {
        "type": type,
        "text": text,
        "emoji": emoji,
        "verbatim": verbatim,
    }


def Mrkdwn(text: str) -> dict[str, str]:
    return {
        "text": text,
        "type": "mrkdwn",
    }


def Button(
    text: str,
    action_id: str = "ack",
    style: str = "primary",
    url: str | None = None,
    value: str | dict | None = None,
) -> dict[str, str | dict]:
    element = {
        "type": "button",
        "action_id": action_id,
        "style": style,
        "text": Text(text, emoji=False),
    }

    if value is not None:
        if isinstance(value, dict):
            element["value"] = json.dumps(value)
        else:
            element["value"] = str(value)

    if url is not None:
        element["url"] = str(url)

    return element


def Checkboxes(
    action_id: str, options: list[tuple[str, str]]
) -> dict[str, str | list[dict[str, Any]]]:
    return {
        "type": "checkboxes",
        "action_id": action_id,
        "options": [
            {
                "text": Text(text),
                "value": value,
            }
            for text, value in options
        ],
    }


def Overflow(
    action_id: str, options: list[tuple[str, str]]
) -> dict[str, str | list[dict]]:
    return {
        "type": "overflow",
        "action_id": action_id,
        "options": [
            {
                "text": Text(text),
                "value": value,
            }
            for text, value in options
        ],
    }


# Blocks
def Actions(*elements: dict[str, Any], block_id: str = "") -> dict:
    return {
        "type": "actions",
        "block_id": block_id,
        "elements": elements,
    }


def Context(*elements: str | dict, block_id: str = "") -> dict:
    return {
        "type": "context",
        "block_id": block_id,
        "elements": [e if isinstance(e, dict) else Mrkdwn(e) for e in elements],
    }


def Divider() -> dict[str, str]:
    return {"type": "divider"}


def Header(text: str, block_id: str = "") -> dict[str, str | dict]:
    return {
        "type": "header",
        "block_id": block_id,
        "text": Text(text),
    }


def Image(url: str, alt_text: str = "") -> dict[str, str]:
    if url == "blank":
        url = "https://api.slack.com/img/blocks/bkb_template_images/placeholder.png"
    return {
        "type": "image",
        "image_url": url,
        "alt_text": alt_text,
    }


def Input(
    block_id: str, label: str, element: dict, dispatch_action: bool = False
) -> dict:
    return {
        "type": "input",
        "block_id": block_id,
        "label": Text(label),
        "element": element,
        "dispatch_action": dispatch_action,
    }


def Section(
    text: str | None = None,
    fields: list[str] | None = None,
    accessory: dict | None = None,
    block_id: str = "",
) -> dict:
    d = {"type": "section"}
    if fields is not None:
        d |= {"fields": [Mrkdwn(f) for f in fields]}

    if text is not None:
        d |= {"text": Mrkdwn(text)}

    if isinstance(accessory, dict):
        d |= {"accessory": accessory}

    if block_id is not None:
        d["block_id"] = block_id

    return d


# Outros
def PlainTextInput(action_id: str = "", multiline=False) -> dict[str, str]:
    return {
        "type": "plain_text_input",
        "action_id": action_id,
        "multiline": multiline,
    }
