"""REST Security"""

from __future__ import annotations
from time import time
from typing import Final, Sequence, TypeGuard
from urllib.parse import quote_plus

from async_reolink.api.connection.model import Response
from async_reolink.api.security.mixin import Security as BaseSecurity

from ..connection.typing import WithConnection

from ..connection.model import Request

from .model import AuthenticationId

from .typing import WithSecurity

from . import command

NO_AUTH: Final = AuthenticationId()


class Security(BaseSecurity, WithConnection, WithSecurity):
    """REST security mixin"""

    def __init__(self, *args, **kwargs) -> None:
        self.__token = ""
        self.__uri_token = ""
        super().__init__(*args, **kwargs)
        self._force_get_callbacks.append(self.__force_get_login)
        self.__token_expires: float = 0
        self.__auth_id = NO_AUTH

    def __force_get_login(self, url: str, _: dict[str, str], commands: Sequence[Request]):
        if len(commands) > 1 or not isinstance(commands[0], command.LoginRequest):
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
        return self.__auth_id

    def _create_authentication_id(self, username: str, password: str = None):
        return AuthenticationId(hash(username), hash(password))

    def _create_login(self, username: str, password: str):
        return command.LoginRequest(user_name=username, password=password)

    def _is_login_response(self, response: Response):
        return isinstance(response, command.LoginResponse)

    async def login(self, username: str = ..., password: str = ...) -> bool:
        if await super().login(username, password):
            self.__auth_id = self._create_authentication_id(username, password)
            return True
        return False

    async def _process_login(self, response: command.LoginResponse) -> bool:
        token = response.token

        self.__token = token.name
        self.__uri_token = quote_plus(self.__token)
        self.__token_expires = time() + token.lease_time

        return True

    def _clear_login(self):
        self.__token = ""
        self.__uri_token = ""
        self.__token_expires = 0
        self.__auth_id = NO_AUTH

    def _create_logout(self):
        return command.LogoutRequest()

    def _create_get_user(self):
        return command.GetUserRequest()

    def _is_get_user_response(self, response: Response):
        return isinstance(response, command.GetUserResponse)
