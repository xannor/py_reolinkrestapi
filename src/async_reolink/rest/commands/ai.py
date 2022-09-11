"""AI REST Commands"""

from typing import Final, Mapping, TypeGuard

from async_reolink.api.commands import ai
from async_reolink.api.ai.typings import AITypes

from ..ai.models import AlarmState, AITypesMap, MutableAITypesMap
from ..ai.typings import AITYPES_STR_MAP
from . import (
    CommandResponse,
    CommandResponseTypes,
    CommandRequestWithChannel,
    CommandResponseWithChannel,
)

# pylint:disable=missing-function-docstring


class GetAiStateRequest(CommandRequestWithChannel, ai.GetAiStateRequest):
    """Get AI State"""

    __slots__ = ()

    COMMAND: Final = "GetAiState"

    def __init__(
        self,
        channel_id: int = 0,
        response_type: CommandResponseTypes = CommandResponseTypes.VALUE_ONLY,
    ):
        super().__init__()
        self.command = type(self).COMMAND
        self.response_type = response_type
        self.channel_id = channel_id


_NONE_DICT: Final[dict] = None


class GetAiStateResponse(
    CommandResponse,
    ai.GetAiStateResponse,
    test="is_response",
):
    """Get AI State Response"""

    __slots__ = ()

    @classmethod
    def is_response(  # pylint: disable=signature-differs
        cls, value: any, /
    ) -> TypeGuard["GetAiStateResponse"]:
        return super().is_response(value, GetAiStateRequest.COMMAND)

    def __getitem__(self, __k: AITypes):
        def _factory():
            return (
                value.get(AITYPES_STR_MAP[__k], None)
                if (value := self._get_value()) is not None
                else None
            )

        return AlarmState(_factory)

    def __contains__(self, __o: AITypes):
        if (value := self._get_value()) is None:
            return False
        return AITYPES_STR_MAP[__o] in value

    def __iter__(self):
        if (value := self._get_value()) is None:
            return
        for _k, _v in AITYPES_STR_MAP.items():
            if _v in value:
                yield _k

    def __len__(self):
        if (value := self._get_value()) is None:
            return 0
        return len(AITYPES_STR_MAP.values() & value.keys())


class GetAiConfigRequest(CommandRequestWithChannel, ai.GetAiConfigRequest):
    """Get AI Configuration"""

    COMMAND: Final = "GetAiCfg"

    def __init__(
        self,
        channel_id: int = 0,
        response_type: CommandResponseTypes = CommandResponseTypes.VALUE_ONLY,
    ):
        super().__init__()
        self.command = type(self).COMMAND
        self.response_type = response_type
        self.channel_id = channel_id


_DETECT_TYPE_KEY: Final = "AiDetectType"
_TYPE_KEY: Final = "type"
_AI_TRACK_KEY: Final = "aiTrack"
_TRACK_TYPE_KEY: Final = "trackType"


class GetAiConfigResponse(
    CommandResponseWithChannel,
    ai.GetAiConfigResponse,
    test="is_response",
):
    """Get AI Configuration Response"""

    @classmethod
    def is_response(  # pylint: disable=signature-differs
        cls, value: any, /
    ) -> TypeGuard["GetAiConfigResponse"]:
        return super().is_response(value, GetAiConfigRequest.COMMAND)

    def _get_detect_type(self) -> dict:
        return (
            value.get(_DETECT_TYPE_KEY, None)
            if (value := self._get_value()) is not None
            else None
        )

    def _get_type(self) -> dict:
        return (
            value.get(_TYPE_KEY, None)
            if (value := self._get_value()) is not None
            else None
        )

    @property
    def detect_type(self):
        """detect type"""

        def _get():
            if (_dict := self._get_detect_type()) is not None:
                return _dict
            if (_dict := self._get_type()) is not None:
                return _dict
            return None

        return AITypesMap(_get)

    @property
    def ai_track(self) -> bool:
        return (
            value.get(_AI_TRACK_KEY, 0)
            if (value := self._get_value()) is not None
            else 0
        )

    def _get_track_type(self) -> dict:
        return (
            value.get(_TRACK_TYPE_KEY, None)
            if (value := self._get_value()) is not None
            else None
        )

    @property
    def track_type(self):
        return AITypesMap(self._get_track_type)


class SetAiConfigRequest(CommandRequestWithChannel, ai.SetAiConfigRequest):
    """Set AI Configuration"""

    COMMAND: Final = "SetAiCfg"

    def __init__(
        self,
        channel_id: int = 0,
        detect: AITypes | set[AITypes] | Mapping[AITypes, bool] | None = None,
        track: AITypes | set[AITypes] | Mapping[AITypes, bool] | None = None,
        response_type: CommandResponseTypes = CommandResponseTypes.VALUE_ONLY,
    ) -> None:
        super().__init__()
        self.command = type(self).COMMAND
        self.response_type = response_type
        self.channel_id = channel_id
        self.detect_type = detect
        self.track_type = track
        self.ai_track = self.track_type is not None and len(self.track_type) > 0

    def _get_dict(self, key: str, create=False) -> dict:
        if (parameter := self._get_parameter(create)) is None:
            return None
        if create and key not in parameter:
            return parameter.setdefault(key, {})
        return parameter.get(key, None)

    @property
    def _detect_type(self):
        return self._get_dict(_DETECT_TYPE_KEY, True)

    @property
    def _type(self):
        return self._get_dict(_TYPE_KEY, True)

    @_type.setter
    def _type(self, value):
        self._parameter[_TYPE_KEY] = value

    @property
    def detect_type(self):
        """detect type"""

        def _get(ensure: bool):
            if (value := self._get_dict(_DETECT_TYPE_KEY, ensure)) is None:
                if (value := self._get_dict(_TYPE_KEY, ensure)) is None:
                    return None
            return value

        return MutableAITypesMap(_get)

    def _update_map(self, _map: MutableAITypesMap, value):
        _map.clear()
        if isinstance(value, Mapping):
            _map.update(**value)
        if isinstance(value, AITypes):
            _map[value] = True
        for item in value:
            _map[AITypes(item)] = True

    @detect_type.setter
    def detect_type(self, value):
        self._update_map(self.detect_type, value)

    @property
    def _has_track_type(self):
        if (parameter := self._get_parameter()) is None:
            return False
        return _TRACK_TYPE_KEY in parameter

    @property
    def track_type(self):
        """track type"""

        def _get(ensure: bool):
            if self._has_track_type or ensure:
                return self._parameter.get(_TRACK_TYPE_KEY, {})
            return None

        return MutableAITypesMap(_get)

    @track_type.setter
    def track_type(self, value):
        self._update_map(self.track_type, value)
