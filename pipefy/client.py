from pipefy.api.cards import CardApi
from pipefy.api.client import ApiClient


class PipefyClient:
    def __init__(self, *args, **kwargs):
        self.api = ApiClient(*args, **kwargs)

    @property
    def cards(self):
        print("oi")
        return CardApi(self)
