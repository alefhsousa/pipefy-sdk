from typing import Dict, Any

from pipefy.models import DictWrapper


class PipefyCardResponse(DictWrapper):
    @property
    def id(self) -> int:
        return self["card"]["id"]

    @property
    def age(self) -> int:
        return self["card"]["age"]

    @property
    def created_by(self) -> str:
        return self["card"]["createdBy"]["email"]

    @property
    def fields_by_uuid(self) -> Dict[str, Any]:
        return {k["field"]["uuid"]: k.get("native_value") for k in self["card"]["fields"]}

    def __eq__(self, other):
        return self.raw_data == other.raw_data
