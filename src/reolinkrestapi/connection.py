"""REST Connection"""
from __future__ import annotations
import asyncio
from dataclasses import asdict

from enum import IntEnum
import inspect
from json import JSONDecoder, loads as DEFAULT_JSON_DECODER
import logging
from typing import Callable, Protocol, overload
from urllib.parse import urlparse
import aiohttp

from reolinkapi.commands import CommandResponse, CommandRequest, CommandRequestWithParam
from reolinkapi.connection import Connection as BaseConnection
from reolinkapi.security import Security as BaseSecurity, LoginRequest

from reolinkapi import errors

from reolinkapi.const import DEFAULT_TIMEOUT

_LOGGER = logging.getLogger(__name__)
_LOGGER_DATA = logging.getLogger(__name__ + ".data")


class SessionFactory(Protocol):
    """Session Factory"""

    def __call__(self, base_url: str, timeout: int) -> aiohttp.ClientSession:
        ...


def _default_create_session(base_url: str, timeout: int):
    return aiohttp.ClientSession(
        base_url=base_url,
        timeout=aiohttp.ClientTimeout(total=timeout),
        connector=aiohttp.TCPConnector(ssl=False),
    )


class Encryption(IntEnum):
    """Connection Encryption"""

    NONE = 0
    HTTPS = 1

PROCESS_RESPONSES_CALLBACK_TYPE = Callable[[list[CommandResponse]], None] #pylint: disable=invalid-name

class Connection(BaseConnection):
    """REST Connection"""

    def __init__(self, *args, session_factory: SessionFactory = None, loads: JSONDecoder = DEFAULT_JSON_DECODER, **kwargs):
        self._process_responses_callbacks: list[PROCESS_RESPONSES_CALLBACK_TYPE] = [
        ]
        super().__init__(*args, **kwargs)
        self.__session: aiohttp.ClientSession | None = None
        self.__session_factory: SessionFactory = (
            session_factory or _default_create_session
        )
        self.__base_url = ""
        self.__hostname = ""
        self.__connection_id = 0
        self.__loads = loads

    def _create_session(self, timeout: int):
        return self.__session_factory(self.__base_url, timeout)

    @property
    def connection_id(self):
        """connection id"""
        return self.__connection_id

    @property
    def base_url(self):
        """base url"""
        return self.__base_url

    @property
    def secured(self):
        """Secure connection"""
        return self.__base_url.startswith("https:")

    @property
    def hostname(self):
        """hostname"""
        return self.__hostname

    @overload
    async def connect(
        self,
        hostname: str,
        port: int = None,
        timeout: float = DEFAULT_TIMEOUT,
        *,
        encryption: Encryption = Encryption.NONE,
    ):  # pylint: disable=arguments-differ
        ...

    async def connect(
        self,
        hostname: str,
        port: int = None,
        timeout: float = DEFAULT_TIMEOUT,
        **kwargs,
    ):
        """setup connection to device"""
        encryption = kwargs.get("encryption", Encryption.NONE)
        if port == 443 or (port is None and encryption == Encryption.HTTPS):
            https = True
            port = None
        elif port == 80 and encryption != Encryption.HTTPS:
            https = False
            port = None
        else:
            https = encryption == Encryption.HTTPS
        await self._setup_connection(
            hostname, port, timeout, https, False
        )

    async def _setup_connection(
        self,
        hostname: str,
        port: int | None,
        timeout: float,
        https: bool,
        full_reset: bool = True,
    ):
        scheme = "https" if https is True else "http"
        _port = f":{port}" if port is not None else ""
        url = f"{scheme}://{hostname}{_port}"
        _id = hash(url)
        if _id == self.__connection_id:
            return
        if self.__connection_id != 0:
            if full_reset:
                await self.disconnect()
            else:
                await self.__session.close()

        self.__base_url = url
        self.__connection_id = _id
        self.__hostname = hostname
        self.__session = self._create_session(timeout)

    async def disconnect(self):
        """disconnect from device"""

        if self.__session is None:
            return
        for callback in self._disconnect_callbacks:
            if inspect.iscoroutinefunction(callback):
                await callback()
            else:
                callback()
        if not self.__session.closed:
            await self.__session.close()
        self.__connection_id = 0
        self.__base_url = ""
        self.__hostname = ""
        self.__session = None

    def _ensure_connection(self):
        if self.__session is None:
            return False

        if self.__session.closed:
            self.__session = self._create_session(self.__session.timeout.total)

        return True

    async def _execute_request(
        self, *args: CommandRequest, use_get: bool = False
    ) -> aiohttp.ClientResponse | None:
        """Internal API"""

        if not self._ensure_connection():
            return None

        if len(args) == 0:
            return None
        query = {"cmd": args[0].cmd}
        if use_get and isinstance(args[0], CommandRequestWithParam):
            query.update(asdict(args[0].param))
        url = "/cgi-bin/api.cgi"
        if args[0].cmd == LoginRequest.COMMAND:
            url += f'?cmd={args[0].cmd}'
        elif isinstance(self, BaseSecurity):
            if self._auth_token != "":
                url += f"?token={self._auth_token}"
        count = None

        headers = {"Accept": "*/*", "Content-Type": "application/json"}

        cleanup = True
        response = None
        context = None
        try:
            encrypted = False
            if use_get:
                _LOGGER.debug("GET: %s<-%s", url, query)
                context = self.__session.get(
                    url,
                    params=query,
                    headers=headers,
                    allow_redirects=False,
                )
            else:
                data = self.__session.json_serialize(map(asdict, args))

                _LOGGER_DATA.debug(
                    "%s%s<-%s", self.__hostname, "(E)" if encrypted else "", data
                )
                context = self.__session.post(
                    url,
                    data=data,
                    headers=headers,
                    allow_redirects=False,
                )

            response = await context
            if count is not None:
                count.free = True
            if response.status in (302, 301) and "location" in response.headers:
                location = response.headers["location"]
                redir = urlparse(location)
                base = urlparse(self.__base_url)
                if (
                    base.scheme != redir.scheme
                    and base.scheme == "http"
                    or redir.scheme == "http"
                ):
                    if redir.scheme == "http":
                        _LOGGER.warning(
                            "Got http redirect from camera (%s), please verify configuration",
                            self.__base_url,
                        )
                        await self._setup_connection(
                            redir.hostname,
                            redir.port,
                            self.__session.timeout.total,
                            False,
                            True,
                        )
                    else:
                        _LOGGER.warning(
                            "Got https redirect from camera (%s), please verify configuration",
                            self.__base_url,
                        )
                        await self._setup_connection(
                            redir.hostname,
                            redir.port,
                            self.__session.timeout.total,
                            True,
                            True,
                        )
                    return await self._execute_request(*args)

                _LOGGER.error(
                    "got unexpected redirect from camera (%s), please verify configurtation",
                    self.__base_url,
                )
                raise aiohttp.ClientResponseError(
                    response.request_info,
                    [response],
                    status=response.status,
                    headers=response.headers,
                )

            if response.status >= 500:
                _LOGGER.error("got critical (%d) response code",
                              response.status)
                raise aiohttp.ClientResponseError(
                    response.request_info,
                    [response],
                    status=response.status,
                    headers=response.headers,
                )
            if response.status >= 400:
                _LOGGER.error("got auth (%d) response code", response.status)
                raise aiohttp.ClientResponseError(
                    response.request_info,
                    [response],
                    status=response.status,
                    headers=response.headers,
                )

            cleanup = False

            return response
        except aiohttp.ClientConnectorError as http_error:
            _LOGGER.error("connection error (%s)", http_error)
            raise errors.ReolinkConnectionError() from http_error
        except asyncio.TimeoutError as timeout_error:
            _LOGGER.error("timeout")
            raise errors.ReolinkTimeoutError() from timeout_error
        except aiohttp.ClientResponseError as response_error:
            raise errors.ReolinkResponseError() from response_error
        except Exception as unhandled_error:
            _LOGGER.error("unhandled exception")
            raise errors.ReolinkUnhandledError() from unhandled_error
        finally:
            if cleanup:
                if response is not None:
                    response.close()
                if context is not None:
                    context.close()

    async def _process_response(
        self, response: aiohttp.ClientResponse
    ) -> list[CommandResponse]:
        if response is None:
            return []

        try:
            data = await response.text()
            decrypted = False

            if data[0] != "[":
                _LOGGER.error("did not get json as response: (%s)", data)
                raise errors.ReolinkResponseError()

            # handle json over text/html (missing accept?)
            data = self.__loads(data)

        finally:
            response.close()

        if not isinstance(data, list):
            data = [data]
        _LOGGER_DATA.debug("%s->%s", "D" if decrypted else "", data)

        for callback in self._process_responses_callbacks:
            if inspect.iscoroutinefunction(callback):
                await callback(data)
            else:
                callback(data)

        return data

    @overload
    async def _execute(
        self, *args: CommandRequest, use_get: True
    ):  # pylint: disable=arguments-differ
        ...

    async def _execute(self, *args: CommandRequest, **kwargs):
        """Internal API"""
        use_get = kwargs.get("use_get", False)
        return await self._process_response(
            await self._execute_request(*args, use_get=use_get)
        )
