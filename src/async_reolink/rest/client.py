""" ReoLink REST Client """

from async_reolink.api.client import Client as BaseClient

from .connection.typing import SSLContextFactory, SessionFactory

from .network.mixin import Network

from .security.mixin import Security

from .connection.mixin import Connection

from .record.mixin import Record

from .__version__ import __version__

from async_reolink.api.connection.model import Response

from async_reolink.api.ai import typing as ai_types
from .ai import command as ai

from .alarm import command as alarm

from .encoding import command as encoding

from async_reolink.api.led import typing as led_types
from .led import command as led

from async_reolink.api.ptz import typing as ptz_types
from .ptz import command as ptz

from .system import command as system


class Client(Connection, Security, Network, Record, BaseClient):
    """Rest API Client"""

    def __init__(
        self, session_factory: SessionFactory = None, ssl: SSLContextFactory = None
    ) -> None:
        super().__init__(session_factory=session_factory, ssl=ssl)

    # region ai

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

    # endregion

    # region alarm

    def _create_get_md_state(self, channel_id: int):
        return alarm.GetMotionStateRequest(channel_id=channel_id)

    def _is_get_md_response(self, response: Response):
        return isinstance(response, alarm.GetMotionStateResponse)

    # endregion

    # region encoding

    def _create_get_encoding(self, channel_id: int):
        return encoding.GetEncodingRequest(channel_id=channel_id)

    def _is_get_encoding_response(self, response: Response):
        return isinstance(response, encoding.GetEncodingResponse)

    # endregion

    # region led

    def _create_get_ir_lights(self, channel_id: int):
        return led.GetIrLightsRequest(channel_id=channel_id)

    def _is_get_ir_lights_response(self, response: Response):
        return isinstance(response, led.GetIrLightsResponse)

    def _create_set_ir_lights(self, state: led_types.LightStates, channel_id: int):
        return led.SetIrLightsRequest(state=state, channel_id=channel_id)

    def _create_get_power_led(self, channel_id: int):
        return led.GetPowerLedRequest(channel_id=channel_id)

    def _is_get_power_led_response(self, response: Response):
        return isinstance(response, led.GetPowerLedResponse)

    def _create_set_power_led(self, state: led_types.LightStates, channel_id: int):
        return led.SetPowerLedRequest(state=state, channel_id=channel_id)

    def _create_get_white_led(self, channel_id: int):
        return led.GetWhiteLedRequest(channel_id=channel_id)

    def _is_get_white_led_response(self, response: Response):
        return isinstance(response, led.GetWhiteLedResponse)

    def _create_set_white_led(self, info: led_types.WhiteLedInfo, channel_id: int):
        request = led.SetWhiteLedRequest(channel_id=channel_id)
        request.info.state = info.state
        if info.brightness is not None:
            request.info.brightness = info.brightness
        if info.brightness_state is not None:
            request.info.brightness_state = info.brightness_state
        if info.lighting_schedule is not None:
            request.info.lighting_schedule = info.lighting_schedule
        if info.ai_detection_type is not None:
            request.info.ai_detection_type = info.ai_detection_type
        return request

    # endregion

    # region PTZ

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

    # endregion

    # region system

    def _create_get_capabilities(self, username: str | None):
        return system.GetAbilitiesRequest(username)

    def _is_get_capabilities_response(self, response: Response):
        return isinstance(response, system.GetAbilitiesResponse)

    def _create_get_device_info(self):
        return system.GetDeviceInfoRequest()

    def _is_get_device_info_response(self, response: Response):
        return isinstance(response, system.GetDeviceInfoResponse)

    def _create_get_time(self):
        return system.GetTimeRequest()

    def _is_get_time_response(self, response: Response):
        return isinstance(response, system.GetTimeResponse)

    def _create_reboot(self):
        return system.RebootRequest()

    def _create_get_hdd_info(self):
        return system.GetHddInfoRequest()

    def _is_get_hdd_info_response(self, response: Response):
        return isinstance(response, system.GetHddInfoResponse)

    # endregion
