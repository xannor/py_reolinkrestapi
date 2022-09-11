"""REST LED Mixin"""

from typing import Mapping, Sequence
from async_reolink.api import led
from async_reolink.api.led.typings import LightStates, LightingSchedule
from async_reolink.api.ai.typings import AITypes
from async_reolink.api.typings import PercentValue

from ..commands import led as commands


class LED(led.LED):
    """REST LED Mixin"""

    def _create_get_ir_lights_request(self, channel: int):
        return commands.GetIrLightsRequest(channel)

    def _create_set_ir_lights_request(self, state: LightStates, channel: int):
        return commands.SetIrLightsRequest(state, channel)

    def _create_get_power_led_request(self, channel: int):
        return commands.GetPowerLedRequest(channel)

    def _create_set_power_led_request(self, state: LightStates, channel: int):
        return commands.SetPowerLedRequest(state, channel)

    def _create_get_white_led_request(self, channel: int):
        return commands.GetWhiteLedRequest(channel)

    def _create_set_white_led_request(
        self,
        state: LightStates,
        brightness: PercentValue | None,
        mode: int | None,
        schedule: LightingSchedule | None,
        ai_detect: Mapping[AITypes, bool] | Sequence[AITypes] | AITypes | None,
        channel: int,
    ):
        req = commands.SetWhiteLedRequest(channel)
        req.info.state = state
        if brightness is not None:
            req.info.brightness = brightness
        if mode is not None:
            req.info.brightness_state = mode
        if schedule is not None:
            req.info.lighting_schedule = schedule
        if ai_detect is not None:
            req.info.ai_detection_type = ai_detect
        return req
