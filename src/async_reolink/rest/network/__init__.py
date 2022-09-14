"""REST Network Mixin"""

from typing import Mapping, Sequence
from async_reolink.api import network
from async_reolink.api.led.typings import LightStates, LightingSchedule
from async_reolink.api.ai.typings import AITypes
from async_reolink.api.typings import PercentValue

from ..commands import network as commands


class Network(network.Network):
    """REST Network Mixin"""

    def _create_get_channel_status_request(self):
        return commands.GetChannelStatusRequest()

    def _create_get_local_link_request(self):
        return commands.GetLocalLinkRequest()

    def _create_get_p2p_request(self):
        return commands.GetP2PRequest()

    def _create_get_ports_request(self):
        return commands.GetNetworkPortsRequest()

    def _create_get_rtsp_urls_request(self, channel_id: int = 0):
        return commands.GetRTSPUrlsRequest(channel_id)
