import requests

from requests import Response


class WebhookMessenger:

    def __init__(self, url: str) -> None:
        """
        Constructos
        :param url: str
        :return: None
        """
        self.url = url

    def send_message(self, message: str) -> Response:
        """
        Send a message to a webhook
        :param message: str
        :return: None
        """
        data = {
            'content': message
        }

        response = requests.post(self.url, json=data)

        if response.status_code != 204:
            raise Exception(f'Error sending message to webhook.\nStatus code: {response.status_code}\nResponse: {response.json()}')

        return response
