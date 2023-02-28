import enum
from dataclasses import dataclass, asdict
from json import dumps
from typing import Any, Optional


class MessageCategory(enum.Enum):
    ERROR = "error"


@dataclass
class Message:
    category: MessageCategory
    expected: Any
    given: Any
    key: str
    message: str
    metadata: Optional[dict] = None

    @property
    def to_json(self):
        return dumps(asdict(self))

    def add_metadata(self, key, data):
        if self.metadata:
            self.metadata[key] = data
        else:
            self.metadata = {key: data}
        return self
