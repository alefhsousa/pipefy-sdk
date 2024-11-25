from typing import Dict, Any, Optional, List
from returns.result import safe

from pipefy.models import DictWrapper


class PipefyPipeResponse(DictWrapper):
    @property
    def pipe(self) -> dict:
        return self["pipe"]

    @property
    def id(self) -> int:
        return self.pipe["id"]

    @property
    def name(self) -> int:
        return self.pipe["name"]

    @property
    def public_form_id(self) -> str:
        return self.pipe.get("publicForm", {}).get("id")

    @property
    def public_form_url(self) -> str:
        return self.pipe.get("publicForm", {}).get("url")

    @property
    def start_form_fields(self) -> List[Dict[str, Any]]:
        return self.pipe.get("start_form_fields", [])

    @property
    def start_form_fields_by_label(self) -> Dict[str, Any]:
        return {item['label']: item for item in self.start_form_fields}

    @property
    def labels(self) -> List[Dict[str, Any]]:
        return self.pipe.get("labels", [])

    @property
    def labels_by_name(self) -> Dict[str, Any]:
        return {item['name']: item for item in self.labels}

    @property
    def phases(self) -> List[Dict[str, Any]]:
        return self.pipe.get("phases", [])

    @property
    def phases_by_name(self) -> Dict[str, Any]:
        return {item['name']: item for item in self.start_form_fields}

    def __eq__(self, other):
        return self.raw_data == other.raw_data

    @safe
    def parse(self, mapping, parse_function=None):
        data = {mapping.get(k, {}).get("key"): v for k, v in self.fields_by_uuid.items()}
        return DictWrapper(dict(original_data=self.raw_data, parsed_data=data))
