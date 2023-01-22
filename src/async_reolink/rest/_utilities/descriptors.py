"""Descriptor helpers"""

from typing import TYPE_CHECKING, Callable, Generic, TypeVar, cast, overload
from typing_extensions import Self

_T = TypeVar("_T")
_R_co = TypeVar("_R_co", covariant=True)


class instance_or_classproperty(Generic[_T]):

    __slots__ = ("__fget", "__cfget")

    def __init__(
        self,
        fget: Callable[[any], _T] | None = ...,
        doc: str | None = ...,
    ) -> None:
        self.__fget = fget
        self.__cfget = fget

    @property
    def fget(self):
        return self.__fget

    @property
    def cfget(self):
        return self.__cfget

    def class_getter(self, getter: Callable[[any], _T]):
        self.__cfget = getter
        return self

    @overload
    def __get__(self, __obj: None, __type: any) -> _T:
        ...

    @overload
    def __get__(self, __obj: any, __type: any = None) -> _T:
        ...

    def __get__(self, __obj: any, __type: type | None = ...):
        if __obj is None and self.__cfget is not None:
            return self.__cfget(__type)
        return self.__fget(__obj)

    def __set__(self, _obj: any, _value: any):
        raise NotImplementedError()


class class_or_instancemethod(classmethod, Generic[_R_co]):
    def __init__(self: "class_or_instancemethod[_R_co]", __f: Callable[..., _R_co]) -> None:
        super().__init__(__f)
        self.__inst_func__ = __f

    def instance_method(self, __f: Callable[..., _R_co]):
        self.__inst_func__ = __f
        return self

    @overload
    def __get__(self, __obj: _T, __type: type[_T] | None = None) -> Callable[..., _R_co]:
        ...

    @overload
    def __get__(self, __obj: None, __type: type[_T]) -> Callable[..., _R_co]:
        ...

    def __get__(self, __obj: _T, __type: type[_T] | None = ...):
        if __obj is None:
            return super().__get__(__obj, __type)
        return self.__inst_func__.__get__(__obj, __type)
