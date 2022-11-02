"""REST Command Factory"""

from typing import TypeGuard

from async_reolink.api.connection.typing import CommandResponse

from .ai.command import CommandFactory as AI
from .alarm.command import CommandFactory as Alarm
from .connection.models import CommandErrorResponse
from .connection.models import CommandRequest as RestCommandRequest
from .connection.models import CommandResponse as RestCommandResponse
from .connection.models import CommandResponseTypes, CommandResponseWithCode
from .encoding.command import CommandFactory as Encoding
from .led.command import CommandFactory as LED
from .network.command import CommandFactory as Network
from .ptz.command import CommandFactory as PTZ
from .record.command import CommandFactory as Record
from .security.command import CommandFactory as Securty
from .system.command import CommandFactory as System


class CommandFactory(AI, Alarm, Encoding, LED, Network, PTZ, Record, Securty, System):
    """REST Command Factory"""

    def is_request(self, request: any) -> TypeGuard[RestCommandRequest]:
        return isinstance(request, RestCommandRequest)

    def is_response(self, response: any) -> TypeGuard[RestCommandResponse]:
        return isinstance(response, RestCommandResponse)

    def is_error(self, response: CommandResponse) -> TypeGuard[CommandErrorResponse]:
        return isinstance(response, CommandErrorResponse)

    def is_success(self, response: CommandResponse) -> TypeGuard[CommandResponseWithCode]:
        return isinstance(response, CommandResponseWithCode)

    @property
    def response_types(self) -> type[CommandResponseTypes]:
        return CommandResponseTypes
