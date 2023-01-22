"""JSON copy routines"""

from typing import (
    Iterable,
    Mapping,
    MutableMapping,
    MutableSequence,
    Protocol,
    Sequence,
    TypeVar,
    overload,
    runtime_checkable,
)

_KT = TypeVar("_KT")
_VT_co = TypeVar("_VT_co", covariant=True)


@runtime_checkable
class SupportsKeysAndGetItem(Protocol[_KT, _VT_co]):
    def keys(self) -> Iterable[_KT]:
        ...

    def __getitem__(self, __key: _KT) -> _VT_co:
        ...


@overload
def update(self: MutableSequence[_VT_co], value: Iterable[_VT_co]) -> None:
    ...


@overload
def update(self: MutableSequence[_VT_co], *values: _VT_co) -> None:
    ...


@overload
def update(
    self: MutableMapping[_KT, _VT_co], value: SupportsKeysAndGetItem[_KT, _VT_co], **kwargs: _VT_co
) -> None:
    ...


@overload
def update(
    self: MutableMapping[_KT, _VT_co], value: Iterable[tuple[_KT, _VT_co]], **kwargs: _VT_co
) -> None:
    ...


@overload
def update(self: MutableMapping[_KT, _VT_co], /, **kwargs: _VT_co) -> None:
    ...


def update(self: any, *args, **kwargs):
    if isinstance(self, MutableMapping):
        seen = {}

        if len(args) == 1:
            _s = args[0]
            if isinstance(_s, SupportsKeysAndGetItem):
                _update_dict(self, seen, {_k: _s.__getitem__(_k) for _k in _s.keys()})
            elif isinstance(_s, Iterable):
                _update_dict(
                    self, seen, {_t[0]: _t[1] for _t in _s if isinstance(_t, tuple) and len(_t) > 1}
                )
        if len(kwargs) > 0:
            _update_dict(self, seen, kwargs)
    if isinstance(self, MutableSequence):
        if len(args) == 1:
            _update_list(self, {}, args[0])
        elif len(args) > 1:
            _update_list(self, {}, args)


@overload
def copy(self: Sequence[_VT_co]) -> list[_VT_co]:
    ...


@overload
def copy(self: Mapping[_KT, _VT_co]) -> dict[_KT, _VT_co]:
    ...


def copy(self: any):
    return _copy(self, {})


def _update_dict(self: dict[str, any], seen: dict, source: dict[str, any]):
    for _k, _v in source.items():
        if _v in seen:
            self[_k] = seen[_v]
            continue
        _sv = self.get(_k)
        if isinstance(_sv, dict) and isinstance(_v, dict):
            seen[_v] = _sv
            _update_dict(_sv, seen, _v)
            continue
        if isinstance(_sv, list) and isinstance(_v, list):
            seen[_v] = _sv
            _update_list(_sv, seen, _v)
            continue

        self[_k] = _copy(_v, seen)


def _update_list(self: list, seen: dict, source: list):
    l = len(self)
    for i, _v in enumerate(source):
        if _v in seen:
            if i < l:
                self[i] = seen[_v]
            else:
                self.append(seen[_v])
            continue
        _sv = self[i] if i < l else None
        if isinstance(_sv, dict) and isinstance(_v, dict):
            seen[_v] = _sv
            _update_dict(_sv, seen, _v)
            continue
        if isinstance(_sv, list) and isinstance(_v, list):
            seen[_v] = _sv
            _update_list(_sv, seen, _v)
            continue
        if i < l:
            self[i] = _copy(_v, seen)
        else:
            self.append(_copy(_v, seen))


def _copy(self: any, seen: dict):
    if self in seen:
        return seen[self]
    if isinstance(self, dict):
        _new = {}
        self[seen] = _new
        for _k, _v in self.items():
            _new[_k] = _copy(_v, seen)
        return _new
    if isinstance(self, list):
        _new = []
        self[seen] = _new
        for _v in self:
            _new.append(_copy(_v, seen))
        return _new
    return self


__all__ = ["copy", "update"]
