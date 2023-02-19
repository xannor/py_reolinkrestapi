"""REST LED Commands"""

from typing import Final, Callable, Protocol, TypedDict

from async_reolink.api.led import command as led
from async_reolink.api.led import typing as led_typing

from .._utilities.providers import value as providers

from .. import model

from . import model as local_model
from . import typing as local_typing

from ..connection.model import (
    Request,
    RequestWithChannel,
    ResponseTypes,
    Response as RestCommandResponse,
)

# pylint:disable=missing-function-docstring


class GetIrLightsRequest(RequestWithChannel, led.GetIrLightsRequest):
    """REST Get IR Lights"""

    __slots__ = ()

    COMMAND: Final = "GetIrLights"
    _COMMAND_ID: Final = hash(COMMAND)

    def __init__(self, /, channel_id: int = ..., response_type: ResponseTypes = ...):
        super().__init__(
            command=type(self).COMMAND, channel_id=channel_id, response_type=response_type
        )

    @property
    def id(self):
        return self._COMMAND_ID ^ self.channel_id


class LightStateJSON(TypedDict):
    """Light State JSON"""

    state: int


class LightStateKeys(Protocol):
    """Light State Keys"""

    state: Final = "state"


_DefaultLightState: Final = led_typing.LightStates.OFF


class GetIrLightsResponse(RestCommandResponse, led.GetIrLightsResponse):
    """REST Get IR Lights Response"""

    @classmethod
    def from_response(cls, response: any, /, request: Request | None = None, **kwargs):
        if super().is_response(response, GetIrLightsRequest.COMMAND):
            return cls(response, request_id=request.id if request else None, **kwargs)
        return None

    __slots__ = ()

    class Value(Protocol):
        """Value"""

        class Lights(Protocol):
            """Lights"""

            class JSON(RequestWithChannel.Parameter.JSON, LightStateJSON):
                """JSON"""

            class Keys(RequestWithChannel.Parameter.Keys, LightStateKeys, Protocol):
                """Keys"""

        class JSON(TypedDict):
            """JSON"""

            IrLights: "GetIrLightsResponse.Value.Lights.JSON"

        class Keys(Protocol):
            """Keys"""

            lights: Final = "IrLights"

    _get_value: providers.FactoryValue[Value.JSON]
    _value: Value.JSON

    def _get_lights(self, create=False) -> Value.Lights.JSON:
        return self.lookup_value(
            self._get_value,
            self.Value.Keys.lights,
            create=create,
            default=None,
        )

    @property
    def _lights(self):
        return self._get_lights()

    @property
    def channel_id(self):
        _default = 0
        return (
            value.get(self.Value.Lights.Keys.channel_id, _default)
            if (value := self._lights)
            else _default
        )

    @property
    def state(self):
        return (
            led_typing.LightStates(value.get(self.Value.Lights.Keys.state, _DefaultLightState))
            if (value := self._lights)
            else _DefaultLightState
        )


class SetIrLightsRequest(Request, led.SetIrLightsRequest):
    """REST Set Ir Lights"""

    __slots__ = ()

    class Parameter(GetIrLightsResponse.Value, Protocol):
        """Parameter"""

    COMMAND: Final = "SetIrLights"
    _COMMAND_ID: Final = hash(COMMAND)

    def __init__(
        self,
        /,
        channel_id: int = ...,
        response_type: ResponseTypes = ...,
        state: led_typing.LightStates = ...,
    ):
        super().__init__(
            command=type(self).COMMAND, channel_id=channel_id, response_type=response_type
        )
        if state and state is not ...:
            self.state = state

    @property
    def id(self):
        return self._COMMAND_ID ^ self.channel_id

    _get_parameter: providers.FactoryValue[Parameter.JSON]
    _parameter: Parameter.JSON

    def _get_lights(self, create=False) -> Parameter.Lights.JSON:
        return self.lookup_value(
            self._get_parameter,
            self.Parameter.Keys.lights,
            create=create,
            default_factory=lambda: dict() if create else None,
        )

    @property
    def _lights(self):
        return self._get_lights()

    @GetIrLightsResponse.channel_id.setter
    def channel_id(self, value):
        self._get_lights(True)[self.Parameter.Lights.Keys.channel_id] = int(value)

    @GetIrLightsResponse.state.setter
    def state(self, value):
        self._get_lights(True)[self.Parameter.Lights.Keys.state] = int(value)


class GetPowerLedRequest(RequestWithChannel, led.GetPowerLedRequest):
    """REST Get Power LED"""

    __slots__ = ()

    COMMAND: Final = "GetPowerLed"
    _COMMAND_ID: Final = hash(COMMAND)

    def __init__(self, /, channel_id: int = ..., response_type: ResponseTypes = ...):
        super().__init__(
            command=type(self).COMMAND, channel_id=channel_id, response_type=response_type
        )

    @property
    def id(self):
        return self._COMMAND_ID ^ self.channel_id


class GetPowerLedResponse(RestCommandResponse, led.GetPowerLedResponse):
    """REST Get Power LED Response"""

    @classmethod
    def from_response(cls, response: any, /, request: Request | None = None, **kwargs):
        if super().is_response(response, GetPowerLedRequest.COMMAND):
            return cls(response, request_id=request.id if request else None, **kwargs)
        return None

    class Value(Protocol):
        """Value"""

        class Lights(GetIrLightsResponse.Value.Lights, Protocol):
            """Lights"""

        class JSON(TypedDict):
            """JSON"""

            PowerLed: GetIrLightsResponse.Value.Lights.JSON

        class Keys(Protocol):
            """Keys"""

            lights: Final = "PowerLed"

    __slots__ = ()

    _get_value: providers.FactoryValue[Value.JSON]
    _value: Value.JSON

    def _get_lights(self, create=False) -> Value.Lights.JSON:
        return self.lookup_value(
            self._get_value,
            self.Value.Keys.lights,
            create=create,
            default=None,
        )

    @property
    def _lights(self):
        return self._get_lights()

    @property
    def channel_id(self):
        if value := self._lights:
            return value.get(self.Value.Lights.Keys.channel_id, 0)
        return 0

    @property
    def state(self):
        if value := self._lights:
            return led_typing.LightStates(value.get(LightStateKeys.state, _DefaultLightState))
        return _DefaultLightState


class SetPowerLedRequest(Request, led.SetPowerLedRequest):
    """REST Set Power LED"""

    __slots__ = ()

    class Parameter(GetPowerLedResponse.Value, Protocol):
        """Parameter"""

    COMMAND: Final = "SetPowerLed"
    _COMMAND_ID: Final = hash(COMMAND)

    def __init__(
        self,
        /,
        state: led_typing.LightStates = ...,
        channel_id: int = ...,
        response_type: ResponseTypes = ...,
    ):
        super().__init__(
            command=type(self).COMMAND, channel_id=channel_id, response_type=response_type
        )
        if state and state is not ...:
            self.state = state

    @property
    def id(self):
        return self._COMMAND_ID ^ self.channel_id

    _get_parameter: providers.FactoryValue[Parameter.JSON]
    _parameter: Parameter.JSON

    def _get_lights(self, create=False) -> Parameter.Lights.JSON:
        return self.lookup_value(
            self._get_parameter,
            self.Parameter.Keys.lights,
            create=create,
            default_factory=lambda: dict() if create else None,
        )

    @property
    def _lights(self):
        return self._get_lights()

    @GetPowerLedResponse.channel_id.setter
    def channel_id(self, value):
        self._get_lights(True)[self.Parameter.Lights.Keys.channel_id] = int(value)

    @GetPowerLedResponse.state.setter
    def state(self, value):
        self._get_lights(True)[self.Parameter.Lights.Keys.state] = int(value)


class GetWhiteLedRequest(RequestWithChannel, led.GetWhiteLedRequest):
    """REST Get White LED"""

    __slots__ = ()

    COMMAND: Final = "GetWhiteLed"
    _COMMAND_ID: Final = hash(COMMAND)

    def __init__(self, /, channel_id: int = ..., response_type: ResponseTypes = ...):
        super().__init__(
            command=type(self).COMMAND, channel_id=channel_id, response_type=response_type
        )

    @property
    def id(self):
        return self._COMMAND_ID ^ self.channel_id


class _WhiteLedRange(providers.Value[dict[str, any]]):
    class JSON(TypedDict):
        """JSON"""

        bright: model.MinMaxRange.JSON

    class Keys(Protocol):
        """Keys"""

        brightness: Final = "bright"

    __slots__ = ()

    __get_value__: providers.FactoryValue[JSON]

    @property
    def brightness(self):
        return model.MinMaxRange(
            self.lookup_factory(self.__get_value__, self.Keys.brightness, default=None)
        )


class GetWhiteLedResponse(RestCommandResponse, led.GetWhiteLedResponse):
    """REST Get White LED Response"""

    @classmethod
    def from_response(cls, response: any, /, request: Request | None = None, **kwargs):
        if super().is_response(response, GetWhiteLedRequest.COMMAND):
            return cls(response, request_id=request.id if request else None, **kwargs)
        return None

    class Value(Protocol):
        """Value"""

        class Lights(Protocol):
            """Lights"""

            class JSON(RequestWithChannel.Parameter.JSON, local_model.WhiteLedInfo.JSON):
                """JSON"""

            class Keys(RequestWithChannel.Parameter.Keys, local_model.WhiteLedInfo.Keys, Protocol):
                """Keys"""

        class JSON(TypedDict):
            """JSON"""

            WhiteLed: "GetWhiteLedResponse.Value.Lights.JSON"

        class Keys(Protocol):
            """Keys"""

            lights: Final = "WhiteLed"

    class Range(Value, Protocol):
        """Range Values"""

        class JSON(TypedDict):
            """JSON"""

            WhiteLed: _WhiteLedRange.JSON

    __slots__ = ()

    _get_value: providers.FactoryValue[Value.JSON]
    _value: Value.JSON

    _get_initial: providers.FactoryValue[Value.JSON]
    _initial: Value.JSON

    _get_range: providers.FactoryValue[Range.JSON]
    _range: Range.JSON

    def _get_lights(self, create=False) -> Value.Lights.JSON:
        return self.lookup_value(
            self._get_value,
            self.Value.Keys.lights,
            create=create,
            default=None,
        )

    @property
    def _lights(self):
        return self._get_lights()

    @property
    def channel_id(self):
        if value := self._lights:
            return value.get(self.Value.Lights.Keys.channel_id, 0)
        return 0

    @property
    def info(self):
        return local_model.WhiteLedInfo(self._get_lights)

    @property
    def initial_info(self):
        return local_model.WhiteLedInfo(
            self.lookup_factory(self._get_initial, self.Value.Keys.lights, default=None)
        )

    @property
    def info_range(self):
        return _WhiteLedRange(
            self.lookup_factory(self._get_range, self.Range.Keys.lights, default=None)
        )


class SetWhiteLedRequest(Request, led.SetWhiteLedRequest):
    """REST Set White LED"""

    class Parameter(GetWhiteLedResponse.Value, Protocol):
        """Parameter"""

    __slots__ = ()

    COMMAND: Final = "SetWhiteLed"
    _COMMAND_ID: Final = hash(COMMAND)

    def __init__(
        self,
        /,
        info: led_typing.WhiteLedInfo = ...,
        channel_id: int = ...,
        response_type: ResponseTypes = ...,
    ):
        super().__init__(command=type(self).COMMAND, response_type=response_type)
        if channel_id is not ...:
            self.channel_id = channel_id
        if info and info is not ...:
            self.info = info

    @property
    def id(self):
        return self._COMMAND_ID ^ self.channel_id

    _get_parameter: providers.FactoryValue[Parameter.JSON]
    _parameter: Parameter.JSON

    def _get_lights(self, create=False) -> Parameter.Lights.JSON:
        return self.lookup_value(
            self._get_parameter,
            self.Parameter.Keys.lights,
            create=create,
            default_factory=lambda: dict() if create else None,
        )

    @property
    def _lights(self):
        return self._get_lights()

    @property
    def channel_id(self):
        if value := self._lights:
            return value.get(
                self.Parameter.Lights.Keys.channel_id, RequestWithChannel.DEFAULT_CHANNEL
            )
        return RequestWithChannel.DEFAULT_CHANNEL

    @channel_id.setter
    def channel_id(self, value):
        if not value:
            value = RequestWithChannel.DEFAULT_CHANNEL
        self._get_lights(True)[self.Parameter.Lights.Keys.channel_id] = int(value)

    @property
    def info(self):
        return local_model.MutableWhiteLedInfo(self._get_lights)

    @info.setter
    def info(self, value: led_typing.WhiteLedInfo):
        self.info.update(value)
