"""Simple Clear Encryption Support"""
from __future__ import annotations

import base64
from dataclasses import dataclass
import hashlib
from random import SystemRandom
from typing import TypedDict, cast
from typing_extensions import TypeGuard
from cryptography.hazmat.primitives.ciphers import Cipher, BlockCipherAlgorithm
from cryptography.hazmat.primitives.ciphers.algorithms import AES
from cryptography.hazmat.primitives.ciphers.modes import CFB

from ..typings.commands import (
    CommandRequestWithParam,
    CommandRequestTypes,
)
from ..typings.security import LoginTokenV2

from . import connection
from ..helpers import security as securityHelpers

from ..typings.encrypt import DigestInfo

from ..base.connection import Connection as BaseConnection
from ..base.security import Security as BaseSecurity


def _istokenv2(token: securityHelpers.LoginToken) -> TypeGuard[LoginTokenV2]:
    return "checkBasic" in token


class EncryptionLoginRequestParam(TypedDict):
    """Attempt to start an encrypted session"""

    Version: int


class EncrtypedLoginRequestParam(EncryptionLoginRequestParam):
    """Initial Encrypted Login Parameters"""

    Digest: DigestInfo


_IV = "bcswebapp1234567".encode("utf8")

_RND = SystemRandom()


def _create_random_nonce(size: int = 24):
    return _RND.randbytes(size).hex()


@dataclass
class _SyncCount:

    free: bool
    id: int
    val: int


class Encrypt:
    """Encryption Mixin"""

    def __init__(self, *args, **kwargs):
        self.__can_encrypt = True
        super().__init__(*args, **kwargs)
        self.__cipher: Cipher | None = None
        self.__counts: list[_SyncCount] | None = None
        if isinstance(self, BaseConnection):
            self._disconnect_callbacks.append(self.__cleanup_dc)
        if isinstance(self, BaseSecurity):
            self._logout_callbacks.append(self.__cleanup)
        self._can_encrypt = True

    @property
    def encrypted(self):
        """Encryption enabled"""
        return self.__can_encrypt and self.__cipher is not None

    @property
    def _can_encrypt(self):
        return self.__can_encrypt

    @_can_encrypt.setter
    def _can_encrypt(self, value: bool):
        self.__can_encrypt = value

    def __cleanup_dc(self):
        self.__can_encrypt = True

    def __cleanup(self):
        self.__cipher = None
        self.__counts = None

    def _encrypt(self, data: str):
        if self.__cipher is None:
            return data
        context = self.__cipher.encryptor()
        size = int(cast(BlockCipherAlgorithm, self.__cipher.algorithm).block_size / 8)
        edata = context.update(data.encode("utf8"))
        pad = size - (len(edata) % size)
        if pad % 8:
            edata += context.update(bytes(pad))
        edata += context.finalize()
        edata = base64.b64encode(edata)
        return edata.decode("ascii")

    def _decrypt(self, data: str):
        if self.__cipher is None:
            return data

        context = self.__cipher.decryptor()
        ddata = context.update(base64.b64decode(data.encode("ascii")))
        ddata += context.finalize()
        return ddata.decode("utf8")

    def _create_cipher(self, key: str):
        self.__cipher = Cipher(AES(key.encode("ascii")), CFB(_IV))

    def _create_counts(self, value: int, total: int):
        self.__counts = list((_SyncCount(True, index, value) for index in range(total)))

    def _query_data_by_count(self, *args, _id: int | None = None):
        if self.__counts is None:
            return (_SyncCount(True, -1, -1), "")

        is_fixed_id = _id in (0, 1, 2)
        available_counts = list(
            (count for count in self.__counts if is_fixed_id or count.free)
        )
        count = (
            next((count for count in available_counts if count.id == _id), None)
            if _id is not None
            else None
        )
        if count is None:
            free = list(
                (count for count in available_counts if count.id not in (0, 1, 2))
            )
            count = SystemRandom().choice(free)

        query_part = "&".join(args)
        if query_part != "":
            query_part = f"&{query_part}"
        count.val += 1
        count_part = f"countId={count.id}&checkNum={count.val}"

        return (count, self._encrypt(count_part + query_part))

    def _create_nonce(self):
        return _create_random_nonce()

    async def _encrypted_login(self, username: str, password: str):
        response = None
        if isinstance(self, connection.Connection):
            response = await self._execute_request(
                CommandRequestWithParam(
                    cmd=securityHelpers.LOGIN_COMMAND,
                    action=CommandRequestTypes.VALUE_ONLY,
                    param=EncryptionLoginRequestParam(Version=1),
                )
            )

        if response is None or not self.__can_encrypt:
            self.__can_encrypt = False
            return None
        auth = response.headers.get("WWW-Authenticate")
        _comma = (
            (pair.strip() for pair in auth[7:].split(","))
            if auth is not None and auth[0:7] == "Digest "
            else None
        )
        _pairs = (
            ((pair.split("=", 2)) for pair in _comma) if _comma is not None else None
        )
        _clean = (
            ((pair[0].strip(), pair[1].strip().strip('"')) for pair in _pairs)
            if _pairs is not None
            else None
        )
        auth = dict(_clean) if _clean is not None else None
        if auth is None:
            self.__can_encrypt = False
            return None

        digest = cast(DigestInfo, dict())
        digest["Uri"] = response.url.path_qs[1:]
        response.close()
        digest["Realm"] = auth["realm"]
        digest["Qop"] = auth["qop"]
        digest["Nonce"] = auth["nonce"]
        digest["Nc"] = auth["nc"]
        digest["Method"] = response.method

        digest["Cnonce"] = self._create_nonce()

        digest["UserName"] = username
        pwhash = hashlib.md5(
            f'{username}:{digest["Realm"]}:{password}'.encode("utf-8")
        ).hexdigest()
        _hash = hashlib.md5(
            f'{digest["Method"]}:{digest["Uri"]}'.encode("utf-8")
        ).hexdigest()
        digest["Response"] = hashlib.md5(
            f'{pwhash}:{digest["Nonce"]}:{digest["Nc"]}:{digest["Cnonce"]}:{digest["Qop"]}:{_hash}'.encode(
                "utf-8"
            )
        ).hexdigest()
        key = (
            hashlib.md5(
                f'{digest["Nonce"]}-{password}-{digest["Cnonce"]}'.encode("utf-8")
            )
            .hexdigest()[0:16]
            .upper()
        )

        _responses = None
        if isinstance(self, connection.Connection):
            _responses = await self._execute_request(
                CommandRequestWithParam(
                    cmd=securityHelpers.LOGIN_COMMAND,
                    action=CommandRequestTypes.VALUE_ONLY,
                    param=EncrtypedLoginRequestParam(Version=1, Digest=digest),
                )
            )
        if _responses is None:
            return None
        self._create_cipher(key)
        responses = None
        if isinstance(self, connection.Connection):
            responses = await self._process_response(_responses)
        if responses is None:
            return None
        token = next(securityHelpers.login_responses(responses), None)
        if token is not None and _istokenv2(token):
            self._create_counts(
                token["checkBasic"],
                token["countTotal"],
            )

        return responses
