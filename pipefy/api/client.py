from gql import Client
from gql.transport.exceptions import TransportQueryError
from gql.transport.requests import RequestsHTTPTransport
from returns.result import safe

from .. import __version__
from ..infrastructure.configuration.conf import settings
from ..models.message import Message, MessageCategory


class ApiClient:
    def __init__(
        self,
        pipefy_url=None,
        auth_token=None,
        user_agent=f"{settings.constants.user_agent}/{__version__}",
    ):
        self.transport = RequestsHTTPTransport(
            url=pipefy_url if pipefy_url else settings.pipefy_url,
            verify=True,
            retries=3,
            headers={
                "Authorization": f"Bearer {auth_token if auth_token else settings.token}",
                "User-Agent": user_agent,
            },
        )
        self.client = Client(transport=self.transport)

    def fetch_data(self, query, variables):
        return self._fetch_data(query, variables).alt(self._failed)

    @safe
    def _fetch_data(self, query, variables):
        return self.client.execute(query, variable_values=variables)

    def _failed(self, failure):
        message = Message(
            category=MessageCategory.ERROR,
            expected="data",
            given="errors",
            key="pipefy.fetch_data.error",
            message="problem to fetch data from pipefy",
        )
        if isinstance(failure, TransportQueryError):
            message.add_metadata("errors", failure.errors)

        return message


class BaseClient:
    def __init__(self, client=None):
        self.client = client
