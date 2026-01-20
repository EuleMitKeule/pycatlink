"""Device module for CatLink integration."""

from typing import Any

from .client import CatlinkApiClient
from .const import (
    PARAMETER_DEVICE_ID,
    HttpMethod,
)
from .models import CatlinkDeviceInfo


class CatlinkDevice:
    """Device class for CatLink integration."""

    def __init__(
        self,
        device_info: CatlinkDeviceInfo,
        client: CatlinkApiClient,
    ) -> None:
        """Initialize the device."""
        self.device_info = device_info
        self._client = client

    async def refresh(self) -> None:
        """Refresh the device data."""

    async def _issue_command(
        self,
        path: str,
        parameters: dict[str, Any],
    ) -> None:
        """Issue a command to the device."""
        await self._client.request_with_return_code(
            path=path,
            method=HttpMethod.POST,
            parameters={
                PARAMETER_DEVICE_ID: self.device_info.id,
                **parameters,
            },
        )

        await self.refresh()
