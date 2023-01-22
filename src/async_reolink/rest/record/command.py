"""REST Record Commands"""

from typing import Callable, Final, Protocol, Sequence, TypeVar, TypedDict
from async_reolink.api.record import command as record
from async_reolink.api.record import typing as rec_typing

from .._utilities.providers import value as providers

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

    def __init__(self, /, channel_id: int = ..., response_type: ResponseTypes = ...):
        super().__init__(
            command=type(self).COMMAND, channel_id=channel_id, response_type=response_type
        )

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

    _get_parameter: providers.FactoryValue[Parameter.JSON]
    _parameter: Parameter.JSON

    def __init__(
        self,
        /,
        search: record.Search = ...,
        channel_id: int = ...,
        response_type: ResponseTypes = ...,
    ):
        super().__init__(
            command=type(self).COMMAND, channel_id=channel_id, response_type=response_type
        )
        if search and search is not ...:
            self.search = search

    def _get_search(self, create=False) -> Parameter.Search.JSON:
        return self.lookup_value(
            self._get_parameter,
            self.Parameter.Keys.search,
            create=create,
            default_factory=lambda: dict() if create else None,
        )

    @property
    def _search(self):
        return self._get_search()

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


class _FactorySequence(providers.Value[list], Sequence[_T]):

    __slots__ = ("__factory",)

    def __init__(
        self,
        value: providers.FactoryValue[list] | list | None,
        factory: Callable[[providers.FactoryValue[any] | None], _T],
        /,
        **kwargs: any,
    ) -> None:
        super().__init__(value, **kwargs)
        self.__factory = factory

    def __getitem__(self, __k: int):
        return self.__factory(self.lookup_factory(self.__get_value__, __k, default=None))

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

    _get_value: providers.FactoryValue[Value.JSON]
    _value: Value.JSON

    def _get_search_result(self, create=False) -> Value.SearchResult.JSON:
        return self.lookup_value(
            self._get_value, self.Value.Keys.search_result, create=create, default=None
        )

    @property
    def _search_result(self):
        return self._get_search_result()

    @property
    def channel_id(self):
        if value := self._search_result:
            return value.get(self.Value.SearchResult.Keys.channel_id, 0)
        return 0

    @property
    def status(self):
        return _FactorySequence(
            self.lookup_factory(
                self._get_search_result, self.Value.SearchResult.Keys.status, default=None
            ),
            SearchStatus,
        )

    @property
    def files(self):
        return _FactorySequence(
            self.lookup_factory(
                self._get_search_result, self.Value.SearchResult.Keys.files, default=None
            ),
            File,
        )
