"""General Models"""

from typing import (
    Final,
    Generic,
    Protocol,
    TypeAlias,
    TypedDict,
    overload,
)
from typing_extensions import LiteralString, Unpack, TypeVar


from async_reolink.api import model, typing

from ._utilities.providers import value as providers, mangle


_LS = TypeVar("_LS", bound=LiteralString)

_JSONDict: TypeAlias = dict[str, any]


class SimpleTime(providers.Value[_JSONDict], model.SimpleTime):
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

    __slots__ = ("_mangle_key",)

    def __init__(
        self,
        value: providers.FactoryValue[_JSONDict] | _JSONDict | None = ...,
        /,
        **kwargs: Unpack[mangle.mangler_kwargs],
    ) -> None:
        super().__init__(value, **{k: kwargs[k] for k in kwargs if k not in mangle.mangler_kwkeys})
        self._mangle_key = mangle.mangler(**kwargs)

    __get_value__: providers.FactoryValue[JSON]

    @property
    def hour(self):
        _default = 0
        return (
            value.get(self._mangle_key(self.Keys.hour), _default)
            if (value := self.__get_value__())
            else _default
        )

    @property
    def minute(self):
        _default = 0
        return (
            value.get(self._mangle_key(self.Keys.minute), _default)
            if (value := self.__get_value__())
            else _default
        )

    @property
    def _unmangled(self) -> JSON:
        if not (value := self.__get_value__()):
            return {}
        return {
            _k: value[_m]
            for _k, _m in ((_k, self._mangle_key(_k)) for _k in self.Keys.__all__)
            if _m in value
        }


class MutableSimpleTime(SimpleTime):
    """REST Mutable Simple Time"""

    __slots__ = ()

    def __default_factory__(self, create=False):
        if not create:
            return None
        value = {}
        if self is not None and not isinstance(self, type):
            self.__set_value__(value)
        return value

    @SimpleTime.hour.setter
    def hour(self, value):
        self.__get_value__(True)[self._mangle_key(self.Keys.hour)] = int(value)

    @SimpleTime.minute.setter
    def minute(self, value):
        self.__get_value__(True)[self._mangle_key(self.Keys.minute)] = int(value)

    def _update(self, **kwargs: Unpack[SimpleTime.JSON]):
        if (value := self.__get_value__(True)) is None:
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

    __get_value__: providers.FactoryValue[JSON]

    @property
    def second(self):
        _default = 0
        return (
            value.get(self._mangle_key(self.Keys.second), _default)
            if (value := self.__get_value__())
            else _default
        )


class MutableTime(MutableSimpleTime, Time):
    """REST Mutable Time"""

    __slots__ = ()

    @Time.second.setter
    def second(self, value):
        self.__get_value__(True)[self._mangle_key(self.Keys.second)] = int(value)

    def update(self, value: typing.Time):
        super().update(value)
        if isinstance(value, Time):
            return
        try:
            self.second = value.second
        except AttributeError:
            pass


class Date(providers.Value[_JSONDict], model.Date):
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

    __slots__ = ("_mangle_key",)

    def __init__(
        self,
        value: providers.FactoryValue[_JSONDict] | _JSONDict | None = ...,
        /,
        **kwargs: Unpack[mangle.mangler_kwargs],
    ) -> None:
        super().__init__(value, **{k: kwargs[k] for k in kwargs if k not in mangle.mangler_kwkeys})
        self._mangle_key = mangle.mangler(**kwargs)

    __get_value__: providers.FactoryValue[JSON]

    @property
    def year(self):
        _default = 0
        return (
            value.get(self._mangle_key(self.Keys.year), _default)
            if (value := self.__get_value__())
            else _default
        )

    @property
    def month(self):
        _default = 0
        return (
            value.get(self._mangle_key(self.Keys.month), _default)
            if (value := self.__get_value__())
            else _default
        )

    @property
    def day(self):
        _default = 0
        return (
            value.get(self._mangle_key(self.Keys.day), _default)
            if (value := self.__get_value__())
            else _default
        )

    @property
    def _unmangled(self) -> JSON:
        if not (value := self.__get_value__()):
            return {}
        return {
            _k: value[_m]
            for _k, _m in ((_k, self._mangle_key(_k)) for _k in self.Keys.__all__)
            if _m in value
        }


class MutableDate(Date):
    """REST Mutable Date"""

    __slots__ = ()

    def __default_factory__(self, create=False):
        if not create:
            return None
        value = {}
        if self is not None and not isinstance(self, type):
            self.__set_value__(value)
        return value

    @Date.year.setter
    def year(self, value):
        self.__get_value__(True)[self._mangle_key(self.Keys.year)] = int(value)

    @Date.month.setter
    def month(self, value: int):
        self.__get_value__(True)[self._mangle_key(self.Keys.month)] = int(value)

    @Date.day.setter
    def day(self, value: int):
        self.__get_value__(True)[self._mangle_key(self.Keys.day)] = int(value)

    def _update(self, **kwargs: Unpack[Date.JSON]):
        if (value := self.__get_value__(True)) is None:
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
class DateTime(providers.Value[_JSONDict], model.DateTime):
    """REST DateTime"""

    class JSON(Date.JSON, Time.JSON):
        """JSON"""

    class Keys(Date.Keys, Time.Keys, Protocol):
        """Keys"""

        __all__ = Date.Keys.__all__ + Time.Keys.__all__

    __slots__ = ("_mangle_key",)

    def __init__(
        self,
        value: providers.FactoryValue[_JSONDict] | _JSONDict | None = ...,
        /,
        **kwargs: Unpack[mangle.mangler_kwargs],
    ) -> None:
        super().__init__(value, **{k: kwargs[k] for k in kwargs if k not in mangle.mangler_kwkeys})
        self._mangle_key = mangle.mangler(**kwargs)

    __get_value__: providers.FactoryValue[JSON]

    year = MutableDate.year.setter(None)
    month = MutableDate.month.setter(None)
    day = MutableDate.day.setter(None)

    hour = MutableTime.hour.setter(None)
    minute = MutableTime.minute.setter(None)
    second = MutableTime.second.setter(None)

    @property
    def _unmangled(self) -> JSON:
        if not (value := self.__get_value__()):
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

    def __default_factory__(self, create=False):
        if not create:
            return None
        value = {}
        if self is not None and not isinstance(self, type):
            self.__set_value__(value)
        return value

    year = MutableDate.year.setter(MutableDate.year.fset)
    month = MutableDate.month.setter(MutableDate.year.fset)
    day = MutableDate.day.setter(MutableDate.year.fset)
    hour = MutableTime.hour.setter(MutableDate.year.fset)
    minute = MutableTime.minute.setter(MutableDate.year.fset)
    second = MutableTime.second.setter(MutableDate.year.fset)

    def _update(self, **kwargs: Unpack[DateTime.JSON]):
        if (value := self.__get_value__(True)) is None:
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


T = TypeVar("T", default=int)


class MinMaxRange(providers.Value[_JSONDict], Generic[T]):
    """Min/Max values"""

    class JSON(TypedDict):
        """JSON"""

        min: T
        max: T

    class Keys(Protocol):
        """Keys"""

        min: Final = "min"
        max: Final = "max"

    __slots__ = ("_mangle_key",)

    __get_value__: providers.FactoryValue[JSON]

    def __init__(
        self,
        value: providers.FactoryValue[_JSONDict] | _JSONDict | None = ...,
        /,
        **kwargs: Unpack[mangle.mangler_kwargs],
    ) -> None:
        super().__init__(value, **{k: kwargs[k] for k in kwargs if k not in mangle.mangler_kwkeys})
        self._mangle_key = mangle.mangler(**kwargs)

    @property
    def min(self) -> T:
        if value := self.__get_value__():
            return value.get(self._mangle_key(self.Keys.min))

    @property
    def max(self) -> T:
        if value := self.__get_value__():
            return value.get(self._mangle_key(self.Keys.max))


class StringRange(providers.Value[_JSONDict]):
    """String Ranges"""

    class JSON(TypedDict):
        """JSON"""

        Len: MinMaxRange[int].JSON

    class Keys(Protocol):
        """Keys"""

        length: Final = "Len"

    __slots__ = ("__prefix", "__suffix")

    __get_value__: providers.FactoryValue[JSON]

    def __init__(
        self,
        value: providers.FactoryValue[_JSONDict] | _JSONDict | None = ...,
        /,
        prefix: str | None = None,
        suffix: str | None = None,
        **kwargs: any,
    ) -> None:
        super().__init__(value, **kwargs)
        self.__prefix = prefix
        self.__suffix = suffix or ""

    __get_value__: providers.FactoryValue[JSON]

    @property
    def length(self):
        """length ranges"""
        return MinMaxRange(
            self.__get_value__,
            prefix=self.__prefix,
            suffix=f"{self.Keys.length}{self.__suffix}",
        )
