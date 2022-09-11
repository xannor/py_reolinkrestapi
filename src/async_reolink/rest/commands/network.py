"""REST Network Commands"""

from typing import TYPE_CHECKING, Callable, Final, Mapping, TypeGuard, cast
from async_reolink.api.commands import network

from async_reolink.api.typings import StreamTypes
from ..typings import STREAMTYPES_STR_MAP

from ..network import models

from ..commands import (
    _CHANNEL_KEY,
    CommandRequest,
    CommandResponseTypes,
    CommandResponse,
)


# pylint:disable=missing-function-docstring
# pylint: disable=too-few-public-methods


class GetLocalLinkRequest(CommandRequest, network.GetLocalLinkRequest):
    """REST Get Local Link Request"""

    __slots__ = ()

    COMMAND: Final = "GetLocalLink"

    def __init__(
        self, response_type: CommandResponseTypes = CommandResponseTypes.VALUE_ONLY
    ) -> None:
        super().__init__()
        self.command = type(self).COMMAND
        self.response_type = response_type


class GetLocalLinkResponse(
    CommandResponse, network.GetLocalLinkResponse, test="is_response"
):
    """REST Get Local Link Response"""

    __slots__ = ()

    @classmethod
    def is_response(  # pylint: disable=signature-differs
        cls, value: any, /
    ) -> TypeGuard["GetLocalLinkResponse"]:
        return super().is_response(value, GetLocalLinkRequest.COMMAND)

    def _local_link(self) -> dict:
        return (
            value.get("LocalLink", None)
            if (value := self._get_value()) is not None
            else None
        )

    @property
    def local_link(self):
        return models.LinkInfo(self._local_link)


class GetChannelStatusRequest(CommandRequest, network.GetChannelStatusRequest):
    """REST Get Channel Status Request"""

    __slots__ = ()

    COMMAND: Final = "GetChannelstatus"

    def __init__(
        self, response_type: CommandResponseTypes = CommandResponseTypes.VALUE_ONLY
    ) -> None:
        super().__init__()
        self.command = type(self).COMMAND
        self.response_type = response_type


class _ChannelStatuses(Mapping[int, models.ChannelStatus]):
    __slots__ = ("__value",)

    def __init__(self, factory: Callable[[], dict]) -> None:
        super().__init__()
        self.__value = factory

    def _factory(self):
        if callable(self.__value):
            return self.__value()
        return self.__value

    def _get_channels(self) -> list:
        return (
            value.get("status", None)
            if (value := self._factory()) is not None
            else None
        )

    def _channel_getter(self, channel_id: int):
        # TODO : verify that channel_id == index

        def _factory() -> dict:
            return (
                channels[channel_id]
                if (channels := self._get_channels()) is not None
                else None
            )

        return _factory

    def __getitem__(self, __k: int):
        return models.ChannelStatus(self._channel_getter(__k))

    def __iter__(self):
        if (channels := self._get_channels()) is None:
            return
        for _d in channels:
            if TYPE_CHECKING:
                _d = cast(dict, _d)
            if (channel := _d.get("channel", None)) is not None:
                if TYPE_CHECKING:
                    channel = cast(int, channel)
                yield channel

    def __len__(self) -> int:
        if (value := self._factory()) is None:
            return 0
        return value.get("count", 0)


class GetChannelStatusResponse(
    CommandResponse, network.GetChannelStatusResponse, test="is_response"
):
    """REST Get Channel Status Response"""

    __slots__ = ()

    @classmethod
    def is_response(  # pylint: disable=signature-differs
        cls, value: any, /
    ) -> TypeGuard["GetChannelStatusResponse"]:
        return super().is_response(value, GetChannelStatusRequest.COMMAND)

    @property
    def channels(self):
        return _ChannelStatuses(self._get_value)


class GetNetworkPortsRequest(CommandRequest, network.GetNetworkPortsRequest):
    """REST Get Network Ports"""

    __slots__ = ()

    COMMAND: Final = "GetNetPort"

    def __init__(
        self, response_type: CommandResponseTypes = CommandResponseTypes.VALUE_ONLY
    ) -> None:
        super().__init__()
        self.command = type(self).COMMAND
        self.response_type = response_type


class GetNetworkPortsResponse(
    CommandResponse, network.GetLocalLinkResponse, test="is_response"
):
    """REST Get Local Link Response"""

    __slots__ = ()

    @classmethod
    def is_response(  # pylint: disable=signature-differs
        cls, value: any, /
    ) -> TypeGuard["GetNetworkPortsResponse"]:
        return super().is_response(value, GetNetworkPortsRequest.COMMAND)

    def _get_ports(self) -> dict:
        return (
            value.get("NetPort", None)
            if (value := self._get_value()) is not None
            else None
        )

    @property
    def ports(self):
        return models.NetworkPorts(self._get_ports)


class GetRTSPUrlsRequest(CommandRequest, network.GetRTSPUrlsRequest):
    """REST Get RTSP Urls Request"""

    __slots__ = ()

    COMMAND: Final = "GetRtspUrl"

    def __init__(
        self,
        channel_id: int = 0,
        response_type: CommandResponseTypes = CommandResponseTypes.VALUE_ONLY,
    ) -> None:
        super().__init__()
        self.command = type(self).COMMAND
        self.response_type = response_type
        self.channel_id = channel_id


class _RTSPUrls(Mapping[StreamTypes, str]):
    __slots__ = ("_factory",)

    def __init__(self, factory: Callable[[], dict]) -> None:
        self._factory = factory

    def __getitem__(self, __k: StreamTypes) -> str:
        if (value := self._factory()) is None:
            return None
        return value.get(STREAMTYPES_STR_MAP[__k] + "Stream", None)

    def __contains__(self, __o: StreamTypes) -> bool:
        if (value := self._factory()) is None:
            return False
        return STREAMTYPES_STR_MAP[__o] + "Stream" in value

    def __iter__(self):
        if (value := self._factory()) is None:
            return
        for _k, _v in STREAMTYPES_STR_MAP.items():
            if _v + "Stream" in value:
                yield _k

    def __len__(self) -> int:
        if (value := self._factory()) is None:
            return 0
        return len(
            (True for _v in STREAMTYPES_STR_MAP.values() if _v + "Stream" in value)
        )


class GetRTSPUrlsResponse(
    CommandResponse, network.GetRTSPUrlsResponse, test="is_response"
):
    """REST Get RTSP Urls Response"""

    __slots__ = ()

    @classmethod
    def is_response(  # pylint: disable=signature-differs
        cls, value: any, /
    ) -> TypeGuard["GetRTSPUrlsResponse"]:
        return super().is_response(value, GetRTSPUrlsRequest.COMMAND)

    def _get_urls(self) -> dict:
        return (
            value.get("rtspUrl", None)
            if (value := self._get_value()) is not None
            else None
        )

    @property
    def channel_id(self) -> int:
        return (
            value.get(_CHANNEL_KEY, 0) if (value := self._get_urls()) is not None else 0
        )

    @property
    def urls(self):
        return _RTSPUrls(self._get_urls)


class GetP2PRequest(CommandRequest, network.GetP2PRequest):
    """REST Get Local Link Request"""

    __slots__ = ()

    COMMAND: Final = "GetP2p"

    def __init__(
        self, response_type: CommandResponseTypes = CommandResponseTypes.VALUE_ONLY
    ) -> None:
        super().__init__()
        self.command = type(self).COMMAND
        self.response_type = response_type


class GetP2PResponse(CommandResponse, network.GetP2PResponse, test="is_response"):
    """REST Get P2P Response"""

    __slots__ = ()

    @classmethod
    def is_response(  # pylint: disable=signature-differs
        cls, value: any, /
    ) -> TypeGuard["GetP2PResponse"]:
        return super().is_response(value, GetP2PRequest.COMMAND)

    def _get_info(self) -> dict:
        return (
            value.get("P2p", None) if (value := self._get_value()) is not None else None
        )

    @property
    def info(self):
        return models.P2PInfo(self._get_info)
