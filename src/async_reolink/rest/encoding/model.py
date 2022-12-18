"""Encoding REST models"""

from typing import Callable, Final, Mapping, Protocol, TypedDict
from async_reolink.api.typing import StreamTypes
from async_reolink.api.encoding import typing as encoding_typing

from .._utilities import providers

from .. import model

from ..encoding.typing import stream_types_str

# pylint:disable=missing-function-docstring


class StreamEncodingInfo(providers.DictProvider[str, any], encoding_typing.StreamEncodingInfo):
    """REST Stream Encoding Info"""

    class JSON(TypedDict):
        """JSON"""

        bitRate: int
        frameRate: int
        gop: int
        height: int
        width: int
        profile: str
        size: str
        video_type: str

    class Keys(Protocol):
        """Keys"""

        bit_rate: Final = "bitRate"
        frame_rate: Final = "frameRate"
        gop: Final = "gop"
        height: Final = "height"
        width: Final = "width"
        profile: Final = "profile"
        size: Final = "size"
        video_type: Final = "video_type"

    _provided_value: JSON

    @property
    def bit_rate(self):
        if value := self._provided_value:
            return value.get(self.Keys.bit_rate, 0)
        return 0

    @property
    def frame_rate(self):
        if value := self._provided_value:
            return value.get(self.Keys.frame_rate, 0)
        return 0

    @property
    def gop(self):
        if value := self._provided_value:
            return value.get(self.Keys.gop, 0)
        return 0

    @property
    def height(self):
        if value := self._provided_value:
            return value.get(self.Keys.height, 0)
        return 0

    @property
    def width(self):
        if value := self._provided_value:
            return value.get(self.Keys.width, 0)
        return 0

    @property
    def profile(self):
        if value := self._provided_value:
            return value.get(self.Keys.profile, "")
        return ""

    @property
    def size(self):
        if value := self._provided_value:
            return value.get(self.Keys.size, "")
        return ""

    @property
    def video_type(self):
        if value := self._provided_value:
            return value.get(self.Keys.video_type, "")
        return ""


class _StreamMapping(providers.DictProvider[str, any], Mapping[StreamTypes, StreamEncodingInfo]):
    __slots__ = ()

    def __getitem__(self, __k: StreamTypes):
        def _get():
            if __value := self._provided_value:
                return __value.get(stream_types_str(__k), None)
            return None

        return StreamEncodingInfo(_get)

    def __iter__(self):
        if not (__value := self._provided_value):
            return

        for __k in StreamTypes:
            if stream_types_str(__k) in __value:
                yield __k

    def __len__(self):
        if __value := self._provided_value:
            return len(stream_types_str() & __value.keys())
        return 0


class EncodingInfo(providers.DictProvider[str, any], encoding_typing.EncodingInfo):
    """REST Encoding Info"""

    class JSON(TypedDict):
        """JSON"""

        audio: int

    class Keys(Protocol):
        """Keys"""

        audio: Final = "audio"

    _provided_value: JSON | dict[str, any]

    @property
    def audio(self):
        return True if (value := self._provided_value) and value.get(self.Keys.audio) else False

    @property
    def stream(self):
        """stream"""

        return _StreamMapping(self._get_value)
