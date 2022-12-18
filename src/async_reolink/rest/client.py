""" ReoLink REST Client """

from async_reolink.api.client import Client as BaseClient

from .connection.typing import SSLContextFactory, SessionFactory

from .ai.mixin import AI

from .alarm.mixin import Alarm

from .encoding.mixin import Encoding

from .led.mixin import LED

from .network.mixin import Network

from .security.mixin import Security

from .system.mixin import System

from .connection.mixin import Connection

from .record.mixin import Record

from .__version__ import __version__


class Client(Connection, AI, Alarm, Encoding, LED, Security, Network, Record, System, BaseClient):
    """Rest API Client"""
