"""Device module for CatLink integration."""

from typing import Any, Generic, Type, TypeVar, cast

from .client import CatlinkApiClient
from .const import (
    API_DEVICE_ACTION_COMMAND,
    API_DEVICE_CHANGE_MODE,
    API_DEVICE_INFO,
    API_DEVICE_LOGS,
    DATA_KEY_DEVICE_INFO,
    DATA_KEY_DEVICE_LOG_TOP5,
    PARAMETER_COMMAND,
    PARAMETER_DEVICE_ID,
    PARAMETER_WORK_MODEL,
    RESPONSE_DATA,
    CatlinkAction,
    CatlinkWorkModel,
    HttpMethod,
)
from .exceptions import CatlinkError
from .models import CatlinkDeviceDetails, CatlinkDeviceInfo

T = TypeVar("T", bound=CatlinkDeviceDetails)


class CatlinkDevice(Generic[T]):
    """Device class for CatLink integration."""

    SUPPORTED_MODELS: list[CatlinkWorkModel] = []
    SUPPORTED_ACTIONS: list[CatlinkAction] = []
    DETAILS_CLASS: Type[CatlinkDeviceDetails] = CatlinkDeviceDetails
    PATH_DETAILS = API_DEVICE_INFO
    PATH_SET_MODE = API_DEVICE_CHANGE_MODE
    PATH_SET_ACTION = API_DEVICE_ACTION_COMMAND
    PATH_LOGS = API_DEVICE_LOGS
    RESPONSE_KEY_LOGS = DATA_KEY_DEVICE_LOG_TOP5

    def __init__(
        self,
        device_info: CatlinkDeviceInfo,
        client: CatlinkApiClient,
    ) -> None:
        """Initialize the device."""
        self.device_info = device_info
        self._client = client

        self._device_details: T | None = None
        self._device_logs: list[str] | None = None

    @property
    async def device_details(self) -> T:
        """Return the device details."""
        await self.refresh()

        if not self._device_details:
            raise CatlinkError("Device details not available")

        return self._device_details

    @property
    async def device_logs(self) -> list[str] | None:
        """Return the device logs."""
        await self.refresh()

        if not self._device_logs:
            raise CatlinkError("Device logs not available")

        return self._device_logs

    async def refresh(self) -> None:
        """Refresh the device data."""
        response = await self._client.request_with_auto_login(
            path=self.PATH_DETAILS,
            method=HttpMethod.GET,
            parameters={
                PARAMETER_DEVICE_ID: self.device_info.id,
            },
        )

        self._device_details = cast(
            T,
            self.DETAILS_CLASS.from_dict(
                response.get(RESPONSE_DATA, {}).get(DATA_KEY_DEVICE_INFO, {})
            ),
        )

        response = await self._client.request_with_auto_login(
            path=self.PATH_LOGS,
            method=HttpMethod.GET,
            parameters={
                PARAMETER_DEVICE_ID: self.device_info.id,
            },
        )

        self._device_logs = (
            response.get(RESPONSE_DATA, {}).get(self.RESPONSE_KEY_LOGS, []) or []
        )

    async def set_work_model(self, work_model: CatlinkWorkModel) -> None:
        """Select the device work model."""
        if work_model not in self.SUPPORTED_MODELS:
            raise CatlinkError(f"Work model {work_model} not supported")

        await self._issue_command(
            path=self.PATH_SET_MODE,
            parameters={
                PARAMETER_WORK_MODEL: work_model,
                PARAMETER_DEVICE_ID: self.device_info.id,
            },
        )

    async def select_action(self, action: CatlinkAction) -> None:
        """Select the device action."""
        if action not in self.SUPPORTED_ACTIONS:
            raise CatlinkError(f"Action {action} not supported")

        await self._issue_command(
            path=self.PATH_SET_ACTION,
            parameters={
                PARAMETER_COMMAND: action,
            },
        )

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
