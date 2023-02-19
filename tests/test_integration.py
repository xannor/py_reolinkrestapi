"""Issues from users"""

from datetime import datetime
from json import dumps, loads
import logging
from types import MappingProxyType
from typing import Final
from async_reolink.api.network.typing import LinkTypes
from async_reolink.api.connection.model import Request
from async_reolink.rest.connection.model import Response as RestCommandResponse
from async_reolink.rest.system import mixin as system
from async_reolink.rest.ptz import mixin as ptz
from async_reolink.rest.ai import mixin as ai
from async_reolink.rest.alarm import mixin as alarm
from async_reolink.rest.network import mixin as network
from .models import MockConnection

from async_reolink.api.system import capabilities

from async_reolink.rest._utilities.json import SmarterJSONEncoder

_JSON: Final = MappingProxyType(
    {
        '[{"cmd": "GetTime", "action": 0}, {"cmd": "GetChannelstatus", "action": 0}, {"cmd": "GetNetPort", "action": 0}, {"cmd": "GetP2p", "action": 0}, {"cmd": "GetLocalLink", "action": 0}]': '[{"cmd": "GetTime", "code": 0, "value": {"Dst": {"enable": 0, "endHour": 2, "endMin": 0, "endMon": 10, "endSec": 0, "endWeek": 5, "endWeekday": 0, "offset": 1, "startHour": 2, "startMin": 0, "startMon": 3, "startSec": 0, "startWeek": 2, "startWeekday": 0}, "Time": {"day": 22, "hour": 11, "hourFmt": 0, "min": 56, "mon": 1, "sec": 2, "timeFmt": "DD/MM/YYYY", "timeZone": 18000, "year": 2023}}}, {"cmd": "GetChannelstatus", "code": 0, "value": {"count": 2, "status": [{"channel": 0, "name": "1", "online": 1, "typeInfo": "Reolink Duo WiFi"}, {"channel": 1, "name": "2", "online": 1, "typeInfo": "Reolink Duo WiFi"}]}}, {"cmd": "GetNetPort", "code": 0, "value": {"NetPort": {"httpEnable": 1, "httpPort": 80, "httpsEnable": 1, "httpsPort": 443, "mediaPort": 9000, "onvifEnable": 0, "onvifPort": 8000, "rtmpEnable": 1, "rtmpPort": 1935, "rtspEnable": 0, "rtspPort": 554}}}, {"cmd": "GetP2p", "code": 0, "value": {"P2p": {"enable": 1, "uid": "UUIDXX"}}}, {"cmd": "GetLocalLink", "code": 0, "value": {"LocalLink": {"activeLink": "Wifi", "dns": {"auto": 1, "dns1": "192.168.1.1", "dns2": ""}, "mac": "xx:xx:xx:xx:xx:xx", "static": {"gateway": "192.168.1.1", "ip": "192.168.1.2", "mask": "255.255.255.0"}, "type": "DHCP"}}}]'
    }
)


class TestRig(MockConnection, system.System, network.Network, ptz.PTZ, ai.AI):
    """Test Rig"""

    def __init__(self, *args, logger: logging.Logger = None, **kwargs) -> None:
        super().__init__(*args, logger=logger, **kwargs)

    def _execute(self, *args: Request):
        if self._logger is not None:
            self._logger.info("_execute fired")

        json = dumps(args, cls=SmarterJSONEncoder)
        json = _JSON[json]
        results: list[dict] = loads(json)

        async def _mock_iterable():
            for response in results:
                yield RestCommandResponse.from_response(response)

        return _mock_iterable()


async def test_init():
    """Test initialization"""

    client = TestRig()
    reqs = (
        system.system.GetTimeRequest(),
        network.command.GetChannelStatusRequest(),
        network.command.GetNetworkPortsRequest(),
        network.command.GetP2PRequest(),
        network.command.GetLocalLinkRequest(),
    )

    worked = False
    async for response in client.batch(reqs):
        assert not isinstance(response, bytes)
        worked = True
        if isinstance(response, system.system.GetTimeResponse):
            continue
        elif isinstance(response, network.command.GetChannelStatusResponse):
            channels = response.channels
            assert channels
            assert len(channels) == 2
            iterated = False
            for channel_id in channels:
                iterated = True
                channel = channels[channel_id]
                assert channel
                assert channel.channel_id == channel_id
                assert channel.name
                assert channel.online
                assert channel.type

            assert iterated

            continue
        elif isinstance(response, network.command.GetNetworkPortsResponse):
            continue
        elif isinstance(response, network.command.GetP2PResponse):
            continue
        elif isinstance(response, network.command.GetLocalLinkResponse):
            continue
        else:
            assert False

    assert worked
