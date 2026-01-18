"""Litter box class for CatLink."""

from .const import (
    API_LITTERBOX_ACTION_COMMAND,
    API_LITTERBOX_BOX_FULL_SETTING,
    API_LITTERBOX_CHANGE_MODE,
    API_LITTERBOX_INFO,
    API_LITTERBOX_LOGS,
    API_LITTERBOX_REPLACE_GARBAGE_BAG,
    DATA_KEY_SCOOPER_LOG_TOP5,
    DISABLE_VALUE,
    ENABLE_VALUE,
    PARAMETER_ENABLE,
    PARAMETER_LEVEL,
    CatlinkAction,
    CatlinkBoxFullLevel,
    CatlinkWorkModel,
)
from .device import CatlinkDevice
from .models import CatlinkLitterBoxDeviceDetails


class CatlinkLitterBoxDevice(CatlinkDevice[CatlinkLitterBoxDeviceDetails]):
    """Litter box class for CatLink."""

    DETAILS_CLASS = CatlinkLitterBoxDeviceDetails
    SUPPORTED_MODELS = [
        CatlinkWorkModel.AUTO,
        CatlinkWorkModel.MANUAL,
        CatlinkWorkModel.TIME,
    ]
    SUPPORTED_ACTIONS = [
        CatlinkAction.CLEANING,
        CatlinkAction.PAUSE,
    ]
    PATH_DETAILS = API_LITTERBOX_INFO
    PATH_LOGS = API_LITTERBOX_LOGS
    PATH_SET_MODE = API_LITTERBOX_CHANGE_MODE
    PATH_SET_ACTION = API_LITTERBOX_ACTION_COMMAND
    RESPONSE_KEY_LOGS = DATA_KEY_SCOOPER_LOG_TOP5

    async def change_bag(self, enable: bool) -> None:
        """Change the garbage bag."""
        await self._issue_command(
            path=API_LITTERBOX_REPLACE_GARBAGE_BAG,
            parameters={
                PARAMETER_ENABLE: ENABLE_VALUE if enable else DISABLE_VALUE,
            },
        )

    async def select_box_full_sensitivity(self, level: CatlinkBoxFullLevel) -> None:
        """Select the box full sensitivity level."""
        await self._issue_command(
            path=API_LITTERBOX_BOX_FULL_SETTING,
            parameters={
                PARAMETER_LEVEL: level,
            },
        )
