"""Feeder device class for CatLink integration."""

from .const import (
    API_FEEDER_DETAIL,
    API_FEEDER_FOOD_OUT,
    API_FEEDER_LOGS,
    DATA_KEY_FEEDER_LOG_TOP5,
    DEFAULT_FOOD_OUT_NUMBER,
    PARAMETER_FOOD_OUT_NUMBER,
)
from .device import CatlinkDevice
from .models import CatlinkFeederDeviceDetails


class CatlinkFeederDevice(CatlinkDevice[CatlinkFeederDeviceDetails]):
    """Feeder device class for CatLink integration."""

    DETAILS_CLASS = CatlinkFeederDeviceDetails
    PATH_DETAILS = API_FEEDER_DETAIL
    PATH_LOGS = API_FEEDER_LOGS
    RESPONSE_KEY_LOGS = DATA_KEY_FEEDER_LOG_TOP5

    async def food_out(self) -> None:
        """Food out of the device."""
        await self._issue_command(
            path=API_FEEDER_FOOD_OUT,
            parameters={
                PARAMETER_FOOD_OUT_NUMBER: DEFAULT_FOOD_OUT_NUMBER,
            },
        )
