"""Account module for CatLink API."""

from .c08 import CatlinkC08Device
from .client import CatlinkApiClient
from .const import (
    API_DEVICE_LIST,
    PARAMETER_TYPE,
    RESPONSE_KEY_DATA,
    RESPONSE_KEY_DEVICES,
    TYPE_NONE,
    HttpMethod,
)
from .device import CatlinkDevice
from .models import CatlinkAccountConfig, CatlinkDeviceInfo


class CatlinkAccount:
    """Account class for CatLink integration."""

    def __init__(self, config: CatlinkAccountConfig) -> None:
        """Initialize the account."""
        self.config = config

        self._client = CatlinkApiClient(config)

    async def get_devices(
        self,
    ) -> list[CatlinkDevice | CatlinkC08Device]:
        """Get the list of devices associated with the account."""
        response = await self._client.request_with_auto_login(
            path=API_DEVICE_LIST,
            method=HttpMethod.GET,
            parameters={
                PARAMETER_TYPE: TYPE_NONE,
            },
        )
        device_infos = [
            CatlinkDeviceInfo.from_dict(response_element)
            for response_element in response.get(RESPONSE_KEY_DATA, {}).get(
                RESPONSE_KEY_DEVICES, []
            )
        ]

        return [self._create_device(device_info) for device_info in device_infos]

    def _create_device(
        self, device_info: CatlinkDeviceInfo
    ) -> CatlinkDevice | CatlinkC08Device:
        """Create the appropriate device instance based on device type."""
        if not device_info.device_type:
            return CatlinkDevice(device_info, self._client)

        device_type_upper = device_info.device_type.upper()

        if device_type_upper == "C08":
            return CatlinkC08Device(device_info, self._client)

        return CatlinkDevice(device_info, self._client)
