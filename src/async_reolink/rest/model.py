"""General Models"""

from typing import (
    Callable,
    Final,
    Generic,
    Iterable,
    Protocol,
    TypeVar,
    TypedDict,
    overload,
)
from typing_extensions import LiteralString, Unpack


from async_reolink.api import model, typing

from ._utilities import providers


_LS = TypeVar("_LS", bound=LiteralString)


class _ManglesKeys:

    # __slots__ = ("__prefix", "__suffix")

    def __init__(self, prefix: str = None, suffix: str = None, title=False) -> None:
        super().__init__()
        self.__prefix = prefix
        self.__suffix = suffix
        self.__title = title

    def _mangle_key(self, key: _LS) -> _LS:
        if not self.__prefix and not self.__suffix:
            return key
        if self.__prefix and self.__title:
            key = key[0].capitalize() + key[1:]
        if self.__prefix and self.__suffix:
            return f"{self.__prefix}{key}{self.__suffix}"
        if self.__prefix:
            return f"{self.__prefix}{key}"
        return f"{key}{self.__suffix}"


class SimpleTime(providers.DictProvider[str, any], _ManglesKeys, model.SimpleTime):
    """REST Simple Time"""

    class JSON(TypedDict):
        """JSON"""

        hour: int
        min: int

    class Keys(Protocol):
        """Keys"""

        hour: Final = "hour"
        minute: Final = "min"

        __all__ = (hour, minute)

    __slots__ = ()

    def __init__(
        self,
        value: providers.ProvidedDict[str, any] | None = None,
        prefix: str | None = None,
        suffix: str | None = None,
    ) -> None:
        super().__init__(value)
        _ManglesKeys.__init__(self, prefix, suffix)

    _provided_value: JSON

    @property
    def hour(self):
        _default = 0
        return (
            value.get(self._mangle_key(self.Keys.hour), _default)
            if (value := self._provided_value)
            else _default
        )

    @property
    def minute(self):
        _default = 0
        return (
            value.get(self._mangle_key(self.Keys.minute), _default)
            if (value := self._provided_value)
            else _default
        )

    @property
    def _unmangled(self) -> JSON:
        if not (value := self._provided_value):
            return {}
        return {
            _k: value[_m]
            for _k, _m in ((_k, self._mangle_key(_k)) for _k in self.Keys.__all__)
            if _m in value
        }


class MutableSimpleTime(SimpleTime):
    """REST Mutable Simple Time"""

    __slots__ = ()

    def _get_provided_value(self, create=False):
        if (value := super()._get_provided_value(create)) is not None or not create:
            return value
        value = {}
        self._set_provided_value(value)
        return value

    @SimpleTime.hour.setter
    def hour(self, value):
        self._get_provided_value(True)[self._mangle_key(self.Keys.hour)] = int(value)

    @SimpleTime.minute.setter
    def minute(self, value):
        self._get_provided_value(True)[self._mangle_key(self.Keys.minute)] = int(value)

    def _update(self, **kwargs: Unpack[SimpleTime.JSON]):
        if (value := self._get_provided_value(True)) is None:
            return
        value.update(
            {
                _m: kwargs[_k]
                for _k, _m in ((_k, self._mangle_key(_k)) for _k in self.Keys.__all__)
                if _k in kwargs
            }
        )

    def update(self, value: typing.SimpleTime):
        if isinstance(value, SimpleTime):
            if _d := value._unmangled:
                self._update(**_d)
            return
        try:
            self.hour = value.hour
        except AttributeError:
            pass
        try:
            self.minute = value.minute
        except AttributeError:
            pass


class Time(SimpleTime, model.Time):
    """REST Time"""

    __slots__ = ()

    class JSON(SimpleTime.JSON):
        """JSON"""

        sec: int

    class Keys(SimpleTime.Keys, Protocol):
        """Keys"""

        second: Final = "sec"

        __all__ = SimpleTime.Keys.__all__ + (second,)

    _value: JSON

    @property
    def second(self):
        _default = 0
        return (
            value.get(self._mangle_key(self.Keys.second), _default)
            if (value := self._provided_value)
            else _default
        )


class MutableTime(MutableSimpleTime, Time):
    """REST Mutable Time"""

    __slots__ = ()

    @Time.second.setter
    def second(self, value):
        self._get_provided_value(True)[self._mangle_key(self.Keys.second)] = int(value)

    def update(self, value: typing.Time):
        super().update(value)
        if isinstance(value, Time):
            return
        try:
            self.second = value.second
        except AttributeError:
            pass


class Date(providers.DictProvider[str, any], _ManglesKeys, model.Date):
    """REST Date"""

    class JSON(TypedDict):
        """JSON"""

        year: int
        mon: int
        day: int

    class Keys(Protocol):
        """Keys"""

        year: Final = "year"
        month: Final = "mon"
        day: Final = "day"

        __all__ = (year, month, day)

    __slots__ = ()

    def __init__(
        self,
        value: providers.ProvidedDict[str, any] | None = None,
        prefix: str | None = None,
        suffix: str | None = None,
    ) -> None:
        super().__init__(value)
        _ManglesKeys.__init__(self, prefix, suffix)

    _value: JSON

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
    def day(self):
        if value := self._provided_value:
            return value.get(self.Keys.day, 0)
        return 0

    @property
    def _unmangled(self) -> JSON:
        if not (value := self._provided_value):
            return {}
        return {
            _k: value[_m]
            for _k, _m in ((_k, self._mangle_key(_k)) for _k in self.Keys.__all__)
            if _m in value
        }


class MutableDate(Date):
    """REST Mutable Date"""

    __slots__ = ()

    @Date.year.setter
    def year(self, value):
        self._get_provided_value(True)[self._mangle_key(self.Keys.year)] = int(value)

    @Date.month.setter
    def month(self, value: int):
        self._get_provided_value(True)[self._mangle_key(self.Keys.month)] = int(value)

    @Date.day.setter
    def day(self, value: int):
        self._get_provided_value(True)[self._mangle_key(self.Keys.day)] = int(value)

    def _update(self, **kwargs: Unpack[Date.JSON]):
        if (value := self._get_provided_value(True)) is None:
            return
        value.update(
            {
                _m: kwargs[_k]
                for _k, _m in ((_k, self._mangle_key(_k)) for _k in self.Keys.__all__)
                if _k in kwargs
            }
        )

    def update(self, value: typing.Date):
        if isinstance(value, Date):
            if _d := value._unmangled:
                self._update(**_d)
            return
        try:
            self.year = value.year
        except AttributeError:
            pass
        try:
            self.month = value.month
        except AttributeError:
            pass
        try:
            self.day = value.day
        except AttributeError:
            pass


@Date.register
@Time.register
class DateTime(providers.DictProvider[str, any], _ManglesKeys, model.DateTime):
    """REST DateTime"""

    class JSON(Date.JSON, Time.JSON):
        """JSON"""

    class Keys(Date.Keys, Time.Keys, Protocol):
        """Keys"""

        __all__ = Date.Keys.__all__ + Time.Keys.__all__

    __slots__ = ()

    def __init__(
        self,
        value: providers.ProvidedDict[str, any] | None = None,
        prefix: str | None = None,
        suffix: str | None = None,
    ) -> None:
        super().__init__(value)
        _ManglesKeys.__init__(self, prefix, suffix)

    _value: JSON

    year = MutableDate.year.setter(None)
    month = MutableDate.month.setter(None)
    day = MutableDate.day.setter(None)

    hour = MutableTime.hour.setter(None)
    minute = MutableTime.minute.setter(None)
    second = MutableTime.second.setter(None)

    @property
    def _unmangled(self) -> JSON:
        if not (value := self._provided_value):
            return {}
        return {
            _k: value[_m]
            for _k, _m in ((_k, self._mangle_key(_k)) for _k in self.Keys.__all__)
            if _m in value
        }


@MutableDate.register
@MutableTime.register
class MutableDateTime(DateTime):
    """REST Mutable DateTime"""

    __slots__ = ()

    year = MutableDate.year.setter(MutableDate.year.fset)
    month = MutableDate.month.setter(MutableDate.year.fset)
    day = MutableDate.day.setter(MutableDate.year.fset)
    hour = MutableTime.hour.setter(MutableDate.year.fset)
    minute = MutableTime.minute.setter(MutableDate.year.fset)
    second = MutableTime.second.setter(MutableDate.year.fset)

    def _update(self, **kwargs: Unpack[DateTime.JSON]):
        if (value := self._get_provided_value(True)) is None:
            return
        value.update(
            {
                _m: kwargs[_k]
                for _k, _m in ((_k, self._mangle_key(_k)) for _k in self.Keys.__all__)
                if _k in kwargs
            }
        )

    def update(self, value: typing.DateTime):
        if isinstance(value, DateTime):
            if _d := value._unmangled:
                self._update(**_d)
            return

        MutableDate.update(self, value)
        MutableTime.update(self, value)


T = TypeVar("T")


class MinMaxRange(providers.DictProvider[str, any], _ManglesKeys, Generic[T]):
    """Min/Max values"""

    class JSON(TypedDict):
        """JSON"""

        min: T
        max: T

    class Keys(Protocol):
        """Keys"""

        min: Final = "min"
        max: Final = "max"

    __slots__ = ()

    @overload
    def __init__(
        self: "MinMaxRange[int]",
        value: providers.ProvidedDict[str, any] | None = None,
        prefix: str | None = None,
        suffix: str | None = None,
    ) -> None:
        super().__init__(value)
        _ManglesKeys.__init__(self, prefix, suffix)
        ...

    def __init__(
        self,
        value: providers.ProvidedDict[str, any] | None = None,
        prefix: str | None = None,
        suffix: str | None = None,
    ) -> None:
        super().__init__(value)
        _ManglesKeys.__init__(self, prefix, suffix)

    _provided_value: JSON

    @property
    def min(self) -> T:
        if value := self._provided_value:
            return value.get(self.Keys.min)

    @property
    def max(self) -> T:
        if value := self._provided_value:
            return value.get(self.Keys.max)


class StringRange(providers.DictProvider[str, any]):
    """String Ranges"""

    class JSON(TypedDict):
        """JSON"""

        Len: MinMaxRange[int].JSON

    class Keys(Protocol):
        """Keys"""

        length: Final = "Len"

    __slots__ = ("__prefix", "__suffix")

    def __init__(
        self,
        value: providers.ProvidedDict[str, any] | None = None,
        prefix: str | None = None,
        suffix: str | None = None,
    ) -> None:
        super().__init__(value)
        self.__prefix = prefix
        self.__suffix = suffix

    _provided_value: JSON

    @property
    def length(self):
        """length ranges"""
        return MinMaxRange(
            self._provided_value, self.__prefix, f"{self.Keys.length}{self.__suffix}"
        )
