"""REST Record Models"""

from datetime import date
from typing import Callable, Final, Iterable, overload
from async_reolink.api.typing import StreamTypes
from async_reolink.api.record import typing

from ..typing import STR_STREAMTYPES_MAP, STREAMTYPES_STR_MAP, FactoryValue
from .. import model

# pylint: disable=missing-function-docstring

_DEFAULT_STREAMTYPE: Final = StreamTypes.MAIN
_DEFAULT_STREAMTYPE_STR = STREAMTYPES_STR_MAP[_DEFAULT_STREAMTYPE]


class Search(typing.Search):
    """REST Search"""

    __slots__ = ("_factory",)

    def __init__(self, factory: Callable[[], dict]) -> None:
        self._factory = factory

    @property
    def status_only(self):
        if (value := self._factory()) is None:
            return False
        return bool(value.get("onlyStatus", 0))

    @property
    def stream_type(self):
        if (value := self._factory()) is None:
            return _DEFAULT_STREAMTYPE
        return STR_STREAMTYPES_MAP[value.get("streamType", _DEFAULT_STREAMTYPE_STR)]

    def _get_start(self) -> dict:
        if (value := self._factory()) is None:
            return None
        return value.get("StartTime", None)

    @property
    def start(self):
        return model.DateTime(self._get_start)

    def _get_end(self) -> dict:
        if (value := self._factory()) is None:
            return None
        return value.get("EndTime", None)

    @property
    def end(self):
        return model.DateTime(self._get_end)

    def _copy(self):
        if not (_d := self._factory()):
            return None
        _d = _d.copy()
        if _t := self.start._copy():
            _t["StartTime"] = _t
        if _t := self.end._copy():
            _t["EndTime"] = _t

        return _d


class MutableSearch(Search):
    """REST Mutable Search"""

    __slots__ = ()

    def __init__(self, factory: FactoryValue[dict] = None) -> None:
        if factory is None:
            _d: dict = None

            def _factory(create=False):
                if _d is None and create:
                    _d = {}
                return _d

            factory = _factory
        super().__init__(factory)
        self._factory = factory

    @property
    def _value(self):
        return self._factory(True)

    @Search.status_only.setter
    def status_only(self, value):
        self._value["onlyStatus"] = int(bool(value))

    @Search.stream_type.setter
    def stream_type(self, value):
        self._value["streamType"] = STREAMTYPES_STR_MAP[value or _DEFAULT_STREAMTYPE]

    def _get_start(self, create=False) -> dict:
        _key: Final = "StartTime"
        if (value := self._factory(create)) is None:
            return None
        if _key in value or not create:
            return value.get(_key, None)
        return value.setdefault(_key, {})

    @property
    def start(self):
        return model.MutableDateTime(self._get_start)

    @start.setter
    def start(self, value: typing.DateTime):
        self.start.update(value)

    def _get_end(self, create=False) -> dict:
        _key: Final = "EndTime"
        if (value := self._factory(create)) is None:
            return None
        if _key in value or not create:
            return value.get(_key, None)
        return value.setdefault(_key, {})

    @property
    def end(self):
        return model.MutableDateTime(self._get_end)

    @end.setter
    def end(self, value: typing.DateTime):
        self.end.update(value)

    def update(self, value: typing.Search):
        if isinstance(value, Search):
            if (_d := value._copy()) and (_u := self._factory(True)):
                _u.update(_d)
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


class File(typing.File):
    """REST Recording File"""

    __slots__ = ("_factory",)

    def __init__(self, factory: Callable[[], dict]) -> None:
        self._factory = factory

    def _get_start(self) -> dict:
        if (value := self._factory()) is None:
            return None
        return value.get("StartTime", None)

    @property
    def frame_rate(self) -> int:
        if (value := self._factory()) is None:
            return 0
        return value.get("frameRate", 0)

    @property
    def width(self) -> int:
        if (value := self._factory()) is None:
            return 0
        return value.get("width", 0)

    @property
    def height(self) -> int:
        if (value := self._factory()) is None:
            return 0
        return value.get("height", 0)

    @property
    def size(self) -> int:
        if (value := self._factory()) is None:
            return 0
        return value.get("size", 0)

    @property
    def name(self) -> str:
        if (value := self._factory()) is None:
            return 0
        return value.get("name", 0)

    @property
    def type(self) -> str:
        if (value := self._factory()) is None:
            return 0
        return value.get("type", 0)

    @property
    def start(self):
        return model.DateTime(self._get_start)

    def _get_end(self) -> dict:
        if (value := self._factory()) is None:
            return None
        return value.get("EndTime", None)

    @property
    def end(self):
        return model.DateTime(self._get_end)


class _SearchStatusTable(Iterable[int]):
    __slots__ = ("_factory",)

    def __init__(self, factory: Callable[[], dict]) -> None:
        self._factory = factory

    def __iter__(self):
        if (value := self._factory()) is None:
            return
        for i, _c in enumerate(str(value), 1):
            if _c == "1":
                yield i


class SearchStatus(typing.SearchStatus):
    """REST Recodring Search Status"""

    __slots__ = ("_factory",)

    def __init__(self, factory: Callable[[], dict]) -> None:
        self._factory = factory

    @property
    def year(self) -> int:
        if (value := self._factory()) is None:
            return 0
        return value.get("year", 0)

    @property
    def month(self) -> int:
        if (value := self._factory()) is None:
            return 0
        return value.get("mon", 0)

    def _get_table(self) -> str:
        if (value := self._factory()) is None:
            return ""
        return value.get("table", "")

    @property
    def days(self):
        return _SearchStatusTable(self._get_table)

    def __iter__(self):
        year = self.year
        month = self.month
        for _d in self.days:
            yield date(year, month, _d)
