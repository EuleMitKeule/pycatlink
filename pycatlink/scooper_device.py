"""Scooper device module for CatLink integration."""

from .const import (
    API_SCOOPER_INFO,
    API_SCOOPER_LOGS,
    DATA_KEY_SCOOPER_LOG_TOP5,
    CatlinkAction,
    CatlinkWorkModel,
)
from .device import CatlinkDevice
from .models import CatlinkDeviceDetails


class CatlinkScooperDevice(CatlinkDevice[CatlinkDeviceDetails]):
    """Scooper device class for CatLink."""

    DETAILS_CLASS = CatlinkDeviceDetails
    SUPPORTED_MODELS = [
        CatlinkWorkModel.AUTO,
        CatlinkWorkModel.MANUAL,
        CatlinkWorkModel.TIME,
        CatlinkWorkModel.EMPTY,
    ]
    SUPPORTED_ACTIONS = [
        CatlinkAction.PAUSE,
        CatlinkAction.START,
    ]
    PATH_DETAILS = API_SCOOPER_INFO
    PATH_LOGS = API_SCOOPER_LOGS
    RESPONSE_KEY_LOGS = DATA_KEY_SCOOPER_LOG_TOP5
