"""REST LED"""

from async_reolink.api.led.mixin import LED as BaseLED

from async_reolink.api.led import typing as led_types

from ..connection.model import Response
from . import command as led


class LED(BaseLED):
    """REST LED Mixin"""

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
        return led.SetWhiteLedRequest(info=info, channel_id=channel_id)
