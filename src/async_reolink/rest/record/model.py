"""REST Record Models"""

from datetime import date
from typing import Callable, Final, Iterable, Protocol, TypedDict
from typing_extensions import Unpack
from async_reolink.api.typing import StreamTypes
from async_reolink.api.record import typing as record_typing

from ...rest.typing import stream_type_str

from .._utilities import providers

from .. import model

# pylint: disable=missing-function-docstring

_DefaultStreamType: Final = StreamTypes.MAIN
_DefaultStreamTypeStr: Final = stream_type_str(_DefaultStreamType)


class Search(providers.DictProvider[str, any], record_typing.Search):
    """REST Search"""

    class JSON(TypedDict):
        """JSON"""

        onlyStatus: int
        streamType: str
        StartTime: model.DateTime.JSON
        EndTime: model.DateTime.JSON

    class Keys(Protocol):
        """Keys"""

        status_only: Final = "onlyStatus"
        stream_type: Final = "streamType"
        start: Final = "StartTime"
        end: Final = "EndTime"

    __slots__ = ()

    _provided_value: JSON

    @property
    def status_only(self):
        return (
            True if (value := self._provided_value) and value.get(self.Keys.status_only) else False
        )

    @property
    def stream_type(self, value: StreamTypes, _: bool):
        if value := self._provided_value:
            return StreamTypes(value.get(self.Keys.stream_type, _DefaultStreamTypeStr))
        return _DefaultStreamType

    def _get_start(self, create=False) -> model.DateTime.JSON:
        return self._get_key_value(self._get_provided_value, self.Keys.start, default=None)

    @property
    def _start(self):
        return self._get_start()

    @property
    def start(self):
        return model.DateTime(self._get_start)

    def _get_end(self, create=False) -> model.DateTime.JSON:
        return self._get_key_value(self._get_provided_value, self.Keys.end, default=None)

    @property
    def _end(self):
        return self._get_end()

    @property
    def end(self):
        return model.DateTime(self._get_end)


class MutableSearch(Search):
    """REST Mutable Search"""

    __slots__ = ()

    def _get_provided_value(self, create=False):
        if (value := super()._get_provided_value(create)) or not create:
            return value
        value = {}
        self._set_provided_value(value)
        return value

    @Search.status_only.setter
    def status_only(self, value):
        self._set_provided_value(True)[self.Keys.status_only] = int(value)

    @Search.stream_type.setter
    def stream_type(self, value):
        self._set_provided_value(True)[self.Keys.stream_type] = stream_type_str(value)

    def _get_start(self, create=False) -> model.DateTime.JSON:
        return self._get_key_value(
            self._get_provided_value,
            self.Keys.start,
            create,
            default=lambda: dict() if create else None,
        )

    @property
    def start(self):
        return model.MutableDateTime(self._get_start)

    @start.setter
    def start(self, value: record_typing.DateTime):
        self.start.update(value)

    def _get_end(self, create=False) -> model.DateTime.JSON:
        return self._get_key_value(
            self._get_provided_value,
            self.Keys.end,
            create,
            default=lambda: dict() if create else None,
        )

    @property
    def end(self):
        return model.MutableDateTime(self._get_end)

    @end.setter
    def end(self, value: record_typing.DateTime):
        self.end.update(value)

    def _update(self, **kwargs: Unpack[Search.JSON]):
        self._get_provided_value(True).update(kwargs)

    def update(self, value: record_typing.Search):
        if isinstance(value, Search):
            if _d := value._provided_value:
                self._update(_d)
            return
        try:
            self.status_only = value.status_only
        except AttributeError:
            pass
        try:
            self.stream_type = value.stream_type
        except AttributeError:
            pass
        try:
            self.start.update(value.start)
        except AttributeError:
            pass
        try:
            self.end.update(value.end)
        except AttributeError:
            pass


class File(providers.DictProvider[str, any], record_typing.File):
    """REST Recording File"""

    class JSON(TypedDict):
        """JSON"""

        frameRate: int
        width: int
        height: int
        name: str
        size: int
        type: str
        start: model.DateTime.JSON
        end: model.DateTime.JSON

    class Keys(Protocol):
        """Keys"""

        frame_rate: Final = "frameRate"
        width: Final = "width"
        height: Final = "height"
        name: Final = "name"
        size: Final = "size"
        type: Final = "type"
        start: Final = Search.Keys.start
        end: Final = Search.Keys.end

    __slots__ = ()

    _provided_value: JSON

    @property
    def frame_rate(self):
        if value := self._provided_value:
            return value.get(self.Keys.frame_rate, 0)
        return 0

    @property
    def width(self):
        if value := self._provided_value:
            return value.get(self.Keys.width, 0)
        return 0

    @property
    def height(self):
        if value := self._provided_value:
            return value.get(self.Keys.height, 0)
        return 0

    @property
    def size(self):
        if value := self._provided_value:
            return value.get(self.Keys.size, 0)
        return 0

    @property
    def name(self):
        if value := self._provided_value:
            return value.get(self.Keys.name, "")
        return ""

    @property
    def type(self):
        if value := self._provided_value:
            return value.get(self.Keys.type, "")
        return ""

    def _get_start(self, create=False) -> model.DateTime.JSON:
        return self._get_key_value(self._get_provided_value, self.Keys.start, default=None)

    @property
    def _start(self):
        return self._get_start()

    @property
    def start(self):
        return model.DateTime(self._get_start)

    def _get_end(self, create=False) -> model.DateTime.JSON:
        return self._get_key_value(self._get_provided_value, self.Keys.end, default=None)

    @property
    def _end(self):
        return self._get_end()

    @property
    def end(self):
        return model.DateTime(self._get_end)


class _SearchStatusTable(providers.ValueProvider[str], Iterable[int]):
    __slots__ = ()

    def __iter__(self):
        if (value := self._provided_value) is None:
            return
        for i, _c in enumerate(value, 1):
            if _c == "1":
                yield i


class SearchStatus(providers.DictProvider[str, any], record_typing.SearchStatus):
    """REST Recodring Search Status"""

    class JSON(TypedDict):
        """JSON"""

        year: int
        mon: int
        table: str

    class Keys(Protocol):
        """Keys"""

        year: Final = "year"
        month: Final = "mon"
        table: Final = "table"

    __slots__ = ()

    _provided_value: JSON

    @property
    def year(self):
        if value := self._provided_value:
            return value.get(self.Keys.year, 0)
        return 0

    @property
    def month(self):
        if value := self._provided_value:
            return value.get(self.Keys.month, 0)
        return 0

    @property
    def _table(self):
        if value := self._provided_value:
            return value.get(self.Keys.table, "")
        return ""

    @property
    def days(self):
        return _SearchStatusTable(lambda _: self._table)

    def __iter__(self):
        year = self.year
        month = self.month
        for _d in self.days:
            yield date(year, month, _d)
