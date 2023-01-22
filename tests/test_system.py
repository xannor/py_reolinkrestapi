""""Stytem Mixin Test"""

import datetime
import logging
import os

from json import dumps, loads

from types import MappingProxyType
from typing import Final
from pytest import mark


from async_reolink.api.connection.model import Request
from async_reolink.rest._utilities.json import SmarterJSONEncoder
from async_reolink.rest.connection.model import Response as RestCommandResponse
from async_reolink.rest.system.mixin import System
from .models import MockConnection_SingleExecute

_JSON: Final = MappingProxyType(
    {
        '[{"cmd": "GetAbility", "action": 0, "param": {"User": {"userName": "NULL"}}}]': '{"cmd": "GetAbility", "code": 0, "value":{"Ability":{"3g":{"ver":0,"permit":0},"abilityChn":[{"live":{"ver":1,"permit":4}}], "scheduleVersion":{"ver":0,"permit":4}}}}',
        '[{"cmd": "GetTime", "action": 0}]': '{"cmd": "GetTime", "code": 0, "value": {"Dst": {"enable": 1, "endHour": 2, "endMin": 59, "endMon": 4, "endSec": 0, "endWeek": 1, "endWeekday": 0, "offset": 1, "startHour": 1, "startMin": 59, "startMon": 10, "startSec": 0, "startWeek": 1, "startWeekday": 0}, "Time": {"day": 15, "hour": 21, "hourFmt": 0, "min": 21, "mon": 9, "sec": 57, "timeFmt": "DD/MM/YYYY", "timeZone": -36000, "year": 2022}}}',
    }
)


class TestRig(MockConnection_SingleExecute, System):
    """Test Rig"""

    async def _mocked_execute(self, request: Request):
        query = dumps([request], cls=SmarterJSONEncoder)
        json = _JSON.get(query, None)
        if json is None:
            return None

        _dict = loads(json)
        response = RestCommandResponse.from_response(_dict)
        return response


async def test_get_ability():
    """Test get_ability returns expected values"""

    rig = TestRig()
    ability = await rig.get_capabilities()

    assert ability
    assert len(ability.channels) > 0
    assert ability.channels[0].live.value == ability.channels[0].live.Type.MAIN_EXTERN_SUB
    assert ability.schedule_version.permissions == ability.schedule_version.Permissions.READ


async def test_get_time():
    """Test get_timereturns expected values"""

    rig = TestRig()
    dev_time = await rig.get_time()
    dev_tz = await rig.get_time_info()

    assert dev_time
    assert dev_tz
    assert dev_time == datetime.datetime(2022, 9, 15, 21, 21, 57, tzinfo=dev_tz)
