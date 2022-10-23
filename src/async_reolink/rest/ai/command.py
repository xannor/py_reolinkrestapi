"""AI REST Commands"""

from typing import Final, TypeGuard

from async_reolink.api.ai import command as ai
from async_reolink.api.connection.typing import CommandResponse

from . import models


from ..connection.models import (
    _CHANNEL_KEY,
    CommandResponse as RestCommandResponse,
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
    RestCommandResponse,
    ai.GetAiStateResponse,
    test="is_response",
):
    """Get AI State Response"""

    __slots__ = ()

    @classmethod
    def is_response(cls, value: any, /):  # pylint: disable=signature-differs
        return super().is_response(value, GetAiStateRequest.COMMAND)

    @property
    def channel_id(self) -> int:
        if (value := self._get_value()) is None:
            return None
        return value.get(_CHANNEL_KEY, None)

    @property
    def state(self):
        return models.State(self._get_value())

    def can_update(self, value: any) -> TypeGuard[models.State]:
        """Is value updatable"""
        return isinstance(value, models.State)


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


class GetAiConfigResponse(
    CommandResponseWithChannel,
    ai.GetAiConfigResponse,
    test="is_response",
):
    """Get AI Configuration Response"""

    @classmethod
    def is_response(cls, value: any, /):  # pylint: disable=signature-differs
        return super().is_response(value, GetAiConfigRequest.COMMAND)

    @property
    def channel_id(self) -> int:
        if (value := self._get_value()) is None:
            return None
        return value.get(_CHANNEL_KEY, None)

    @property
    def config(self):
        return models.Config(self._get_value())

    def can_update(self, value: any) -> TypeGuard[models.Config]:
        """Is value updatable"""
        return isinstance(value, models.Config)


class SetAiConfigRequest(CommandRequestWithChannel, ai.SetAiConfigRequest):
    """Set AI Configuration"""

    COMMAND: Final = "SetAiCfg"

    def __init__(
        self,
        channel_id: int = 0,
        response_type: CommandResponseTypes = CommandResponseTypes.VALUE_ONLY,
    ) -> None:
        super().__init__()
        self.command = type(self).COMMAND
        self.response_type = response_type
        self.channel_id = channel_id

    @property
    def config(self):
        return models.MutableConfig(self._get_parameter)


class CommandFactory(ai.CommandFactory):
    """AI Rest Command Factory"""

    def create_get_ai_state_request(self, channel_id: int):
        return GetAiStateRequest(channel_id)

    def is_get_ai_config_response(
        self, response: CommandResponse
    ) -> TypeGuard[GetAiConfigResponse]:
        return isinstance(response, GetAiConfigResponse)

    def create_get_ai_config_request(self, channel_id: int):
        return GetAiConfigRequest(channel_id)

    def is_get_ai_state_response(
        self, response: CommandResponse
    ) -> TypeGuard[GetAiStateResponse]:
        return isinstance(response, GetAiStateResponse)

    def create_set_ai_config(self, channel_id: int, config: ai.Config):
        request = SetAiConfigRequest(channel_id)
        request.config.update(config)
        return request
