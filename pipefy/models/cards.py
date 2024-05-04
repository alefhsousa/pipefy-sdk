from typing import Dict, Any
from returns.result import safe

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
        return self["card"].get("createdBy", {}).get("email")

    @property
    def fields_by_uuid(self) -> Dict[str, Any]:
        return {
            k.get("field", {}).get("uuid"): k.get("native_value")
            for k in self["card"].get("fields", [])
        }

    @property
    def fields_by_id(self) -> Dict[str, Any]:
        return {
            k.get("field", {}).get("id"): k.get("value")
            for k in self["card"].get("fields", [])
        }

    def __eq__(self, other):
        return self.raw_data == other.raw_data

    @safe
    def parse(self, mapping, parse_function=None):
        data = {mapping.get(k, {}).get("key"): v for k, v in self.fields_by_uuid.items()}
        return DictWrapper(dict(original_data=self.raw_data, parsed_data=data))
