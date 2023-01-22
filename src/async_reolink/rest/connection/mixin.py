"""REST Connection"""
from __future__ import annotations
from functools import partial

import inspect
from json import JSONDecoder, dumps as _DEFAULT_JSON_ENCODER, loads as DEFAULT_JSON_DECODER
import logging
from typing import (
    Final,
    overload,
)
import aiohttp

from async_reolink.api.connection.model import (
    Response,
    Request,
)
from async_reolink.api.connection.mixin import Connection as BaseConnection

from async_reolink.api import errors

from async_reolink.api.const import DEFAULT_TIMEOUT
from .._utilities.json import SmarterJSONEncoder

from ..const import DEFAULT_HTTP_PORT, DEFAULT_HTTPS_PORT

from .model import Response as RestResponse, ErrorResponse, ResponseWithCode
from ..connection.typing import Encryption, SSLContextFactory, SessionFactory, WithConnection

from ..errors import CONNECTION_ERRORS, RESPONSE_ERRORS

_LOGGER = logging.getLogger(__name__)
_LOGGER_DATA = logging.getLogger(__name__ + ".data")

DEFAULT_JSON_ENCODER: Final = partial(_DEFAULT_JSON_ENCODER, cls=SmarterJSONEncoder)


def _default_create_session(base_url: str, timeout: int, ssl: SSLContextFactory = None):
    return aiohttp.ClientSession(
        base_url=base_url,
        json_serialize=DEFAULT_JSON_ENCODER,
        timeout=aiohttp.ClientTimeout(total=timeout),
        connector=aiohttp.TCPConnector(ssl=ssl(base_url) if ssl is not None else None),
    )


class Connection(BaseConnection, WithConnection):
    """REST Connection"""

    def __init__(
        self,
        *args,
        session: SessionFactory | None = None,
        ssl: SSLContextFactory | None = None,
        loads: JSONDecoder = DEFAULT_JSON_DECODER,
        **kwargs,
    ):
        self._force_get_callbacks = []
        # self._response_callback: list[Callable[[CommandResponse], None]]
        super().__init__(*args, **kwargs)
        self.__session: aiohttp.ClientSession | None = None
        self.__session_factory: SessionFactory = session or _default_create_session
        self.__ssl_context: SSLContextFactory = ssl
        self.__base_url = ""
        self.__hostname = ""
        self.__connection_id = 0
        self.__loads = loads

    def _create_session(self, timeout: int):
        return self.__session_factory(self.__base_url, timeout, self.__ssl_context)

    @property
    def is_connected(self):
        """is connected"""
        return self.__connection_id != 0

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

    @property
    def commands(self):
        return self.__commands

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
        if port == DEFAULT_HTTPS_PORT or (port is None and encryption == Encryption.HTTPS):
            https = True
            port = None
        elif port == DEFAULT_HTTP_PORT and encryption != Encryption.HTTPS:
            https = False
            port = None
        else:
            https = encryption == Encryption.HTTPS

        scheme = "https" if https is True else "http"
        _port = f":{port}" if port is not None else ""
        url = f"{scheme}://{hostname}{_port}"
        _id = hash(url)
        if _id == self.__connection_id:
            return True
        if self.__connection_id != 0:
            await self.disconnect()

        self.__base_url = url
        self.__connection_id = _id
        self.__hostname = hostname
        self.__session = self._create_session(timeout)

        async with self.__session.get("/") as response:
            await response.text()

        for callback in self._connect_callbacks:
            if inspect.iscoroutinefunction(callback):
                await callback()
            else:
                callback()

        return True

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

    def __process_response(self, value: any, request: Request = None) -> Response | None:
        if not RestResponse.is_response(value):
            raise errors.ReolinkResponseError("Invalid response from device")
        response = Response.from_response(value, request)
        if isinstance(response, ErrorResponse):
            for callback in self._error_handlers:
                if callback(response):
                    return None

        # for handler in self._response_callback:
        #    handler(response)
        return response

    async def __execute(self, *args: Request):
        if not self.is_connected:
            return

        if len(args) == 0:
            return
        use_get = False
        query = {}
        url = "/cgi-bin/api.cgi"
        for callback in self._force_get_callbacks:
            if inspect.iscoroutinefunction(callback):
                cb_result = await callback(url, query, args)
            else:
                cb_result = callback(url, query, args)

            if cb_result:
                if isinstance(cb_result, tuple) and len(cb_result) == 2:
                    if not use_get:
                        use_get = bool(cb_result[0])
                    url = str(cb_result[1])
                elif isinstance(cb_result, str):
                    url = cb_result
                elif not use_get:
                    use_get = True

        headers = {"Accept": "*/*", "Content-Type": "application/json"}

        cleanup = True
        response = None
        context = None

        def _cleanup():
            nonlocal response, context
            if response:
                response.close()
            response = None
            if context:
                context.close()
            context = None

        try:
            encrypted = False
            if use_get:
                _LOGGER_DATA.debug("GET: %s<-%s", url, query)
                context = self.__session.get(
                    url,
                    params=query,
                    headers=headers,
                    allow_redirects=False,
                )
            else:
                data = self.__session.json_serialize(args)

                _LOGGER_DATA.debug("%s<-%s", url, data)
                context = self.__session.post(
                    url,
                    data=data,
                    headers=headers,
                    allow_redirects=False,
                )

            response = await context
            if response.status >= 300:
                _LOGGER.error("got redirect (%d) response code", response.status)
                raise aiohttp.ClientResponseError(
                    response.request_info,
                    [response],
                    status=response.status,
                    headers=response.headers,
                )
            if response.status >= 500:
                _LOGGER.error("got critical (%d) response code", response.status)
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
        except CONNECTION_ERRORS:
            raise
        except RESPONSE_ERRORS:
            raise
        except Exception as unhandled_error:
            _LOGGER.error("unhandled exception")
            raise errors.ReolinkUnhandledError() from unhandled_error
        finally:
            if cleanup:
                _cleanup()

        if not response:
            return

        if "json" in response.content_type:
            try:
                command_responses = await response.json()
            finally:
                _cleanup()
        elif "text" in response.content_type:
            try:
                command_responses = await response.text()
            finally:
                _cleanup()

            if command_responses[0] != "[":
                _LOGGER.error("did not get json as response: (%s)", data)
                raise errors.ReolinkResponseError(
                    code=errors.ErrorCodes.PROTOCOL_ERROR,
                    details="invalid response",
                )

            command_responses = self.__loads(command_responses)
        else:
            try:
                async for chunk in response.content.iter_any():
                    yield chunk
            finally:
                _cleanup()
            return

        if not isinstance(command_responses, list):
            command_response = self.__process_response(command_responses, args[0])
            if command_response is not None:
                yield command_response
            return

        _LOGGER_DATA.debug(
            "%s%s->%s", self.__hostname, "(D)" if encrypted else "", command_responses
        )

        for i, command_response in enumerate(command_responses):
            command_response = self.__process_response(command_response, args[i])
            if command_response is not None:
                yield command_response

    def _execute(self, *args: Request):
        """Internal API"""

        return self.__execute(*args)

    def _has_response_code(self, response: Response):
        return isinstance(response, ResponseWithCode)

    def _is_success_response(self, response: Response):
        return isinstance(response, ResponseWithCode)
