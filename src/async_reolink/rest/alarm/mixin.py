"""REST Alarm"""

from async_reolink.api.alarm.mixin import Alarm as BaseAlarm

from ..connection.model import Response
from . import command as alarm


class Alarm(BaseAlarm):
    """REST Alarm Mixin"""

    def _create_get_md_state(self, channel_id: int):
        return alarm.GetMotionStateRequest(channel_id=channel_id)

    def _is_get_md_response(self, response: Response):
        return isinstance(response, alarm.GetMotionStateResponse)
