"""REST Record"""

from dataclasses import dataclass
from typing import Final
from reolinkapi.commands import (
    CommandRequestWithParam, CommandChannelParameter, CommandRequestTypes
)
from reolinkapi.record import Record as BaseRecord
from .seed import Seed

from . import connection

class Record(BaseRecord):
    """Record Mixin"""

    async def get_snap(self, channel: int = 0):
        """get snapshot"""

        if isinstance(self, connection.Connection):
            response = await self._execute_request(
                SnapshotCommand(Seed(), channel),
                use_get=True,  # Duo repeats channel 0 with a post snap request
            )

        else:
            return None

        if response is None:
            return None

        try:
            return await response.read()
        finally:
            response.close()

@dataclass
class SnapshotRequestParameter(CommandChannelParameter):
    """Snapshot Command Request Parameter"""

    rs: str

class SnapshotCommand(CommandRequestWithParam[SnapshotRequestParameter]):
    """Get Snapshot"""

    COMMAND:Final = ""

    def __init__(self, channel:int=0, rs:str=None, requestType:CommandRequestTypes=CommandRequestTypes.VALUE_ONLY):
        super().__init__(type(self).COMMAND, requestType, SnapshotRequestParameter(channel, rs))
