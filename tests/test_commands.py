"""commands tests"""

from typing import Final
from async_reolink.rest.connection import model

from json import dumps

from async_reolink.rest._utilities.json import SmarterJSONEncoder

_EXPECTED_JSON: Final = '{"cmd": "test", "action": 1, "param": {"channel": 1}}'


def test_request():
    req = model.RequestWithChannel(command="test", channel_id=1)
    req.response_type = model.ResponseTypes.DETAILED

    assert isinstance(req.__get_value__(), dict)
    json = dumps(req, cls=SmarterJSONEncoder)
    assert json == _EXPECTED_JSON
