"""CatLink API Library."""

from .account import CatlinkAccount
from .const import (
    CatlinkAction,
    CatlinkBoxFullLevel,
    CatlinkWorkModel,
    CatlinkWorkStatus,
)
from .device import CatlinkDevice
from .exceptions import CatlinkError, CatlinkLoginError, CatlinkRequestError
from .feeder_device import CatlinkFeederDevice
from .litterbox_device import CatlinkLitterBoxDevice
from .models import (
    CatlinkAccountConfig,
    CatlinkDeviceDetails,
    CatlinkDeviceError,
    CatlinkDeviceInfo,
    CatlinkFeederDeviceDetails,
    CatlinkLitterBoxDeviceDetails,
    CatlinkSharers,
    CatlinkTimingSettings,
)
from .scooper_device import CatlinkScooperDevice

__all__ = [
    "CatlinkAccount",
    "CatlinkAccountConfig",
    "CatlinkDevice",
    "CatlinkError",
    "CatlinkLoginError",
    "CatlinkRequestError",
    "CatlinkDeviceInfo",
    "CatlinkFeederDevice",
    "CatlinkLitterBoxDevice",
    "CatlinkLitterBoxDeviceDetails",
    "CatlinkScooperDevice",
    "CatlinkDeviceDetails",
    "CatlinkFeederDeviceDetails",
    "CatlinkTimingSettings",
    "CatlinkSharers",
    "CatlinkDeviceError",
    "CatlinkWorkStatus",
    "CatlinkWorkModel",
    "CatlinkAction",
    "CatlinkBoxFullLevel",
]
