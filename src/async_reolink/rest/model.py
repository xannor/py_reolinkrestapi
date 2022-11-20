"""General Models"""

from typing import Callable, Final, Generic, TypeVar, overload

from async_reolink.api import model, typing

from .typing import FactoryValue

T = TypeVar("T")


class _Factory:

    __slots__ = ("_factory",)

    def __init__(self, factory: Callable[[], dict]) -> None:
        self._factory = factory


class SimpleTime(_Factory, model.SimpleTime):
    """REST Simple Time"""

    _HOUR_KEY: Final = "Hour"
    _MIN_KEY: Final = "Min"

    __slots__ = ("_hour_key", "_min_key")

    def __init__(self, factory: Callable[[], dict], prefix: str = None, suffix: str = None) -> None:
        super().__init__(factory)
        self.__post_init__(prefix, suffix)

    def __post_init__(self, prefix: str = None, suffix: str = None):
        self._hour_key = f"{prefix or ''}{self._HOUR_KEY}{suffix or ''}"
        self._min_key = f"{prefix or ''}{self._MIN_KEY}{suffix or ''}"

    @property
    def hour(self) -> int:
        if (value := self._factory()) is None:
            return 0
        return value.get(self._hour_key, 0)

    @property
    def minute(self) -> int:
        if (value := self._factory()) is None:
            return 0
        return value.get(self._min_key, 0)

    def _copy(self):
        if not (_d := self._factory()):
            return None
        return {key: value for key, value in _d.items() if key in (self._hour_key, self._min_key)}


class _MutableFactory(_Factory):
    def __init__(self, factory: FactoryValue[dict] = None) -> None:
        super().__init__(None)
        self._factory = factory
        if factory is None:
            _d = None

            def _factory(create=False):
                if not _d and create:
                    _d = {}
                return _d

            self._factory: FactoryValue[dict] = _factory
        else:
            self._factory = factory


class MutableSimpleTime(_MutableFactory, SimpleTime):
    """REST Mutable Simple Time"""

    def __init__(
        self, factory: FactoryValue[dict] = None, prefix: str = None, suffix: str = None
    ) -> None:
        SimpleTime.__init__(self, None, prefix, suffix)
        _MutableFactory.__init__(self, factory)

    @SimpleTime.hour.setter
    def hour(self, value):
        if (value := self._factory(True)) is not None:
            value[self._hour_key] = value

    @SimpleTime.minute.setter
    def minute(self, value):
        if (value := self._factory(True)) is not None:
            value[self._min_key] = value

    def update(self, value: typing.SimpleTime):
        if isinstance(value, SimpleTime):
            if (_d := value._copy()) and (_u := self._factory(True)):
                # filter keys since this could be a partial child object
                _u.update(_d)
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

    _SEC_KEY: Final = "Sec"

    __slots__ = ("_sec_key",)

    def __init__(self, factory: Callable[[], dict], prefix: str = None, suffix: str = None) -> None:
        super().__init__(factory, prefix, suffix)
        self.__post_init__(prefix, suffix)

    def __post_init__(self, prefix: str = None, suffix: str = None):
        super().__post_init__(prefix, suffix)
        self._sec_key = f"{prefix or ''}{self._SEC_KEY}{suffix or ''}"

    @property
    def second(self) -> int:
        if (value := self._factory()) is None:
            return 0
        return value.get(self._sec_key, 0)

    def _copy(self):
        if not (_d := self._factory()):
            return None
        return {
            key: value
            for key, value in _d.items()
            if key in (self._hour_key, self._min_key, self._sec_key)
        }


class MutableTime(MutableSimpleTime, Time):
    """REST Mutable Time"""

    def __init__(
        self, factory: FactoryValue[dict] = None, prefix: str = None, suffix: str = None
    ) -> None:
        super().__init__(factory, prefix, suffix)

    @Time.second.setter
    def second(self, value):
        if (value := self._factory(True)) is not None:
            value[self._sec_key] = value

    def update(self, value: typing.Time):
        if isinstance(value, Time):
            if (_d := value._copy()) and (_u := self._factory(True)):
                # filter keys since this could be a partial child object
                _u.update(_d)
            return
        super().update(value)
        try:
            self.second = value.second
        except AttributeError:
            pass


class Date(_Factory, model.Date):
    """REST Date"""

    _YEAR_KEY: Final = "Year"
    _MON_KEY: Final = "Mon"
    _DAY_KEY: Final = "Day"

    __slots__ = ("_year_key", "_mon_key", "_day_key")

    def __init__(self, factory: Callable[[], dict], prefix: str = None, suffix: str = None) -> None:
        super().__init__(factory)
        self.__post_init__(prefix, suffix)

    def __post_init__(self, prefix: str = None, suffix: str = None):
        self._year_key = f"{prefix or ''}{self._YEAR_KEY}{suffix or ''}"
        self._mon_key = f"{prefix or ''}{self._MON_KEY}{suffix or ''}"
        self._day_key = f"{prefix or ''}{self._DAY_KEY}{suffix or ''}"

    @property
    def year(self) -> int:
        if (value := self._factory()) is None:
            return 0
        return value.get(self._year_key, 0)

    @property
    def month(self) -> int:
        if (value := self._factory()) is None:
            return 0
        return value.get(self._mon_key, 0)

    @property
    def day(self) -> int:
        if (value := self._factory()) is None:
            return 0
        return value.get(self._day_key, 0)

    def _copy(self):
        if not (_d := self._factory()):
            return None
        return {
            key: value
            for key, value in _d.items()
            if key in (self._year_key, self._mon_key, self._day_key)
        }


class MutableDate(_MutableFactory, Date):
    """REST Mutable Date"""

    __slots__ = ()

    def __init__(
        self, factory: FactoryValue[dict] = None, prefix: str = None, suffix: str = None
    ) -> None:
        Date.__init__(self, None, prefix, suffix)
        _MutableFactory.__init__(self, factory)

    @Date.year.setter
    def year(self, value):
        if (value := self._factory(True)) is not None:
            value[self._year_key] = value

    @Date.month.setter
    def month(self, value):
        if (value := self._factory(True)) is not None:
            value[self._mon_key] = value

    @Date.day.setter
    def day(self, value):
        if (value := self._factory(True)) is not None:
            value[self._day_key] = value

    def update(self, value: typing.Date):
        if isinstance(value, Date):
            if (_d := value._copy()) and (_u := self._factory(True)):
                # filter keys since this could be a partial child object
                _u.update(_d)
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
class DateTime(_Factory, model.DateTime):
    """REST DateTime"""

    __slots__ = Date.__slots__ + Time.__slots__ + SimpleTime.__slots__

    def __init__(self, factory: Callable[[], dict], prefix: str = None, suffix: str = None) -> None:
        super().__init__(factory)
        Date.__post_init__(self, prefix, suffix)
        Time.__post_init__(self, prefix, suffix)

    @property
    def year(self):
        return Date.year.fget(self)

    @property
    def month(self):
        return Date.month.fget(self)

    @property
    def day(self):
        return Date.day.fget(self)

    @property
    def hour(self):
        return Time.hour.fget(self)

    @property
    def minute(self):
        return Time.minute.fget(self)

    @property
    def second(self):
        return Time.second.fget(self)

    def _copy(self):
        _d = Date._copy(self)
        _t = Time._copy(self)
        if not _d and not _t:
            return None
        if _d and _t:
            _d.update(_t)
        if _d:
            return _d
        return _t


@MutableDate.register
@MutableTime.register
class MutableDateTime(DateTime):
    """REST Mutable DateTime"""

    __slots__ = ()

    def __init__(
        self, factory: FactoryValue[dict] = None, prefix: str = None, suffix: str = None
    ) -> None:
        super().__init__(factory, prefix, suffix)

    year = DateTime.year.setter(MutableDate.year.fset)
    month = DateTime.month.setter(MutableDate.month.fset)
    day = DateTime.day.setter(MutableDate.day.fset)
    hour = DateTime.hour.setter(MutableTime.hour.fset)
    minute = DateTime.minute.setter(MutableTime.minute.fset)
    second = DateTime.second.setter(MutableTime.second.fset)

    def update(self, value: typing.DateTime):
        if isinstance(value, DateTime):
            if (_d := value._copy()) and (_u := self._factory(True)):
                _u.update(_d)
            return
        MutableDate.update(self, value)
        MutableTime.update(self, value)


class MinMaxRange(Generic[T]):
    """Min/Max values"""

    __slots__ = ("_suffix", "_factory")

    @overload
    def __init__(self: "MinMaxRange[int]", suffix: str, factory: Callable[[], dict]):
        ...

    def __init__(self, suffix: str, factory: Callable[[], dict]) -> None:
        self._suffix = suffix
        self._factory = factory

    @property
    def min(self) -> T | None:
        """minimum value"""
        if (value := self._factory()) is None:
            return None
        return value.get("min" + self._suffix, None)

    @property
    def max(self) -> T | None:
        """maximum value"""
        if (value := self._factory()) is None:
            return None
        return value.get("max" + self._suffix, None)


class StringRange:
    """String Ranges"""

    __slots__ = ("_factory",)

    def __init__(self, factory: Callable[[], dict]) -> None:
        self._factory = factory

    @property
    def length(self):
        """length ranges"""
        return MinMaxRange("Len", self._factory)
