"""Enum Helpers"""

from enum import Enum, Flag
from typing import (
    TYPE_CHECKING,
    ClassVar,
    Generic,
    Iterator,
    Mapping,
    cast,
    get_args,
    overload,
)

from typing_extensions import TypeVar

from .._utilities.descriptors import instance_or_classproperty

E = TypeVar("E", bound=Enum, default=Enum, infer_variance=True)
V = TypeVar("V", default=int, infer_variance=True)
T = TypeVar("T", default=int, infer_variance=True)


class EnumMap(Generic[E, V]):
    """Maps between enum and value"""

    @instance_or_classproperty
    def Enum(self):
        return self.__enum

    @classmethod
    def get_enum_type(cls):
        args = get_args(cls)
        if len(args) < 1:
            return None
        return type(args[0])

    @Enum.class_getter
    def Enum(cls) -> type[E]:
        return cls.get_enum_type() or Enum

    @instance_or_classproperty
    def Value(self):
        return self.__type

    @classmethod
    def get_value_type(cls):
        args = get_args(cls)
        if len(args) < 2:
            return None
        return type(args[1])

    @Value.class_getter
    def Value(cls):
        return cls.get_value_type() or int

    __slots__ = ("__cache", "__enum", "__type", "__default")

    def __init__(self, __map: Mapping[E, V], /, __default: E = ...):
        super().__init__()
        self.__cache = {}
        self.__default = __default
        self.__enum: type[E] = self.get_enum_type()
        self.__type: type[V] = self.get_value_type()
        for _k, _v in __map.items():
            self.__cache[_k] = _v
            self.__cache[_v] = _k
            if self.__enum is None:
                self.__enum = type(_k)
            if self.__type is None:
                self.__type = type(_v)
        if self.__enum is None or self.__type is None:
            _t = get_args(__map)
            if self.__enum is None:
                self.__enum = _t[0] if len(_t) > 0 else Enum
            if self.__type is None:
                self.__type = _t[1] if len(_t) > 1 else int

    @property
    def DEFAULT(self) -> E:
        if self.__default is ...:
            __enum = self.Enum
            __default = next(iter(__enum))
            if TYPE_CHECKING:
                __default = cast(__enum, __default)
            self.__default = __default
        return self.__default

    def to_enum(self, value: any) -> E:
        if isinstance(value, self.Enum):
            return value
        return self[value]

    def to_value(self, enum: any) -> V:
        if isinstance(enum, self.Enum):
            return enum
        return self[enum]

    def enums(self):
        _iter = iter(self.Enum)
        if TYPE_CHECKING:
            _iter = cast(Iterator[E], _iter)
        for _e in _iter:
            if _e in self:
                yield _e

    def values(self):
        __type = self.Value
        for _e in self.Enum:
            if (_v := self.get(_e, ...)) is not ...:
                if TYPE_CHECKING:
                    _v = cast(__type, _v)
                yield _v

    def __contains__(self, value: any):
        return value in self.__cache

    @overload
    def __call__(self, key: E) -> V:
        ...

    @overload
    def __call__(self, key: V) -> E:
        ...

    def __call__(self, key: any):
        return self[key]

    @overload
    def get(self, key: E, /) -> V:
        ...

    @overload
    def get(self, key: E, __default: T, /) -> V | T:
        ...

    @overload
    def get(self, key: V, /) -> E:
        ...

    @overload
    def get(self, key: V, __default: T, /) -> E | T:
        ...

    def get(self, key: any, __default: ...):
        if __default is not ...:
            return self.__cache.get(key, __default)
        return self.__cache.get(key)

    @overload
    def __getitem__(self, key: E) -> V:
        ...

    @overload
    def __getitem__(self, key: V) -> E:
        ...

    def __getitem__(self, key: any):
        return self.__cache[key]


F = TypeVar("F", bound=Flag)


class FlagMap(Generic[F, V]):
    @instance_or_classproperty
    def Flag(self) -> type[F]:
        return self.__flag

    @classmethod
    def get_flag_type(cls):
        args = get_args(cls)
        if len(args) < 1:
            return None
        return type(args[0])

    @Flag.class_getter
    def Flag(cls) -> type[F]:
        return cls.get_flag_type() or Flag

    @instance_or_classproperty
    def Value(self):
        return self.__type

    @classmethod
    def get_value_type(cls):
        args = get_args(cls)
        if len(args) < 2:
            return None
        return type(args[1])

    @Value.class_getter
    def Value(cls):
        return cls.get_value_type() or int

    __slots__ = ("__cache", "__flag", "__type", "__none", "__all")

    def __init__(self, __map: Mapping[F, V], /, __none: F = ..., __all: F = ...):
        super().__init__()
        self.__cache = {}
        self.__none = __none
        self.__all = __all

        self.__flag: type[F] = self.get_flag_type()
        self.__type: type[V] = self.get_value_type()
        for _k, _v in __map.items():
            self.__cache[_k] = _v
            self.__cache[_v] = _k
            if self.__flag is None:
                self.__flag = type(_k)
            if self.__type is None:
                self.__type = type(_v)
        if self.__flag is None or self.__type is None:
            _t = get_args(__map)
            if self.__flag is None:
                self.__flag = _t[0] if len(_t) > 0 else Flag
            if self.__type is None:
                self.__type = _t[1] if len(_t) > 1 else int

    @property
    def NONE(self) -> F:
        if self.__none is ...:
            __type = self.Flag
            self.__none = __type(0)
        return self.__none

    @property
    def ALL(self) -> F:
        if self.__all is ...:
            __all = self.NONE
            _iter = iter(self.Flag)
            if TYPE_CHECKING:
                _iter = cast(Iterator[F], _iter)
            for _f in _iter:
                __all |= _f
            self.__all = __all
        return self.__all

    def _missing_(self, flag: F = None, value: V = None):
        _flag: F = None
        _value: V = None
        if flag is None or value is None:
            _iter = iter(self.Flag)
            if TYPE_CHECKING:
                __type = self.Flag
                _iter = cast(Iterator[__type], _iter)
            for _f in _iter:
                if (_v := self.__cache.get(_f, None)) is not None:
                    if (flag is not None and flag & _f == _f) or (
                        value is not None and value & _v == _v
                    ):
                        if _flag is None:
                            _flag = _f
                            _value = _v
                        else:
                            _flag |= _f
                            _value |= _v
            if _flag is None:
                _flag = self.NONE
            elif TYPE_CHECKING:
                _flag = cast(__type, _flag)

        self.__cache[_flag] = _value
        self.__cache[_value] = _flag

        return (_flag, _value)

    def to_flag(self, value: any) -> F:
        if isinstance(value, self.Flag):
            return value

        if value in self.__cache:
            return self.__cache[value]

        (_flag, _value) = self._missing_(value=value)
        return _flag

    def to_value(self, flag: any) -> V:
        if isinstance(flag, self.Value):
            return flag

        if flag in self.__cache:
            return self.__cache[flag]

        (_flag, _value) = self._missing_(flag=flag)
        return _value

    def flags(self):
        _iter = iter(self.Flag)
        if TYPE_CHECKING:
            __type = self.Flag
            _iter = cast(Iterator[__type], _iter)

        for _f in _iter:
            if _f in self:
                yield _f

    def values(self):
        __type = self.Value
        for _f in self.Flag:
            if (_v := self.get(_f, ...)) is not ...:
                if TYPE_CHECKING:
                    _v = cast(__type, _v)
                yield _v

    @overload
    def __call__(self, value: F) -> V:
        ...

    @overload
    def __call__(self, value: V) -> F:
        ...

    def __call__(self, value: any):
        return self.get(value)

    def __contains__(self, value: any):
        return value in self.__cache

    @overload
    def __getitem__(self, key: F) -> V:
        ...

    @overload
    def __getitem__(self, key: V) -> F:
        ...

    def __getitem__(self, key: any):
        return self.__cache[key]

    @overload
    def get(self, key: F, /) -> V:
        ...

    @overload
    def get(self, key: F, __default=T, /) -> V | T:
        ...

    @overload
    def get(self, key: V, /) -> F:
        ...

    @overload
    def get(self, key: V, __default=T, /) -> F | T:
        ...

    def get(self, key: any, __default=..., /):
        if __default is not ...:
            return self.__cache.get(key, __default)

        if (_r := self.__cache.get(key, ...)) is not ...:
            return _r

        if isinstance(key, self.Flag):
            flag = key
            value = None
        else:
            flag = None
            value = key

        (_flag, _value) = self._missing_(flag, value)
        if value is None:
            return _value
        return _flag
