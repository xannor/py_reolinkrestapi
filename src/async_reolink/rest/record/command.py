"""REST Record Commands"""

from typing import Callable, Final, Protocol, Sequence, TypeVar, TypedDict
from async_reolink.api.record import command as record
from async_reolink.api.record import typing

from .._utilities import providers

from .model import MutableSearch, SearchStatus, File


from ..connection.model import (
    Request,
    RequestWithChannel,
    Response as RestResponse,
    ResponseTypes,
)

# pylint:disable=missing-function-docstring


class GetSnapshotRequest(RequestWithChannel, record.GetSnapshotRequest):
    """REST Get Snaposhot Request"""

    COMMAND: Final = "Snap"
    _COMMAND_ID: Final = hash(COMMAND)

    def __init__(
        self,
        channel_id: int = 0,
        response_type: ResponseTypes = ResponseTypes.VALUE_ONLY,
    ):
        super().__init__()
        self.command = type(self).COMMAND
        self.response_type = response_type
        self.channel_id = channel_id

    @property
    def raw_parameter(self):
        return self._parameter

    @property
    def id(self):
        return self._COMMAND_ID ^ self.channel_id


class SearchRecordingsRequest(Request, record.SearchRecordingsRequest):
    """REST Search Recordings Request"""

    class Parameter(Protocol):
        """Parameter"""

        class Search(Protocol):
            """Search"""

            class JSON(RequestWithChannel.Parameter.JSON, MutableSearch.JSON):
                """JSON"""

            class Keys(RequestWithChannel.Parameter.Keys, MutableSearch.Keys, Protocol):
                """Keys"""

        class JSON(TypedDict):
            """JSON"""

            Search: "SearchRecordingsRequest.Parameter.Search.JSON"

        class Keys(Protocol):
            """Keys"""

            search: Final = "Search"

    COMMAND: Final = "Search"

    _parameter: Parameter.JSON

    def __init__(
        self,
        channel_id: int = 0,
        response_type: ResponseTypes = ResponseTypes.VALUE_ONLY,
    ):
        super().__init__()
        self.command = type(self).COMMAND
        self.response_type = response_type
        self.channel_id = channel_id

    def _get_search(self, create=False):
        if not (value := self._get_parameter(create)):
            return None
        if not (search := value.get(self.Keys.parameter)) and create:
            search: dict = value.setdefault(self.Keys.parameter, {})
        return search

    _search: Parameter.Search.JSON = property(_get_search)

    @property
    def channel_id(self):
        if value := self._search:
            return value.get(self.Parameter.Search.Keys.channel_id, 0)
        return 0

    @channel_id.setter
    def channel_id(self, value):
        self._get_search(True)[self.Parameter.Search.Keys.channel_id] = int(value)

    @property
    def search(self):
        return MutableSearch(self._get_search)

    @search.setter
    def search(self, value):
        self.search.update(value)


_T = TypeVar("_T")


class _FactorySequence(providers.ListProvider[any], Sequence[_T]):

    __slots__ = ("__factory",)

    def __init__(
        self,
        value: providers.ProvidedList[any],
        factory: Callable[[providers.ProvidedValue[any] | None], _T],
    ) -> None:
        super().__init__(value)
        self.__factory = factory

    def _get_item(self, __k: int) -> dict:
        return value[__k] if (value := self._value) is not None else None

    def __getitem__(self, __k: int):
        def _factory():
            return self._get_item(__k)

        return self.__factory(_factory)

    def __len__(self):
        if (_list := self._value) is None:
            return 0
        return len(_list)


class SearchRecordingsResponse(RestResponse, record.SearchRecordingsResponse):
    """REST Search Results"""

    @classmethod
    def from_response(cls, response: any, /, request: Request | None = None, **kwargs):
        if super().is_response(response, SearchRecordingsRequest.COMMAND):
            return cls(response, request_id=request.id if request else None, **kwargs)
        return None

    class Value(Protocol):
        """Value"""

        class SearchResult(Protocol):
            """Search Result"""

            class JSON(RequestWithChannel.Parameter.JSON):
                """JSON"""

                Status: list[SearchStatus.JSON]
                File: list[File.JSON]

            class Keys(RequestWithChannel.Parameter.Keys, Protocol):
                """Keys"""

                status: Final = "Status"
                files: Final = "File"

        class JSON(TypedDict):
            """JSON"""

            SearchResult: "SearchRecordingsResponse.Value.SearchResult.JSON"

        class Keys(Protocol):
            """Keys"""

            search_result: Final = "SearchResult"

    __slots__ = ()

    _value: Value.JSON

    def _get_search_result(self, create=False) -> dict:
        if value := self._get_provided_value(create):
            return value.get(self.Value.Keys.search_result)
        return None

    _search_result: Value.SearchResult.JSON = property(_get_search_result)

    @property
    def channel_id(self):
        if value := self._search_result:
            return value.get(self.Value.SearchResult.Keys.channel_id, 0)
        return 0

    @property
    def status(self):
        return _FactorySequence(lambda _: self._search_result, SearchStatus)

    @property
    def files(self):
        return _FactorySequence(lambda _: self._search_result, File)
