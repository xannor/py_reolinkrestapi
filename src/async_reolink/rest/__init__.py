""" ReoLink REST API """

from async_reolink.api.led import LED
from async_reolink.api.network import Network
from async_reolink.api.system import System
from async_reolink.api.video import Video
from async_reolink.api.encoding import Encoding
from async_reolink.api.alarm import Alarm
from async_reolink.api.ai import AI
from async_reolink.api.ptz import PTZ
from .connection import Connection, SessionFactory
from .record import Record
from .security import Security

from .__version__ import __version__


class Client(
    Connection,
    Security,
    System,
    Network,
    Video,
    Encoding,
    Record,
    Alarm,
    AI,
    LED,
    PTZ,
):
    """Rest API Client"""

    def __init__(self, session_factory: SessionFactory = None) -> None:
        super().__init__(session_factory=session_factory)

#__all__ = ["Client", "__version__"]
