from pipefy.api.cards import CardApi
from pipefy.api.client import ApiClient
from pipefy.api.pipe import PipeApi


class PipefyClient:
    def __init__(self, *args, **kwargs):
        self.api = ApiClient(*args, **kwargs)

    @property
    def cards(self):
        return CardApi(self)

    @property
    def pipe(self):
        return PipeApi(self)
