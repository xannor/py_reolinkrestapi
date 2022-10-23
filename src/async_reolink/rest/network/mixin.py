"""REST Network Mixin"""

from async_reolink.api.network import mixin as network
from async_reolink.api.typing import StreamTypes

from ..security.typing import WithSecurity


class Network(network.Network, WithSecurity):
    """REST Network Mixin"""

    async def get_rtmp_url(self, channel: int = 0, stream: StreamTypes = ...):
        url = await super().get_rtmp_url(channel, stream)
        token = self._auth_token
        if token is not None:
            url += f"&token={token}"
        return url
