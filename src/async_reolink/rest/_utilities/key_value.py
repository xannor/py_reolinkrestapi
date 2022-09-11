"""Lazy key value"""

from async_reolink.api._utilities.typings import (
    SupportsGetItem,
    SupportsSetItem,
    SupportsDeleteItem,
    setdefault,
)

from typing import Callable, Generic, Mapping, TypeVar, overload

from .lazy import (
    SupportsLazyFactory,
    NO_RESULT as _MISSING,
    LazyProperty,
    ValueFactoryCall,
)

_KT_contra = TypeVar("_KT_contra", contravariant=True)
_VT_co = TypeVar("_VT_co", covariant=True)
_KT = TypeVar("_KT")
_VT = TypeVar("_VT")
_T = TypeVar("_T")


class KeyValue(Generic[_KT_contra, _VT_co]):
    """Key Value Descriptor for LazyValue descendant"""

    __slots__ = ("_key", "_default", "_readonly", "_ensure", "_get_obj")

    def __init__(
        self,
        key: _KT_contra,
        /,
        default: _VT_co = _MISSING,
        default_factory: Callable[[], _VT_co] = None,
        readonly=False,
        ensure=False,
    ) -> None:
        if default_factory is not None:
            if default is not _MISSING:
                raise ValueError("cannot specify both default and default_factory")
            default = default_factory
        self._key = key
        self._default = default
        self._readonly = readonly
        self._ensure = ensure
        self._get_obj = self.__get_obj

    @property
    def key(self):
        """key"""
        return self._key

    @property
    def default(self):
        """default"""
        return self._default

    @property
    def readonly(self):
        """read only"""
        return self._readonly

    @property
    def ensure(self):
        """ensured"""
        return self._ensure

    def __get_obj(
        self, obj: SupportsLazyFactory[SupportsGetItem[_KT_contra]], ensure=False
    ):
        return obj.__lazy_factory__(ensure)

    def __get_default(self) -> _VT_co:
        if callable(self._default):
            return self._default()
        else:
            return self._default

    def __get_value(
        self, obj: SupportsLazyFactory[SupportsGetItem[_KT_contra]], ensure=False
    ) -> _VT_co:
        obj = self._get_obj(obj, ensure)
        try:
            if obj is not _MISSING:
                return obj[self._key]
        except (KeyError, IndexError):
            pass
        value = self.__get_default()
        if obj is not _MISSING and value is not _MISSING and ensure:
            return setdefault(obj, self._key, value)
        return value

    @overload
    def __get__(self, obj: None, __type: type) -> "KeyValue[_KT_contra,_VT_co]":
        ...

    @overload
    def __get__(
        self, obj: SupportsLazyFactory[SupportsGetItem[_KT_contra]], __type: type
    ) -> _VT_co:
        ...

    def __get__(
        self,
        obj: SupportsLazyFactory[SupportsSetItem[_KT_contra, _VT_co]],
        __type: type = None,
    ):
        if obj is None:
            return self
        value = self.__get_value(obj, self._ensure)
        if value is _MISSING:
            raise AttributeError()
        return value

    def __set__(
        self,
        obj: SupportsLazyFactory[SupportsDeleteItem[_KT_contra, any]],
        value: _VT_co,
    ):
        if self._readonly:
            raise AttributeError()
        obj = self._get_obj(obj, True)
        if obj is None:
            raise AttributeError()
        obj[self._key] = value

    def __delete__(self, obj: SupportsLazyFactory[SupportsDeleteItem[_KT_contra]]):
        if self._readonly:
            raise AttributeError()
        obj = self._get_obj(obj)
        if obj is None:
            return
        del obj[self._key]

    @overload
    def key_value(
        self: "KeyValue[any,Mapping]",
        key: _KT,
        /,
        readonly=False,
        ensure=False,
    ) -> "KeyValue[_KT,any]":
        ...

    @overload
    def key_value(
        self: "KeyValue[any,Mapping]",
        key: _KT,
        /,
        default: _VT,
        readonly=False,
        ensure=False,
    ) -> "KeyValue[_KT,_VT]":
        ...

    @overload
    def key_value(
        self: "KeyValue[any,Mapping]",
        key: _KT,
        /,
        default_factory: Callable[[], _VT],
        readonly=False,
        ensure=False,
    ) -> "KeyValue[_KT,_VT]":
        ...

    def key_value(
        self,
        key,
        /,
        default=_MISSING,
        default_factory=None,
        readonly=False,
        ensure=False,
    ):
        """sub key->value"""

        _kv = KeyValue(
            key,
            default=default,
            default_factory=default_factory,
            readonly=readonly,
            ensure=ensure,
        )

        def _get_obj(obj, ensure):
            return self.__get_value(obj, ensure)

        # pylint: disable=protected-access
        _kv._get_obj = _get_obj

        return _kv

    @overload
    def lazy(self, factory: Callable[[_VT_co], _T]):
        """Convert value"""

        def _factory(f) -> _T:
            raise NotImplementedError()

        _p = LazyProperty(_factory)

        def _get_factory(obj, create) -> ValueFactoryCall:
            raise NotImplementedError()

        _p._get_factory = _get_factory

        return _p


@overload
def key_value(
    key: _KT,
    /,
    readonly=False,
    ensure=False,
) -> KeyValue[_KT, any]:
    ...


@overload
def key_value(
    key: _KT, /, default: _VT, readonly=False, ensure=False
) -> KeyValue[_KT, _VT]:
    ...


@overload
def key_value(
    key: _KT,
    /,
    default_factory: Callable[[], _VT],
    readonly=False,
    ensure=False,
) -> KeyValue[_KT, _VT]:
    ...


def key_value(
    key, /, default=_MISSING, default_factory=None, readonly=False, ensure=False
):
    """key value constructor"""

    return KeyValue(
        key,
        default=default,
        default_factory=default_factory,
        readonly=readonly,
        ensure=ensure,
    )
