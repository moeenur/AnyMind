from http import HTTPStatus
from django.conf import settings
import logging
import requests
import copy

logger = logging.getLogger(__name__)


class ClientApi:
    endpoint_url = None
    method = 'get'
    auth_token = settings.TW_AUTH_TOKEN

    def construct_url(self):
        return self.endpoint_url.format(settings=settings)

    def get_auth_token(self):
        return f"Bearer {self.auth_token}" if self.auth_token else None

    def clean_data(self, data):
        return copy.deepcopy(data)

    def make_headers(self):
        return {
            "Authorization": self.get_auth_token()
        }

    def send(self, headers, payload):
        if self.method == 'get':
            response = requests.get(self.construct_url(), headers=headers, params=payload)
        else:
            raise Exception('Unknown method')
        if response.status_code != HTTPStatus.OK:
            logger.exception('[ClientApi][send] Error: {}'.format(response.content))
            raise InternalAPIResponseError(response=response)
        return response

    def run(self, data):
        headers = self.make_headers()
        cleaned_data = self.clean_data(data)
        return self.send(headers, cleaned_data)


class APIServerException(Exception):
    pass


class InternalAPIResponseError(APIServerException):
    def __init__(self, response):
        self.message = 'Internal Server {} error.'.format(response.status_code)
        self.response = response
        self.status_code = response.status_code

    def __str__(self):
        return f'{self.message} \nresponse:\n {self.response.content}'
