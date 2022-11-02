"""REST Security"""

from __future__ import annotations
from time import time
from typing import Sequence
from urllib.parse import quote_plus

from async_reolink.api.security.mixin import Security as BaseSecurity

from ..connection.typing import WithConnection

from ..connection.models import CommandRequest
from .command import (
    LoginRequest,
    LoginResponse,
)

from .typing import WithSecurity


class Security(BaseSecurity, WithConnection, WithSecurity):
    """REST security mixin"""

    def __init__(self, *args, **kwargs) -> None:
        self.__token = ""
        self.__uri_token = ""
        super().__init__(*args, **kwargs)
        self._force_get_callbacks.append(self.__force_get_login)
        self.__token_expires: float = 0
        self.__last_pwd_hash = 0

    def __force_get_login(self, url: str, _: dict[str, str], commands: Sequence[CommandRequest]):
        if len(commands) > 1 or not isinstance(commands[0], LoginRequest):
            if self.__token:
                return (False, url + f"?token={self.__uri_token}")
            return
        return url + f"?cmd={commands[0].command}"

    @property
    def _auth_token(self):
        return self.__token

    @property
    def is_authenticated(self) -> bool:
        # we use a 1s offest to give time for simple checks to do an operation
        return bool(self.__token) and self.authentication_timeout > 1

    @property
    def authentication_timeout(self):
        return self.__token_expires - time()

    @property
    def authentication_id(self):
        return self.__last_pwd_hash

    async def _prelogin(self, username: str):
        # keep hash of username so we can logout on new info provided
        pwd_hash = hash(username)
        if self.__last_pwd_hash != pwd_hash:
            await self.logout()
            self.__last_pwd_hash = pwd_hash

        if not self.is_connected:
            return False
        return True

    async def _process_login(self, response: LoginResponse) -> bool:
        token = response.token

        self.__token = token.name
        self.__uri_token = quote_plus(self.__token)
        self.__token_expires = time() + token.lease_time

        return True

    def _clear_login(self):
        self.__token = ""
        self.__uri_token = ""
        self.__token_expires = 0
