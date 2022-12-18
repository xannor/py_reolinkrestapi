"""REST AI"""

from async_reolink.api.ai.mixin import AI as BaseAI

from async_reolink.api.ai import typing as ai_types

from ..connection.model import Response
from . import command as ai


class AI(BaseAI):
    """REST AI Mixin"""

    def _create_get_ai_config(self, channel: int):
        return ai.GetAiConfigRequest(channel_id=channel)

    def _is_get_ai_config_response(self, response: Response):
        return isinstance(response, ai.GetAiConfigResponse)

    def _create_get_ai_state(self, channel: int):
        return ai.GetAiStateRequest(channel_id=channel)

    def _is_get_ai_state_response(self, response: Response):
        return isinstance(response, ai.GetAiStateResponse)

    def _create_set_ai_config(self, channel: int, config: ai_types.Config):
        request = ai.SetAiConfigRequest(channel_id=channel)
        request.config.update(config)
        return request
