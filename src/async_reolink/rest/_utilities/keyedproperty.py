"""keyed property"""

from typing import (
    TYPE_CHECKING,
    Callable,
    Final,
    Generic,
    Protocol,
    TypeGuard,
    TypeVar,
    final,
    overload,
)


class dictfactory(Protocol):
    """dictonary factory"""

    def __factory__(self, canCreate=False) -> dict:
        ...


def _has_factory(obj: any) -> TypeGuard[dictfactory]:
    return hasattr(obj, "__factory__") and callable(obj.__factory__)


@final
class _Tag:
    pass


_MISSING: Final = _Tag()

MISSING: Final = _Tag()

NO_DEFAULT: Final = _Tag()

C = TypeVar("C")

T = TypeVar("T")

S = TypeVar("S")


class keyedproperty(Generic[T]):
    """keyed property"""

    __slots__ = (
        "_key",
        "_pfx",
        "_sfx",
        "_name",
        "_readonly",
        "_default",
        "_default_factory",
        "_get_trans",
        "_set_trans",
    )

    def __init__(
        self,
        /,
        key: str = None,
        prefix: str = None,
        suffix: str = None,
        readonly=False,
    ):
        super().__init__()
        self._key = key
        self._pfx = prefix
        self._sfx = suffix
        self._readonly = readonly
        self._default = MISSING

    @property
    def key(self):
        return f"{self._pfx}{self._key or self._name}{self._sfx}"

    def get_raw(self, obj: dictfactory, canCreate=False, default=MISSING) -> any:
        if _d := obj.__factory__(canCreate):
            value = _d.get(self.key, default)
        else:
            value = default
        if value is MISSING:
            raise AttributeError()
        return value

    def get_value(
        self,
        obj: dictfactory,
        canCreate=False,
        default=_MISSING,
        default_factory: Callable[[any], T] = None,
    ):
        value = self.get_raw(
            obj,
            canCreate,
        )

    @overload
    def value_factory(self, obj: dictfactory, /, default: S, canCreate=False) -> T | S:
        ...

    @overload
    def value_factory(
        self, obj: dictfactory, /, default_factory: Callable[[], S], canCreate=False
    ) -> T | S:
        ...

    @overload
    def value_factory(self, obj: dictfactory, /, canCreate=False) -> T:
        ...

    def value_factory(
        self,
        obj: dictfactory,
        /,
        canCreate=False,
        default=MISSING,
        default_factory: Callable[[], any] = None,
    ):
        if default_factory is not None and default is not MISSING:
            raise ValueError("cannot provide both default and default_factory")
        if _d := obj.__factory__(canCreate):
            value = _d.get(self.key, default)
        else:
            value = default
        if value is MISSING:
            if default_factory is not None:
                value = default_factory()
            else:
                raise AttributeError()
            if canCreate and _d:
                return _d.setdefault(self.key, value)
        return value

    def __set_name__(self, _owner: type, name: str):
        self._name = name

    @overload
    def __get__(self, obj: None, objType: type):
        return self

    @overload
    def __get__(self, obj: any, objType: type = None) -> T:
        ...

    def __get__(self, obj: any, objType: type | None = None):
        if obj is None and isinstance(objType, type):
            return self
        if not _has_factory(obj):
            raise AttributeError()
        return self.value_factory(obj, default=self._default, default_factory=self._default_factory)

    def __set__(self, obj: any, value: T):
        if self._readonly or not _has_factory(obj) or not (_d := obj.__factory__(True)):
            raise AttributeError()

    @overload
    def defaults(self, /, default: T) -> "keyedproperty[T]":
        ...

    @overload
    def defaults(self, default_factory: Callable[[any], T] = None) -> "keyedproperty[T]":
        ...

    def defaults(self, default_factory: Callable[[any], T] = None, /, default: T = MISSING):
        """set defaults"""
        if default is not MISSING and default_factory is not None:
            raise ValueError("both default and default_factory cannot be set at the same time")
        new = keyedproperty(self._key, self._pfx, self._sfx, self._readonly)
        new._default = default
        new._default_factory = default_factory
        return new

    def transform(
        self, getter: Callable[[any, T], S], setter: Callable[[any, S], T] = None
    ) -> "keyedproperty[S]":
        """transform value"""

        new = keyedproperty(self._key, self._pfx, self._sfx, self._readonly)
        new._default = self._default
        new._default_factory = self._default_factory
        new._get_trans = getter
        new._set_trans = setter
        return new


class c(dictfactory):
    @keyedproperty().transform
    def prop(self, value):
        return int(value)


t = c.prop

q = t.value_factory

v = c().prop
