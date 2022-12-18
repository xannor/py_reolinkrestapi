"""AI REST Commands"""

from typing import Final, TypeGuard

from async_reolink.api.connection.model import Request
from async_reolink.api.ai import command as ai

from . import model


from ..connection.model import (
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
    _COMMAND_ID: Final = hash(COMMAND)

    def __init__(
        self,
        channel_id: int = 0,
        response_type: ResponseTypes = ResponseTypes.VALUE_ONLY,
    ):
        super().__init__()
        self.command = self.COMMAND
        self.response_type = response_type
        self.channel_id = channel_id

    @property
    def id(self):
        return self._COMMAND_ID ^ self.channel_id


class GetAiStateResponse(
    ResponseWithChannel,
    ai.GetAiStateResponse,
):
    """Get AI State Response"""

    @classmethod
    def from_response(cls, response: any, /, request: Request | None = None, **kwargs):
        if super().is_response(response, command=GetAiStateRequest.COMMAND):
            return cls(response, request_id=request.id if request else None, **kwargs)
        return None

    __slots__ = ()

    @property
    def state(self):
        return model.UpdatableState(self._value)


class GetAiConfigRequest(RequestWithChannel, ai.GetAiConfigRequest):
    """Get AI Configuration"""

    COMMAND: Final = "GetAiCfg"
    _COMMAND_ID: Final = hash(COMMAND)

    def __init__(
        self,
        channel_id: int = 0,
        response_type: ResponseTypes = ResponseTypes.VALUE_ONLY,
    ):
        super().__init__()
        self.command = self.COMMAND
        self.response_type = response_type
        self.channel_id = channel_id

    @property
    def id(self):
        return self._COMMAND_ID ^ self.channel_id


class GetAiConfigResponse(
    ResponseWithChannel,
    ai.GetAiConfigResponse,
):
    """Get AI Configuration Response"""

    @classmethod
    def from_response(cls, response: any, /, request: Request | None = None, **kwargs):
        if super().is_response(response, command=GetAiConfigRequest.COMMAND):
            return cls(response, request_id=request.id if request else None, **kwargs)
        return None

    @property
    def config(self):
        return model.Config(self._value)


class SetAiConfigRequest(RequestWithChannel, ai.SetAiConfigRequest):
    """Set AI Configuration"""

    COMMAND: Final = "SetAiCfg"
    _COMMAND_ID: Final = hash(COMMAND)

    def __init__(
        self,
        channel_id: int = 0,
        response_type: ResponseTypes = ResponseTypes.VALUE_ONLY,
    ) -> None:
        super().__init__()
        self.command = self.COMMAND
        self.response_type = response_type
        self.channel_id = channel_id

    @property
    def id(self):
        return self._COMMAND_ID ^ self.channel_id

    @property
    def config(self):
        return model.MutableConfig(self._get_parameter)

    @config.setter
    def config(self, value):
        self.config.update(value)
