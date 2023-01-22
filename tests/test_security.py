""""Security Mixin Test"""

import logging
import os

from json import dumps, loads

from types import MappingProxyType
from typing import Final
from pytest import mark


from async_reolink.api.connection.model import Request
from async_reolink.rest._utilities.json import SmarterJSONEncoder
from async_reolink.rest.connection.model import Response as RestCommandResponse
from async_reolink.rest.security.mixin import Security
from .models import MockConnection_SingleExecute

_JSON: Final = MappingProxyType(
    {
        '[{"cmd": "Login", "action": 0, "param": {"User": {"userName": "admin", "password": "test", "Version": 0}}}]': '{"cmd": "Login", "code": 0, "value": {"Token":{"leaseTime": 60, "name": "test"}}}'
    }
)


class TestRig(MockConnection_SingleExecute, Security):
    """Test Rig"""

    async def _mocked_execute(self, request: Request):
        query = dumps([request], cls=SmarterJSONEncoder)
        json = _JSON.get(query, None)
        if json is None:
            return None

        _dict = loads(json)
        response = RestCommandResponse.from_response(_dict)
        return response


async def test_login():
    """Test login returns expected values"""

    rig = TestRig()
    assert await rig.login("admin", "test")
    assert rig.is_authenticated
    assert 59.999 < rig.authentication_timeout < 60
    # cannot fix the actual timeout time so within 1/100 a second is close enough to validate
    auth = rig.authentication_id
    assert auth
    assert auth.weak == hash("admin")
    assert auth.strong == hash("test")
