""" ReoLink REST Client """

from async_reolink.api.client import Client as BaseClient

from .connection.typing import SSLContextFactory, SessionFactory

from .network.mixin import Network

from .security.mixin import Security

from .connection.mixin import Connection

from .record.mixin import Record

from .__version__ import __version__


class Client(Connection, Security, Network, Record, BaseClient):
    """Rest API Client"""

    def __init__(
        self, session_factory: SessionFactory = None, ssl: SSLContextFactory = None
    ) -> None:
        super().__init__(session_factory=session_factory, ssl=ssl)
