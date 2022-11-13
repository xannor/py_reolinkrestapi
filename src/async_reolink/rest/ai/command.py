"""AI REST Commands"""

from typing import Final, TypeGuard

from async_reolink.api.connection.model import Request
from async_reolink.api.ai import command as ai

from . import model


from ..connection.model import (
    _CHANNEL_KEY,
    Response,
    ResponseTypes,
    RequestWithChannel,
    ResponseWithChannel,
)

# pylint:disable=missing-function-docstring


class GetAiStateRequest(RequestWithChannel, ai.GetAiStateRequest):
    """Get AI State"""

    __slots__ = ()

    COMMAND: Final = "GetAiState"

    def __init__(
        self,
        channel_id: int = 0,
        response_type: ResponseTypes = ResponseTypes.VALUE_ONLY,
    ):
        super().__init__()
        self.command = type(self).COMMAND
        self.response_type = response_type
        self.channel_id = channel_id


_NONE_DICT: Final[dict] = None


class GetAiStateResponse(
    Response,
    ai.GetAiStateResponse,
):
    """Get AI State Response"""

    __slots__ = ()

    @classmethod
    def from_response(cls, response: any, request: Request | None = None):
        if super().is_response(response, command=GetAiStateRequest.COMMAND):
            return cls(response, request_id=request.id if request else None)
        return None

    @property
    def channel_id(self) -> int:
        if (value := self._get_value()) is None:
            return None
        return value.get(_CHANNEL_KEY, None)

    @property
    def state(self):
        return model.State(self._get_value())

    def can_update(self, value: any) -> TypeGuard[model.State]:
        """Is value updatable"""
        return isinstance(value, model.State)


class GetAiConfigRequest(RequestWithChannel, ai.GetAiConfigRequest):
    """Get AI Configuration"""

    COMMAND: Final = "GetAiCfg"

    def __init__(
        self,
        channel_id: int = 0,
        response_type: ResponseTypes = ResponseTypes.VALUE_ONLY,
    ):
        super().__init__()
        self.command = type(self).COMMAND
        self.response_type = response_type
        self.channel_id = channel_id


class GetAiConfigResponse(
    ResponseWithChannel,
    ai.GetAiConfigResponse,
):
    """Get AI Configuration Response"""

    @classmethod
    def from_response(cls, response: any, request: Request | None = None):
        if super().is_response(response, command=GetAiStateRequest.COMMAND):
            return cls(response, request_id=request.id if request else None)
        return None

    @property
    def channel_id(self) -> int:
        if (value := self._get_value()) is None:
            return None
        return value.get(_CHANNEL_KEY, None)

    @property
    def config(self):
        return model.Config(self._get_value())

    def can_update(self, value: any) -> TypeGuard[model.Config]:
        """Is value updatable"""
        return isinstance(value, model.Config)


class SetAiConfigRequest(RequestWithChannel, ai.SetAiConfigRequest):
    """Set AI Configuration"""

    COMMAND: Final = "SetAiCfg"

    def __init__(
        self,
        channel_id: int = 0,
        response_type: ResponseTypes = ResponseTypes.VALUE_ONLY,
    ) -> None:
        super().__init__()
        self.command = type(self).COMMAND
        self.response_type = response_type
        self.channel_id = channel_id

    @property
    def config(self):
        return model.MutableConfig(self._get_parameter)
