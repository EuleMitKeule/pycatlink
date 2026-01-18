"""Account module for CatLink API."""

from typing import Any

from .client import CatlinkApiClient
from .const import (
    API_DEVICE_LIST,
    DATA_KEY_DEVICES,
    PARAMETER_TYPE,
    RESPONSE_DATA,
    TYPE_NONE,
    HttpMethod,
)
from .device import CatlinkDevice
from .feeder_device import CatlinkFeederDevice
from .litterbox_device import CatlinkLitterBoxDevice
from .models import CatlinkAccountConfig, CatlinkDeviceInfo
from .scooper_device import CatlinkScooperDevice


class CatlinkAccount:
    """Account class for CatLink integration."""

    def __init__(self, config: CatlinkAccountConfig) -> None:
        """Initialize the account."""
        self.config = config

        self._client = CatlinkApiClient(config)

    async def get_devices(
        self,
    ) -> list[
        CatlinkDevice[Any]
        | CatlinkFeederDevice
        | CatlinkLitterBoxDevice
        | CatlinkScooperDevice
    ]:
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
            for response_element in response.get(RESPONSE_DATA, {}).get(
                DATA_KEY_DEVICES
            )
            or []
        ]

        return [self._create_device(device_info) for device_info in device_infos]

    def _create_device(
        self, device_info: CatlinkDeviceInfo
    ) -> (
        CatlinkDevice[Any]
        | CatlinkFeederDevice
        | CatlinkLitterBoxDevice
        | CatlinkScooperDevice
    ):
        """Create the appropriate device instance based on device type."""
        if not device_info.device_type:
            return CatlinkDevice(device_info, self._client)

        device_type_upper = device_info.device_type.upper()

        if "FEEDER" in device_type_upper:
            return CatlinkFeederDevice(device_info, self._client)

        if any(
            x in device_type_upper for x in ["LITTER", "BOX"]
        ) or device_info.device_type in ["C08", "C02", "C03"]:
            return CatlinkLitterBoxDevice(device_info, self._client)

        if "SCOOP" in device_type_upper:
            return CatlinkScooperDevice(device_info, self._client)

        return CatlinkDevice(device_info, self._client)
