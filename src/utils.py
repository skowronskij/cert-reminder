import json

from pathlib import Path
from typing import List

from .messengers.webhook_messenger import WebhookMessenger


def read_settings(settings_path: str) -> dict:
    """
    Read settings from a file
    :param settings_path: str
    :return: dict
    """
    settings_path = Path(settings_path)

    with open(settings_path) as f:
        settings = json.load(f)

    return settings


def check_required_keys(settings: dict) -> None:
    """
    Check if all required keys are present in settings
    :param settings: dict
    :return: None
    """
    required_keys = ['URLS', 'DAYS_BUFFER']
    for key in required_keys:
        if key not in settings.keys():
            raise KeyError(f'Missing settings key: {key}')


def send_webhook_messages(message: str, webhook_urls: List[str] = []) -> None:
    """
    Send a webhook message
    :param message: str
    :param webhook_urls: List[str]
    :return: None
    """
    for url in webhook_urls:
        WebhookMessenger(url).send_message(message)
