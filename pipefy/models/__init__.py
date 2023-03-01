from typing import Dict, Any


class DictWrapper:
    def __init__(self, data: Dict[str, Any]):
        self._data = data

    def __getitem__(self, key: str) -> Any:
        return self._data[key]

    def __setitem__(self, key: str, value: Any) -> Any:
        self._data[key] = value

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, DictWrapper):
            return False

        return self._data == other._data

    def get(self, key: str, default=None):
        return self._data.get(key, default)

    @property
    def raw_data(self) -> Dict[str, Any]:
        """The original raw dict"""
        return self._data

    def parse(self, mapping, parse_function=None):
        print("start mapping")
        return self
