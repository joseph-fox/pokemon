"""
Base JSON client
"""
import json
import typing
import urllib
from http import client as http_client

import requests
from django.conf import settings
from rest_framework import status

from . import exceptions


class BaseClient:
    base_url = ""
    session = None
    service_name = ""
    extra_headers = None
    token = None
    timeout = 5
    verify_ssl = True

    def __init__(self, session=None):

        if not session:
            session = requests.Session()

        self.session = session

    def _request(
            self,
            method: str,
            path: str,
            valid_statuses: typing.Tuple[int],
            headers: dict = None,
            data: dict = None,
            params=None,
    ):
        if headers is None:
            headers = self._get_headers()

        url = urllib.parse.urljoin(self.base_url, path)

        if data:
            # Explicitly dump the data to JSON.
            # This is crucial. Note all parties honour the JSON header.
            data = json.dumps(data)

        try:
            response = self.session.request(
                method=method,
                url=url,
                data=data,
                params=params,
                headers=headers,
                timeout=self.timeout,
                verify=self.verify_ssl,
            )

        except requests.RequestException as e:
            raise exceptions.UnableToConnect(
                f"We are unable to connect to {self.service_name} - {str(e)}"
            )

        self._raise_for_status(response, valid_statuses)

        if response.status_code == http_client.NO_CONTENT:
            return

        if self._is_content_type_json(response.headers.get("Content-Type")):
            try:
                return response.json()
            except ValueError:
                # Unable to de-serialise the JSON data.
                return

        return response.text

    def _raise_for_status(self, response, valid_statuses):
        if response.status_code == status.HTTP_429_TOO_MANY_REQUESTS:
            raise exceptions.TooManyRequests

        if response.status_code in valid_statuses:
            return

        if response.status_code == status.HTTP_404_NOT_FOUND:
            raise exceptions.NotFound(
                f"Not found - {response.status_code}: " f"{response.text}"
            )

        raise exceptions.InvalidStatus(
            f"The status code is invalid - {response.status_code}: "
            f"{response.text}"
        )

    def _get_headers(self):
        headers = {"Content-Type": "application/json"}
        if self.token:
            headers.update({"Authorization": f"Bearer {self.token}"})

        if self.extra_headers:
            headers.update(self.extra_headers)

        return headers

    def get(
            self,
            *,
            path,
            params=None,
            headers=None
    ):
        return self._request(
            method="get",
            path=path,
            params=params,
            valid_statuses=(http_client.OK,),
            headers=headers,
        )

    def _is_content_type_json(self, content_type):
        if content_type is None:
            return False

        # Be defensive against variations in the content type string.
        if "application/" in content_type and "json" in content_type:
            return True

        return False


class PokemonClient(BaseClient):
    base_url = settings.POKEMON_API_BASE_URL
    timeout = 30

    def get_creatures(self):
        # Get a list of creatures
        path = 'pokemon/'
        return self.get(path=path)

    def get_creature_subset(self, *, offset: int, limit: int):
        """
        Get the URL of one single creature using offset and limit.
        And, leave the responsibility of idempotency to workers.
        """
        path = f'pokemon/?offset={offset}&limit={limit}'
        return self.get(path=path)

    def get_creature(self, *, vendor_id: int):
        path = f'pokemon/{vendor_id}/'

        return self.get(path=path)

    def get_species_description(self, *, name: str):
        path = f'pokemon-species/{name}/'

        return self.get(path=path)


#  Make a singleton
pokemon_client = PokemonClient()
