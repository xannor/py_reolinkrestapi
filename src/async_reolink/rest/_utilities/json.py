"""JSON helpers"""

import json
from typing import Final, Protocol, TypeGuard

_JSONEncoder = json.JSONEncoder


class SupportsJSON(Protocol):
    """Supports JSON method"""

    def __json__(self, encoder: _JSONEncoder) -> any:
        ...


__JSON__: Final = "__json__"


def supports_json(value: any) -> TypeGuard[SupportsJSON]:
    """Test is object supports __json__"""
    return value is not None and callable(getattr(value, __JSON__, None))


class SmarterJSONEncoder(_JSONEncoder):
    """Encoder that will attempt a SupportsJSON check"""

    def default(self, o: any):
        if supports_json(o):
            return o.__json__(self)
        return super().default(o)


def monkey_patch_smarter_json():
    """Force default json encoder to support __json__"""

    if issubclass(json.JSONEncoder, SmarterJSONEncoder):
        return

    json.JSONEncoder = SmarterJSONEncoder
