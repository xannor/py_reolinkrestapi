""" ReoLink REST API """

from reolinkapi.parts.led import LED
from reolinkapi.parts.network import Network
from reolinkapi.parts.system import System
from reolinkapi.parts.video import Video
from reolinkapi.parts.encoding import Encoding
from reolinkapi.parts.alarm import Alarm
from reolinkapi.parts.ai import AI
from reolinkapi.parts.security import Security
from .parts.connection import Connection, SessionFactory
from .parts.record import Record

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
