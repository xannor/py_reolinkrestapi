""""Stytem Mixin Test"""

import logging
import os

from json import dumps, loads

from types import MappingProxyType
from typing import Final
from pytest import mark


from async_reolink.api.connection.model import Request
from async_reolink.rest.connection.model import Response as RestCommandResponse
from async_reolink.api.system.mixin import System
from .models import MockConnection_SingleExecute

_JSON: Final = MappingProxyType(
    {
        '[{"cmd": "GetAbility", "action": 0, "param": {"User": {"userName": "null"}}}]': '{"cmd": "GetAbility", "code": 0, "value":{"Ability":{"3g":{"ver":0,"perm":0},"abilityChn":[{"live":{"ver":1,"perm":4}}], "scheduleVersion":{"ver":0,"perm":4}}}}'
    }
)


class TestRig(MockConnection_SingleExecute, System):
    """Test Rig"""

    async def _mocked_execute(self, request: Request):
        query = dumps([request._get_request()])
        json = _JSON.get(query, None)
        if json is None:
            return None

        _dict = loads(json)
        response = RestCommandResponse.create_from(_dict)
        return response


async def test_get_ability():
    """Test get_ability returns expected values"""

    rig = TestRig()
    ability = await rig.get_ability()

    assert ability
    assert len(ability.channels) > 0
    assert ability.channels[0].live.value == 1
    assert ability.schedule_version.permissions == 4
