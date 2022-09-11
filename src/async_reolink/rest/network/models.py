"""REST Network Models"""

from typing import Callable
from async_reolink.api.network import typings


from .typings import STR_LINKTYPES_MAP

# pylint: disable=missing-function-docstring


class IPInfo(typings.IPInfo):
    """REST IP Info"""

    __slots__ = ("_factory",)

    def __init__(self, factory: Callable[[], dict]) -> None:
        self._factory = factory

    @property
    def gateway(self) -> str:
        if (value := self._factory()) is None:
            return None
        return value.get("gateway", None)

    @property
    def address(self) -> str:
        if (value := self._factory()) is None:
            return None
        return value.get("ip", None)

    @property
    def mask(self) -> str:
        if (value := self._factory()) is None:
            return None
        return value.get("mask", None)


class LinkInfo(typings.LinkInfo):
    """REST Link Info"""

    __slots__ = ("_factory",)

    def __init__(self, factory: Callable[[], dict]) -> None:
        self._factory = factory

    @property
    def active_link(self) -> str:
        if (value := self._factory()) is None:
            return None
        return value.get("activeLink", None)

    @property
    def mac(self) -> str:
        if (value := self._factory()) is None:
            return None
        return value.get("mac", None)

    @property
    def type(self):
        if (_dict := self._factory()) is None:
            return None
        if (value := _dict.get("type", None)) is None:
            return None
        return STR_LINKTYPES_MAP[value]

    @property
    def ip(self):  # pylint: disable=invalid-name
        def _get():
            if (value := self._factory()) is None:
                return None
            return value.get("static", None)

        return IPInfo(_get)


class ChannelStatus(typings.ChannelStatus):
    """REST Channel Status"""

    __slots__ = ("_factory",)

    def __init__(self, factory: Callable[[], dict]) -> None:
        self._factory = factory

    @property
    def channel_id(self) -> int:
        if (value := self._factory()) is None:
            return None
        return value.get("channel", None)

    @property
    def name(self) -> str:
        if (value := self._factory()) is None:
            return ""
        return value.get("name", "")

    @property
    def online(self) -> bool:
        if (value := self._factory()) is None:
            return 0
        return value.get("online", 0)

    @property
    def type(self) -> str:
        if (value := self._factory()) is None:
            return None
        return value.get("typeInfo", None)


class P2PInfo(typings.P2PInfo):
    """REST P2P Info"""

    __slots__ = ("_factory",)

    def __init__(self, factory: Callable[[], dict]) -> None:
        self._factory = factory

    @property
    def enabled(self) -> bool:
        if (value := self._factory()) is None:
            return 0
        return value.get("enable", 0)

    @property
    def uid(self) -> str:
        if (value := self._factory()) is None:
            return None
        return value.get("uid", None)


class NetworkPort(typings.NetworkPort):
    """REST Network Port"""

    __slots__ = ("_factory", "_prefix")

    def __init__(self, prefix: str, factory: Callable[[], dict]) -> None:
        self._prefix = prefix
        self._factory = factory

    @property
    def value(self) -> int:
        if (value := self._factory()) is None:
            return 0
        return value.get(self._prefix + "Port", 0)

    @property
    def enabled(self) -> bool:
        if (value := self._factory()) is None:
            return 0
        return value.get(self._prefix + "Enable", 0)

    def __bool__(self):
        return bool(self.enabled and self.value)

    def __int__(self):
        return self.value if self.enabled else 0


class NetworkPorts(typings.NetworkPorts):
    """REST Network Ports"""

    __slots__ = ("__value",)

    def __init__(self, factory: Callable[[], dict]) -> None:
        self.__value = factory

    def _factory(self):
        if callable(self.__value):
            return self.__value()
        return self.__value

    @property
    def media(self):
        return NetworkPort("media", self._factory)

    @property
    def http(self):
        return NetworkPort("http", self._factory)

    @property
    def https(self):
        return NetworkPort("https", self._factory)

    @property
    def onvif(self):
        return NetworkPort("onvif", self._factory)

    @property
    def rtsp(self):
        return NetworkPort("rtsp", self._factory)

    @property
    def rtmp(self):
        return NetworkPort("rtmp", self._factory)

    def update(self, value: dict | Callable[[], dict]):
        self.__value = value
