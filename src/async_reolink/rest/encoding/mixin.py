"""REST Encoding"""

from async_reolink.api.encoding.mixin import Encoding as BaseEncoding

from ..connection.model import Response
from . import command as encoding


class Encoding(BaseEncoding):
    """REST Encoding Mixin"""

    def _create_get_encoding(self, channel_id: int):
        return encoding.GetEncodingRequest(channel_id=channel_id)

    def _is_get_encoding_response(self, response: Response):
        return isinstance(response, encoding.GetEncodingResponse)
