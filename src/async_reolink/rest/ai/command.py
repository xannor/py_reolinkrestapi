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

    def __init__(self, /, channel_id: int = ..., response_type: ResponseTypes = ...):
        super().__init__(
            command=type(self).COMMAND, channel_id=channel_id, response_type=response_type
        )

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

    def __init__(self, /, channel_id: int = ..., response_type: ResponseTypes = ...):
        super().__init__(
            command=type(self).COMMAND, channel_id=channel_id, response_type=response_type
        )

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
        self, /, channel_id: int = ..., response_type: ResponseTypes = ..., config: ai.Config = ...
    ):
        super().__init__(
            command=type(self).COMMAND, channel_id=channel_id, response_type=response_type
        )
        if config and config is not ...:
            self.config = config

    @property
    def id(self):
        return self._COMMAND_ID ^ self.channel_id

    @property
    def config(self):
        return model.MutableConfig(type(self)._parameter.fget.__get__(self))

    @config.setter
    def config(self, value):
        self.config.update(value)
