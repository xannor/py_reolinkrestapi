""" test auth mixin """

import logging
import os
from pytest import mark
from async_reolink.api import system

from async_reolink import rest

from .common import MockConnection

_JSON = {
    system.GetAbilitiesCommand.COMMAND: (
        '[{"cmd": "GetAbility", "action": 0, "param": {"User": {"userName": "null"}}}]',
        '[{"cmd": "GetAbility", "code": 0, "value":{"Ability":{}}}]',
    ),
    system.GetDeviceInfoCommand.COMMAND: (
        '[{"cmd": "GetDevInfo", "action": 0}]',
        '[{"cmd": "GetDevInfo", "code": 0, "value": {"DevInfo":{}}}]',
    ),
}


class SystemTestRig(MockConnection, system.System):
    """System test rig"""

    JSON = _JSON


async def test_ability():
    """ability expected values test"""

    client = SystemTestRig()
    assert await client.get_ability() is not None


@mark.skip("Manual run only, requires live device")
async def test_live_ability(caplog):
    """login live test"""

    caplog.set_level(logging.DEBUG)
    client = Client()
    await client.connect(os.environ.get("DEV_IP", "localhost"))
    assert await client.login(
        os.environ.get("DEV_USER", "admin"), os.environ.get("DEV_PASS", "")
    )
    abilities = await client.get_ability()
    await client.disconnect()
    assert abilities


async def test_devinfo():
    """device info test"""

    client = SystemTestRig()
    info = await client.get_device_info()
    assert info is not None


@mark.skip("Manual run only, requires live device")
async def test_live_devinfo(caplog):
    """device info live test"""

    caplog.set_level(logging.DEBUG)
    client = Client()
    await client.connect(os.environ.get("DEV_IP", "localhost"))
    assert await client.login(
        os.environ.get("DEV_USER", "admin"), os.environ.get("DEV_PASS", "")
    )
    info = await client.get_device_info()
    assert info is not None
    await client.disconnect()
