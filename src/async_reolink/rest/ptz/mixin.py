"""REST PTZ"""

from async_reolink.api.ptz.mixin import PTZ as BasePTZ

from async_reolink.api.ptz import typing as ptz_types

from ..connection.model import Response
from . import command as ptz


class PTZ(BasePTZ):
    """REST PTZ Mixin"""

    def _create_get_ptz_presets(self, channel_id: int):
        return ptz.GetPresetRequest(channel_id)

    def _is_get_ptz_presets_response(self, response: Response):
        return isinstance(response, ptz.GetPresetResponse)

    def _create_set_ptz_preset(self, channel_id: int, preset: ptz_types.Preset):
        return ptz.SetPresetRequest(preset, channel_id)

    def _create_get_ptz_patrols(self, channel_id: int):
        return ptz.GetPatrolRequest(channel_id)

    def _is_get_ptz_patrols_response(self, response: Response):
        return isinstance(response, ptz.GetPatrolResponse)

    def _create_set_ptz_patrol(self, channel_id: int, patrol: ptz_types.Patrol):
        return ptz.SetPatrolRequest(patrol, channel_id)

    def _create_get_ptz_tatterns(self, channel_id: int):
        return ptz.GetTatternRequest(channel_id)

    def _is_get_ptz_tatterns_response(self, response: Response):
        return isinstance(response, ptz.GetTatternResponse)

    def _create_set_ptz_tatterns(self, channel_id: int, *track: ptz_types.Track):
        return ptz.SetTatternRequest(track, channel_id=channel_id)

    def _create_set_ptz_control(
        self,
        channel_id: int,
        operation: ptz_types.Operation,
        speed: int | None,
        preset_id: int | None,
    ):
        return ptz.SetControlRequest(operation, preset_id, speed, channel_id)

    def _create_get_ptz_autofocus(self, channel_id: int):
        return ptz.GetAutoFocusRequest(channel_id)

    def _is_get_ptz_autofocus_response(self, response: Response):
        return isinstance(response, ptz.GetAutoFocusResponse)

    def _create_set_ptz_autofocus(self, channel_id: int, disabled: bool):
        return ptz.SetAutoFocusRequest(disabled, channel_id)

    def _create_get_ptz_zoom_focus(self, channel_id: int):
        return ptz.GetZoomFocusRequest(channel_id)

    def _is_get_ptz_zoom_focus_response(self, response: Response):
        return isinstance(response, ptz.GetZoomFocusResponse)

    def _create_set_ptz_zoom_focus(
        self, channel_id: int, operation: ptz_types.ZoomOperation, position: int
    ):
        return ptz.SetZoomFocusRequest(operation, position, channel_id)
