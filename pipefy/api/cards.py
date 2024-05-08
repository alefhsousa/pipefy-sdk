import uuid
from typing import Optional, List, Dict, Any

from gql import gql
from returns.pipeline import is_successful
from returns.result import Success

from .client import BaseClient
from ..models.cards import PipefyCardResponse

default_load_card_query = """
        query loadCard($id: ID!){
              card(id: $id) {
                age
                id
                suid
                title
                finished_at
                createdAt
                updated_at
                createdBy {
                  displayName
                  email
                }
                pipe {
                  id
                  suid
                  uuid
                  description
                  title_field {
                    label
                    id
                    internal_id
                  }
                  color
                  name
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

create_card_with_phase_id_mutation = """
    mutation createCard($pipe_id: ID!, $fields: [FieldValueInput],
    $title: String, $phase_id: ID $identifier: String){
      createCard(input: {
        pipe_id: $pipe_id,
        title: $title,
        phase_id: $phase_id
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

delete_card_mutation = """
    mutation deleteCard($card_id: ID!, $identifier: String){
      deleteCard(input: {id: $card_id, clientMutationId: $identifier}) {
        success
      }
    }
"""

get_all_cards_from_pipe_query = """
            query AllCards($pipeId: ID!, $nextCursor: String) {
                allCards(pipeId: $pipeId, first:50, after: $nextCursor) {
                    nodes {
                      id
                      age
                      current_phase {
                        id
                        name
                      }
                      fields {
                        field {
                            id
                            internal_id
                            index_name
                            index
                        }
                        value
                      }

                    }
                    pageInfo {
                      endCursor
                      hasNextPage
                      startCursor
                    }
                }
            }
            """


update_card_labels_mutation = """
        mutation addCardLabels($card_id: ID!, $label_ids: [ID]!) {
          updateCard(input: { id: $card_id, label_ids: $label_ids }) {
            card {
                age
                  fields {
                    value
                    field {
                      id
                    }
                  }
                current_phase {
                    name
                    id
                }
            }
            clientMutationId
          } 
        }
"""

update_card_field_mutation = """
        mutation mutation updateCardField($card_id: ID!, $field_id: ID!, $value: [UndefinedInput]) {
          updateCardField(input: { card_id: $card_id, field_id: $field_id, new_value: $value}) {
            card {
                age
                  fields {
                    value
                    field {
                      id
                    }
                  }
                current_phase {
                    name
                    id
                }
            }
            clientMutationId
          } 
        }
"""


class CardApi(BaseClient):
    def create(
        self,
        pipe_id: str,
        title: Optional[str] = None,
        fields: Optional[List[Dict[str, Any]]] = None,
        identifier: Optional[str] = None,
        mutation: Optional[str] = None,
    ):
        mutation = mutation or create_card_mutation
        identifier = identifier or str(uuid.uuid4())
        return self.client.api.fetch_data(
            gql(mutation), dict(pipe_id=pipe_id, fields=fields, title=title, identifier=identifier)
        )

    def create_with_phase_id(
        self,
        pipe_id: str,
        phase_id: str,
        title: Optional[str] = None,
        fields: Optional[List[Dict[str, Any]]] = None,
        identifier: Optional[str] = None,
        mutation: Optional[str] = None,
    ):
        mutation = mutation or create_card_with_phase_id_mutation
        identifier = identifier or str(uuid.uuid4())
        return self.client.api.fetch_data(
            gql(mutation),
            dict(
                pipe_id=pipe_id,
                fields=fields,
                phase_id=phase_id,
                title=title,
                identifier=identifier,
            ),
        )

    def delete(
        self, card_id: str, identifier: Optional[str] = None, mutation: Optional[str] = None
    ):
        mutation = mutation or delete_card_mutation
        identifier = identifier or str(uuid.uuid4())
        return self.client.api.fetch_data(
            gql(mutation), dict(card_id=card_id, identifier=identifier)
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

    def get_all_cards_from_pipe(
        self,
        pipe_id: str,
        cursor: Optional[str] = None,
        accumulator: Optional[List[Dict]] = None,
        query: Optional[str] = None,
    ):
        query = query or get_all_cards_from_pipe_query
        acc_data = accumulator or list()
        dados = (
            self.client.api.fetch_data(gql(query), {"pipeId": pipe_id, "nextCursor": cursor})
            .map(lambda r: self.parse_data(r))
            .map(lambda r: self._add_pipe_id(r, pipe_id))
            .map(lambda r: self._accumulate_data(r, acc_data))
            .map(lambda r: self._fetch_possible_next_page(r))
        )

        if is_successful(dados):
            data = dados.unwrap()
            if data["has_next_page"]:
                return self.get_all_cards_from_pipe(
                    data["pipe_id"], accumulator=data["accumulator"], cursor=data["endCursor"]
                )
            return Success(data['accumulator'])

        return dados

    def upsert_label_cards(
        self,
        card_id: str,
        labels: List[str],
        identifier: Optional[str] = None,
        mutation: Optional[str] = None,
    ):
        mutation = mutation or update_card_labels_mutation
        identifier = identifier or str(uuid.uuid4())
        return self.client.api.fetch_data(
            gql(mutation), dict(card_id=card_id, label_ids=labels, identifier=identifier)
        )

    def parse_data(self, data: Dict[str, Any]):
        cards = [PipefyCardResponse({'card': card}) for card in data["allCards"]["nodes"]]
        return {"response": data, "parsed_cards": cards}

    def _fetch_possible_next_page(self, data: Dict[str, Any]):
        page_info = data["response"]["allCards"]["pageInfo"]
        has_next_page = page_info["hasNextPage"]
        if has_next_page:
            data["has_next_page"] = True
            data["endCursor"] = page_info["endCursor"]
        else:
            data["has_next_page"] = False

        return data

    def _accumulate_data(self, data: Dict[str, Any], accumulator: List[Any]):
        accumulator += data["parsed_cards"]
        data["accumulator"] = accumulator
        return data

    def _call_function_if_has_next_page(self, data: Dict[str, Any]):
        if data["has_next_page"]:
            return self.get_all_cards_from_pipe(
                data["pipe_id"], accumulator=data["accumulator"], cursor=data["endCursor"]
            )

        return Success(data)

    def _add_pipe_id(self, data: Dict[str, Any], pipe_id: str):
        data["pipe_id"] = pipe_id
        return data