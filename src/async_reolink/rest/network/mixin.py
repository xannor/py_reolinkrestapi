"""REST Network Mixin"""

from async_reolink.api.connection.model import Response
from async_reolink.api.network import mixin as network
from async_reolink.api.typing import StreamTypes

from ..security.typing import WithSecurity

from . import command


class Network(network.Network, WithSecurity):
    """REST Network Mixin"""

    def _create_get_channel_status(self):
        return command.GetChannelStatusRequest()

    def _is_get_channel_status_response(self, response: Response):
        return isinstance(response, command.GetChannelStatusResponse)

    def _create_get_local_link(self):
        return command.GetLocalLinkRequest()

    def _is_get_local_link_response(self, response: Response):
        return isinstance(response, command.GetLocalLinkResponse)

    def _create_get_p2p(self):
        return command.GetP2PRequest()

    def _is_get_p2p_response(self, response: Response):
        return isinstance(response, command.GetP2PResponse)

    def _create_get_ports(self):
        return command.GetNetworkPortsRequest()

    def _is_get_ports_response(self, response: Response):
        return isinstance(response, command.GetNetworkPortsResponse)

    def _create_get_rtsp_urls(self, channel_id: int):
        return command.GetRTSPUrlsRequest(channel_id=channel_id)

    def _is_get_rtsp_urls_response(self, response: Response):
        return isinstance(response, command.GetRTSPUrlsResponse)

    async def get_rtmp_url(self, channel: int = 0, stream: StreamTypes = ...):
        url = await super().get_rtmp_url(channel, stream)
        token = self._auth_token
        if token is not None:
            url += f"&token={token}"
        return url

    def _create_get_wifi_info(self):
        return command.GetWifiInfoRequest()

    def _is_get_wifi_info_response(self, response: Response):
        return isinstance(response, command.GetWifiInfoResponse)

    def _create_get_wifi_signal(self):
        return command.GetWifiSignalRequest()

    def _is_get_wifi_signal_response(self, response: Response):
        return isinstance(response, command.GetWifiSignalResponse)
