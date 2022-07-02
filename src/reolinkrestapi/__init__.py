""" ReoLink REST API """

from reolinkapi.led import LED
from reolinkapi.network import Network
from reolinkapi.system import System
from reolinkapi.video import Video
from reolinkapi.encoding import Encoding
from reolinkapi.alarm import Alarm
from reolinkapi.ai import AI
from reolinkapi.security import Security
from .connection import Connection, SessionFactory
from .record import Record

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
):
    """Rest API Client"""

    def __init__(self, session_factory: SessionFactory = None) -> None:
        super().__init__(session_factory=session_factory)

__all__ = ["Client"]
