"""CatLink API Library."""

from .account import CatlinkAccount
from .device import CatlinkDevice
from .exceptions import CatlinkError
from .feeder_device import CatlinkFeederDevice
from .litterbox_device import CatlinkLitterBoxDevice
from .models import (
    CatlinkAccountConfig,
    CatlinkDeviceDetails,
    CatlinkDeviceInfo,
    CatlinkFeederDeviceDetails,
)
from .scooper_device import CatlinkScooperDevice

__all__ = [
    "CatlinkAccount",
    "CatlinkAccountConfig",
    "CatlinkDevice",
    "CatlinkError",
    "CatlinkDeviceInfo",
    "CatlinkFeederDevice",
    "CatlinkLitterBoxDevice",
    "CatlinkScooperDevice",
    "CatlinkDeviceDetails",
    "CatlinkFeederDeviceDetails",
]
