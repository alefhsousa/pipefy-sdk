from typing import Optional

from gql import gql

from .client import BaseClient
from ..models.pipe import PipefyPipeResponse

default_describe_pipe_query = """
        query describePipe($id: ID!){
          pipe(id: $id) {
            id
            name
            publicForm {
              id
              url
            }
            start_form_fields {
              label
              id
              required
            }
            labels {
              id
              name
              color
            }
            phases {
              id
              name
            }
          }
        }
    """


class PipeApi(BaseClient):

    def describe(self, pipe_id: str, query: Optional[str] = None):
        query = query or default_describe_pipe_query
        return self.client.api.fetch_data(gql(query), {"id": pipe_id}).map(
            lambda r: PipefyPipeResponse(r)
        )
