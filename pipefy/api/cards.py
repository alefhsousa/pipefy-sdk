from typing import Optional

from gql import gql

from .client import BaseClient
from ..models.cards import PipefyCardResponse

default_load_card_query = """
        query loadCard($id: ID!){
              card(id: $id) {
                age
                id
                createdAt
                createdBy {
                  displayName
                  email
                }
                fields {
                  name
                  field {
                    id
                    uuid
                  }
                  value
                  native_value
                }
              }
            }
    """


class CardApi(BaseClient):
    def load_card(self, card_id: str, query: Optional[str] = None):
        query = query or default_load_card_query
        return self.client.api.fetch_data(gql(query), {"id": card_id}).map(
            lambda r: PipefyCardResponse(r)
        )
