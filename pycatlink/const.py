"""Constants for the CatLink API."""

from enum import Enum, StrEnum


class HttpMethod(str, Enum):
    """HTTP methods."""

    GET = "GET"
    POST = "POST"


ENV_CATLINK_PHONE = "CATLINK_PHONE"
ENV_CATLINK_PASSWORD = "CATLINK_PASSWORD"
ENV_CATLINK_PHONE_INTERNATIONAL_CODE = "CATLINK_PHONE_INTERNATIONAL_CODE"

DEFAULT_API_BASE = "https://app.catlinks.cn/api/"

SIGN_KEY = "00109190907746a7ad0e2139b6d09ce47551770157fe4ac5922f3a5454c82712"
RSA_PUBLIC_KEY = (
    "MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQCCA9I+iEl2AI8dnhdwwxPxHVK8iNAt6aTq6UhNsLsguWS5qtbLnuGz2RQdfNS"
    "aKSU2B6D/vE2gb1fM6f1A5cKndqF/riWGWn1EfL3FFQZduOTxoA0RTQzhrTa5LHcJ/an/NuHUwShwIOij0Mf4g8faTe4FT7/HdA"
    "oK7uW0cG9mZwIDAQAB"
)
RSA_PRIVATE_KEY = (
    "MIICdgIBADANBgkqhkiG9w0BAQEFAASCAmAwggJcAgEAAoGBAIID0j6ISXYAjx2eF3DDE/EdUryI0C3ppOrpSE2wuyC5ZLmq1s"
    "ue4bPZFB181JopJTYHoP+8TaBvV8zp/UDlwqd2oX+uJYZafUR8vcUVBl245PGgDRFNDOGtNrksdwn9qf824dTBKHAg6KPQx/iD"
    "x9pN7gVPv8d0Cgru5bRwb2ZnAgMBAAECgYAccTuQRH5Vmz+zyf70wyhcqf6Mkh2Avck/PrN7k3sMaKJZX79HokVb89RLsyBLbU"
    "7fqAGXkJkmzNTXViT6Colvi1T7QQWhkvPsPEsu/89s5yo0ME2+rtvBA/niy1iQs6UYTzZivSKosLVgCTmcOYbp5eUCP8IPtKy/"
    "3vzkIBMZqQJBALn0bAgCeXwctYqznCboNHAX7kGk9HjX8VCOfaBh1WcAYWk7yKzYZemMKXMw5ifeopT0uUpLEk5mlN4nxwBsTp"
    "sCQQCy/SHTlQyt/yauVyrJipZflUK/hq6hIZFIu1Mc40L6BDNAboi42P9suznXbV7DD+LNpxFnkYlee8sitY0R474lAkEAsjBV"
    "lRdJ8nRQQij6aQ35sbA8zwqSeXnz842XNCiLpbfnoD95fKeggLuevJMO+QWOJc6b/2UQlbAW1wqm1vDyIQJAUhYVNVvd/M5Phx"
    "Ui4ltUq3Fgs0WpQOyMHLcMXus7BD544svOmDesrMkQtePK2dqnQXmlWcI9Jb/QYZKxp8qyoQJAP2kK4dc3AA4BDVQUMHYiSnGp"
    "I0eGQrD/W4rBeoCX8sJDCH49lMsec52TFI2Gn8tTKOCqqgGvRSKDJ005HlnmKw=="
)

DEFAULT_PHONE_INTERNATIONAL_CODE = "86"
DEFAULT_LANGUAGE = "en_US"
DEFAULT_REQUEST_TIMEOUT = 5

API_LOGIN_PASSWORD = "login/password"
API_DEVICE_LIST = "token/device/union/list/sorted"
API_DEVICE_CHANGE_MODE = "token/device/changeMode"
API_DEVICE_ACTION_COMMAND = "token/device/actionCmd"
API_DEVICE_INFO = "token/device/info"
API_DEVICE_LOGS = "token/device/stats/log/top5"
API_SCOOPER_INFO = "token/litterbox/info"
API_FEEDER_DETAIL = "token/device/feeder/detail"
API_FEEDER_LOGS = "token/device/feeder/stats/log/top5"
API_FEEDER_FOOD_OUT = "token/device/feeder/foodOut"
API_LITTERBOX_INFO = "token/litterbox/info"
API_LITTERBOX_LOGS = "token/litterbox/stats/log/top5"
API_LITTERBOX_CHANGE_MODE = "token/litterbox/changeMode"
API_LITTERBOX_ACTION_COMMAND = "token/litterbox/actionCmd"
API_LITTERBOX_BOX_FULL_SETTING = "token/litterbox/boxFullSetting"
API_LITTERBOX_REPLACE_GARBAGE_BAG = "token/litterbox/replaceGarbageBagCmd"
API_SCOOPER_LOGS = "token/device/scooper/stats/log/top5"
API_SCOOPER_LOGS_LITTERBOX = "token/litterbox/stats/log/top5"

ERROR_CODE_TOKEN_EXPIRED = 1002
ERROR_CODE_SUCCESS = 0

PLATFORM_ANDROID = "ANDROID"

USER_AGENT = "okhttp/3.10.0"

HEADER_LANGUAGE = "language"
HEADER_USER_AGENT = "User-Agent"
HEADER_TOKEN = "token"

PARAMETER_NONCESTR = "noncestr"
PARAMETER_TOKEN = "token"
PARAMETER_SIGN = "sign"
PARAMETER_PLATFORM = "platform"
PARAMETER_INTERNATIONAL_CODE = "internationalCode"
PARAMETER_MOBILE = "mobile"
PARAMETER_PASSWORD = "password"
PARAMETER_TYPE = "type"
PARAMETER_DEVICE_ID = "deviceId"
PARAMETER_WORK_MODEL = "workModel"
PARAMETER_COMMAND = "cmd"
PARAMETER_LEVEL = "level"
PARAMETER_ENABLE = "enable"
PARAMETER_FOOD_OUT_NUMBER = "footOutNum"

RESPONSE_RETURN_CODE = "returnCode"
RESPONSE_DATA = "data"

DATA_KEY_TOKEN = "token"
DATA_KEY_DEVICES = "devices"
DATA_KEY_DEVICE_INFO = "deviceInfo"
DATA_KEY_DEVICE_LOG_TOP5 = "deviceLogTop5"
DATA_KEY_FEEDER_LOG_TOP5 = "feederLogTop5"
DATA_KEY_SCOOPER_LOG_TOP5 = "scooperLogTop5"

DEVICE_DETAIL_WORK_STATUS = "workStatus"
DEVICE_DETAIL_WORK_MODE = "workModel"
DEVICE_DETAIL_CURRENT_MESSAGE = "currentMessage"
DEVICE_DETAIL_CURRENT_ERROR = "currentError"
DEVICE_DETAIL_WEIGHT = "weight"
DEVICE_DETAIL_ERROR = "error"
DEVICE_DETAIL_FOOD_OUT_STATUS = "foodOutStatus"

DEVICE_DATA_ID = "id"
DEVICE_DATA_MAC = "mac"
DEVICE_DATA_MODEL = "model"
DEVICE_DATA_DEVICE_TYPE = "deviceType"
DEVICE_DATA_DEVICE_NAME = "deviceName"
DEVICE_DATA_CURRENT_ERROR_MESSAGE = "currentErrorMessage"


class CatlinkWorkStatus(StrEnum):
    """Work status enumeration."""

    IDLE = "00"
    RUNNING = "01"
    NEED_RESET = "02"


class CatlinkWorkModel(StrEnum):
    """Work model enumeration."""

    AUTO = "00"
    MANUAL = "01"
    TIME = "02"
    EMPTY = "03"


class CatlinkAction(StrEnum):
    """Action enumeration."""

    PAUSE = "00"
    START = "01"
    CLEANING = "01"


class CatlinkBoxFullLevel(StrEnum):
    """Box full level enumeration."""

    LEVEL_1 = "LEVEL_01"
    LEVEL_2 = "LEVEL_02"
    LEVEL_3 = "LEVEL_03"
    LEVEL_4 = "LEVEL_04"


DEFAULT_FOOD_OUT_NUMBER = 5
ENABLE_VALUE = "1"
DISABLE_VALUE = "0"

TYPE_NONE = "NONE"

PASSWORD_MAX_LENGTH = 16
