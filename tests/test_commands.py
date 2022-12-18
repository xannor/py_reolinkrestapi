"""commands tests"""

from typing import Final
from async_reolink.rest.connection import model

from json import dumps

from async_reolink.rest._utilities.json import SmarterJSONEncoder

_EXPECTED_JSON: Final = '{"cmd": "test", "action": 1, "param": {"channel": 1}}'


def test_request():
    req = model.RequestWithChannel()
    req.command = "test"
    req.response_type = model.ResponseTypes.DETAILED
    req.channel_id = 1

    assert isinstance(req._provided_value, dict)
    json = dumps(req, cls=SmarterJSONEncoder)
    assert json == _EXPECTED_JSON
