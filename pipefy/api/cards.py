import uuid
from typing import Optional, List, Dict, Any

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

move_card_to_phase_mutation = """
    mutation moveCardToPhase($card_id: ID!, $phase_id: ID!, $identifier: String) {
      moveCardToPhase(input: {
        clientMutationId: $identifier,
        card_id: $card_id,
        destination_phase_id: $phase_id
      }) {
        card {
          age
        }
      }
    }
"""


create_card_comment_mutation = """
    mutation createComment($card_id: ID!, $comment: String!, $identifier: String) {
  createComment(input: {
    clientMutationId: $identifier,
    card_id: $card_id,
    text: $comment
  }) {
    clientMutationId
    comment {
      author {
        name
        username
      }
      created_at
      id
      text
    }
  }
}
"""

create_card_mutation = """
    mutation createCard($pipe_id: ID!, $fields: [FieldValueInput],
    $title: String, $identifier: String){
      createCard(input: {
        pipe_id: $pipe_id,
        title: $title,
        fields_attributes: $fields
        clientMutationId: $identifier
      }) {
        card {
          age
          id
        }
      }
    }
"""


class CardApi(BaseClient):

    def create(self, pipe_id: str, title: Optional[str] = None, fields: Optional[List[Dict[str, Any]]] = None,
               identifier: Optional[str] = None,
               mutation: Optional[str] = None):
        mutation = mutation or create_card_mutation
        identifier = identifier or str(uuid.uuid4())
        return self.client.api.fetch_data(
            gql(mutation), dict(pipe_id=pipe_id, fields=fields, title=title, identifier=identifier)
        )

    def load_card(self, card_id: str, query: Optional[str] = None):
        query = query or default_load_card_query
        return self.client.api.fetch_data(gql(query), {"id": card_id}).map(
            lambda r: PipefyCardResponse(r)
        )

    def move_to_phase(
        self,
        card_id: str,
        phase_id: str,
        identifier: Optional[str] = None,
        mutation: Optional[str] = None,
    ):
        mutation = mutation or move_card_to_phase_mutation
        identifier = identifier or str(uuid.uuid4())
        return self.client.api.fetch_data(
            gql(mutation), dict(card_id=card_id, phase_id=phase_id, identifier=identifier)
        )

    def create_comment(
        self,
        card_id: str,
        comment: str,
        identifier: Optional[str] = None,
        mutation: Optional[str] = None,
    ):
        mutation = mutation or create_card_comment_mutation
        identifier = identifier or str(uuid.uuid4())
        return self.client.api.fetch_data(
            gql(mutation), dict(card_id=card_id, comment=comment, identifier=identifier)
        )
