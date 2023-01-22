"""REST System"""

from async_reolink.api.system.mixin import System as BaseSystem

from ..connection.model import Response
from . import command as system


class System(BaseSystem):
    """REST System Mixin"""

    def _create_get_capabilities(self, username: str | None):
        return system.GetAbilitiesRequest(user_name=username)

    def _is_get_capabilities_response(self, response: Response):
        return isinstance(response, system.GetAbilitiesResponse)

    def _create_get_device_info(self):
        return system.GetDeviceInfoRequest()

    def _is_get_device_info_response(self, response: Response):
        return isinstance(response, system.GetDeviceInfoResponse)

    def _create_get_time(self):
        return system.GetTimeRequest()

    def _is_get_time_response(self, response: Response):
        return isinstance(response, system.GetTimeResponse)

    def _create_reboot(self):
        return system.RebootRequest()

    def _create_get_hdd_info(self):
        return system.GetHddInfoRequest()

    def _is_get_hdd_info_response(self, response: Response):
        return isinstance(response, system.GetHddInfoResponse)
