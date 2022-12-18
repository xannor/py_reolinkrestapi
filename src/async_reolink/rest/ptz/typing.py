"""REST PTZ Typings"""

from types import MappingProxyType
from typing import Final, ValuesView, overload
from async_reolink.api.ptz.typing import ZoomOperation, Operation

_OPERATION_MAP: Final = MappingProxyType(
    {
        Operation.STOP: "Stop",
        Operation.LEFT: "Left",
        Operation.RIGHT: "Right",
        Operation.UP: "Up",
        Operation.LEFT_UP: "LeftUp",
        Operation.LEFT_DOWN: "LeftDown",
        Operation.RIGHT_UP: "RightUp",
        Operation.RIGHT_DOWN: "RightDown",
        Operation.IRIS_SHRINK: "IrisDec",
        Operation.IRIS_ENLARGE: "IrisInc",
        Operation.ZOOM_OUT: "ZoomDec",
        Operation.ZOOM_IN: "ZoomInc",
        Operation.FOCUS_BACK: "FocusInc",
        Operation.FOCUS_FORWARD: "FocusDec",
        Operation.AUTO: "Auto",
        Operation.PATROL_START: "StartPatrol",
        Operation.PATROL_STOP: "StopPatrol",
        Operation.TO_PRESET: "ToPos",
    }
)

for _k, _v in _OPERATION_MAP.items():
    Operation._value2member_map_[_v] = _k


class _Missing:
    pass


_MISSING: Final = _Missing()


@overload
def operation_str() -> ValuesView[str]:
    ...


@overload
def operation_str(value: Operation) -> str:
    ...


def operation_str(value: Operation = _Missing):
    if value is _MISSING:
        return _OPERATION_MAP.values()
    return _OPERATION_MAP.get(value)


_ZOOMOPERATION_MAP: Final = MappingProxyType(
    {
        ZoomOperation.ZOOM: "ZoomPos",
        ZoomOperation.FOCUS: "FocusPos",
    }
)

for _k, _v in _ZOOMOPERATION_MAP.items():
    ZoomOperation._value2member_map_[_v] = _k


@overload
def zoom_operation_str() -> ValuesView[str]:
    ...


@overload
def zoom_operation_str(value: ZoomOperation) -> str:
    ...


def zoom_operation_str(value: ZoomOperation):
    if value is _MISSING:
        return _ZOOMOPERATION_MAP.values()
    return _ZOOMOPERATION_MAP.get(value)
