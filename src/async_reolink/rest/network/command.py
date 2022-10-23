"""REST Network Commands"""

from typing import TYPE_CHECKING, Callable, Final, Mapping, TypeGuard
from async_reolink.api.network import command as network
from async_reolink.api.connection.typing import CommandResponse

from async_reolink.api.typing import StreamTypes
from ..typing import STREAMTYPES_STR_MAP
from ..models import MinMaxRange

from . import models

from ..connection.models import (
    _CHANNEL_KEY,
    CommandRequest,
    CommandResponseTypes,
    CommandResponse as RestCommandResponse,
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
    RestCommandResponse, network.GetLocalLinkResponse, test="is_response"
):
    """REST Get Local Link Response"""

    __slots__ = ()

    @classmethod
    def is_response(cls, value: any, /):  # pylint: disable=signature-differs
        return super().is_response(value, GetLocalLinkRequest.COMMAND)

    def _local_link(self) -> dict:
        return (
            value.get("LocalLink", None)
            if (value := self._get_value()) is not None
            else None
        )

    @property
    def local_link(self):
        # we are not passing the factory here since this object is meant to be detachable
        return models.LinkInfo(self._local_link())


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


class GetChannelStatusResponse(
    RestCommandResponse, network.GetChannelStatusResponse, test="is_response"
):
    """REST Get Channel Status Response"""

    __slots__ = ()

    @classmethod
    def is_response(cls, value: any, /):  # pylint: disable=signature-differs
        return super().is_response(value, GetChannelStatusRequest.COMMAND)

    @property
    def channels(self):
        # we are not passing the factory here since this object is meant to be detachable
        return models.ChannelStatuses(self._get_value())


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
    RestCommandResponse, network.GetNetworkPortsResponse, test="is_response"
):
    """REST Get Local Link Response"""

    __slots__ = ()

    @classmethod
    def is_response(cls, value: any, /):  # pylint: disable=signature-differs
        return super().is_response(value, GetNetworkPortsRequest.COMMAND)

    def _get_ports(self) -> dict:
        return (
            value.get("NetPort", None)
            if (value := self._get_value()) is not None
            else None
        )

    @property
    def ports(self):
        # we are not passing the factory here since this object is meant to be detachable
        return models.NetworkPorts(self._get_ports())


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
    __slots__ = ("_value",)

    def __init__(self, value: dict) -> None:
        self._value = value

    def _factory(self):
        return self._value

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
    RestCommandResponse, network.GetRTSPUrlsResponse, test="is_response"
):
    """REST Get RTSP Urls Response"""

    __slots__ = ()

    @classmethod
    def is_response(cls, value: any, /):  # pylint: disable=signature-differs
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
        # we are not passing the factory here since this object is meant to be detachable
        return _RTSPUrls(self._get_urls())


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


class GetP2PResponse(RestCommandResponse, network.GetP2PResponse, test="is_response"):
    """REST Get P2P Response"""

    __slots__ = ()

    @classmethod
    def is_response(cls, value: any, /):  # pylint: disable=signature-differs
        return super().is_response(value, GetP2PRequest.COMMAND)

    def _get_info(self) -> dict:
        return (
            value.get("P2p", None) if (value := self._get_value()) is not None else None
        )

    @property
    def info(self):
        # we are not passing the factory here since this object is meant to be detachable
        return models.P2PInfo(self._get_info())


class GetWifiInfoRequest(CommandRequest, network.GetWifiInfoRequest):
    """REST Get Wifi Info Request"""

    __slots__ = ()

    COMMAND: Final = "GetWifi"

    def __init__(
        self, response_type: CommandResponseTypes = CommandResponseTypes.VALUE_ONLY
    ) -> None:
        super().__init__()
        self.command = type(self).COMMAND
        self.response_type = response_type


class GetWifiInfoResponse(
    RestCommandResponse, network.GetWifiInfoResponse, test="is_request"
):
    """REST Get Wifi Info Response"""

    __slots__ = ()

    @classmethod
    def is_response(cls, value: any, /):  # pylint: disable=signature-differs
        return super().is_response(value, GetWifiInfoRequest.COMMAND)

    def _get_info(self) -> dict:
        return (
            value.get("Wifi", None)
            if (value := self._get_value()) is not None
            else None
        )

    @property
    def info(self):
        # we are not passing the factory here since this object is meant to be detachable
        return models.WifiInfo(self._get_info())


class GetWifiSignalRequest(CommandRequest, network.GetWifiSignalRequest):
    """REST Get Signal Strength Request"""

    __slots__ = ()

    COMMAND: Final = "GetWifiSignal"

    def __init__(
        self, response_type: CommandResponseTypes = CommandResponseTypes.VALUE_ONLY
    ) -> None:
        super().__init__()
        self.command = type(self).COMMAND
        self.response_type = response_type


_SIGNAL_KEY: Final = "wifiSignal"


class GetWifiSignalResponse(
    RestCommandResponse, network.GetWifiSignalResponse, test="is_request"
):
    """REST Get Wifi Signal Strength Response"""

    __slots__ = ()

    @classmethod
    def is_response(cls, value: any, /):  # pylint: disable=signature-differs
        return super().is_response(value, GetWifiSignalRequest.COMMAND)

    def _get_info(self, factory: Callable[[], dict]):
        def _factory() -> dict:
            return (
                value.get("WifiSignal", None)
                if (value := factory()) is not None
                else None
            )

        return _factory

    @property
    def signal(self) -> int:
        if (value := self._get_value()) is None:
            return 0
        return value.get(_SIGNAL_KEY, 0)

    @property
    def initial_signal(self) -> int | None:
        if (value := self._get_initial()) is None:
            return None
        return value.get(_SIGNAL_KEY, 0)

    @property
    def signal_range(self):
        if (value := self._get_range()) is None:
            return None

        def _factory():
            return value

        return MinMaxRange("", _factory)


class CommandFactory(network.CommandFactory):
    """REST Network Command Factory"""

    def create_get_local_link_request(self):
        return GetLocalLinkRequest()

    def is_get_local_link_response(
        self, response: CommandResponse
    ) -> TypeGuard[GetLocalLinkResponse]:
        return isinstance(response, GetLocalLinkResponse)

    def create_get_channel_status_request(self):
        return GetChannelStatusRequest()

    def is_get_channel_status_response(
        self, response: CommandResponse
    ) -> TypeGuard[GetChannelStatusResponse]:
        return isinstance(response, GetChannelStatusResponse)

    def create_get_ports_request(self):
        return GetNetworkPortsRequest()

    def is_get_ports_response(
        self, response: CommandResponse
    ) -> TypeGuard[GetNetworkPortsResponse]:
        return isinstance(response, GetNetworkPortsResponse)

    def create_get_rtsp_urls_request(self, channel_id: int):
        return GetRTSPUrlsRequest(channel_id)

    def is_get_rtsp_urls_response(
        self, response: CommandResponse
    ) -> TypeGuard[GetRTSPUrlsResponse]:
        return isinstance(response, GetRTSPUrlsResponse)

    def create_get_p2p_request(self):
        return GetP2PRequest()

    def is_get_p2p_response(
        self, response: CommandResponse
    ) -> TypeGuard[GetP2PResponse]:
        return isinstance(response, GetP2PResponse)

    def create_get_wifi_info_request(self):
        return GetWifiInfoRequest()

    def is_get_wifi_info_response(
        self, response: CommandResponse
    ) -> TypeGuard[GetWifiInfoResponse]:
        return isinstance(response, GetWifiInfoResponse)

    def create_get_wifi_signal_request(self):
        return GetWifiSignalRequest()

    def is_get_wifi_signal_response(
        self, response: CommandResponse
    ) -> TypeGuard[GetWifiSignalResponse]:
        return isinstance(response, GetWifiSignalResponse)
