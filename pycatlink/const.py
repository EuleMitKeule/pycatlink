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

DEFAULT_LANGUAGE = "en_US"
DEFAULT_REQUEST_TIMEOUT = 5

API_LOGIN_PASSWORD = "login/password"
API_DEVICE_LIST = "token/device/union/list/sorted"
API_PET_LIST = "token/pet/list"
API_DEVICE_CHANGE_MODE = "token/device/changeMode"
API_DEVICE_ACTION_COMMAND = "token/device/actionCmd"
API_DEVICE_INFO = "token/device/info"
API_DEVICE_LOGS = "token/device/stats/log/top5"
API_SCOOPER_INFO = "token/litterbox/info"
API_FEEDER_DETAIL = "token/device/feeder/detail"
API_FEEDER_LOGS = "token/device/feeder/stats/log/top5"
API_FEEDER_FOOD_OUT = "token/device/feeder/foodOut"
API_LITTERBOX_INFO = "token/litterbox/info"
API_LITTERBOX_C08_INFO = "token/litterbox/info/c08"
API_LITTERBOX_LOGS = "token/litterbox/stats/log/top5"
API_LITTERBOX_CHANGE_MODE = "token/litterbox/changeMode"
API_LITTERBOX_ACTION_COMMAND = "token/litterbox/actionCmd"
API_LITTERBOX_ACTION_COMMAND_V3 = "token/litterbox/actionCmd/v3"
API_LITTERBOX_BOX_FULL_SETTING = "token/litterbox/boxFullSetting"
API_LITTERBOX_REPLACE_GARBAGE_BAG = "token/litterbox/replaceGarbageBagCmd"
API_SCOOPER_LOGS = "token/device/scooper/stats/log/top5"
API_SCOOPER_LOGS_LITTERBOX = "token/litterbox/stats/log/top5"
API_LITTERBOX_PET_WEIGHT_AUTO_UPDATE = "token/litterbox/pet/weight/autoUpdate"
API_LITTERBOX_CAT_LITTER_SETTING = "token/litterbox/catLitterSetting"
API_LITTERBOX_KITTY_MODEL_SWITCH = "token/litterbox/kittyModelSwitch"
API_LITTERBOX_SAFE_TIME_SETTING = "token/litterbox/safeTimeSetting"
API_LITTERBOX_DEEP_CLEAN_AUTO_BURIAL = "token/litterbox/deepClean/autoBurial"
API_LITTERBOX_DEEP_CLEAN_CONTINUOUS_CLEANING = (
    "token/litterbox/deepClean/continuousCleaning"
)
API_LITTERBOX_KEY_LOCK = "token/litterbox/keyLock"
API_LITTERBOX_INDICATOR_LIGHT_SETTING = "token/litterbox/indicatorLightSetting"
API_LITTERBOX_KEYPAD_TONE = "token/litterbox/keypadTone"
API_LITTERBOX_STATS_DATA_COMPARE_V2 = "token/litterbox/stats/data/compare/v2"
API_LITTERBOX_NOTICE_CONFIG_SET = "token/litterbox/noticeConfig/set"
API_LITTERBOX_STATS_CATS = "token/litterbox/stats/cats"
API_LITTERBOX_STATS_LOG_TOP5 = "token/litterbox/stats/log/top5"
API_LITTERBOX_LINKED_PETS = "token/litterbox/linkedPets"
API_LITTERBOX_CAT_LIST_SELECTABLE = "token/litterbox/cat/listSelectable"
API_LITTERBOX_C08_WIFI_INFO = "token/litterbox/wifi/info"
API_LITTERBOX_NOTICE_CONFIG_LIST_C08 = "token/litterbox/noticeConfig/list/c08"
API_LITTERBOX_ABOUT_DEVICE = "token/litterbox/aboutDevice"

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
PARAMETER_ACTION = "action"
PARAMETER_BEHAVIOR = "behavior"
PARAMETER_LITTER_TYPE = "litterType"
PARAMETER_LOCK_STATUS = "lockStatus"
PARAMETER_STATUS = "status"
PARAMETER_PANEL_TONE = "panelTone"
PARAMETER_KIND = "kind"
PARAMETER_TIMES = "times"
PARAMETER_SAFE_TIME = "safeTime"
PARAMETER_NOTICE_ITEM = "noticeItem"
PARAMETER_NOTICE_SWITCH = "noticeSwitch"

RESPONSE_RETURN_CODE = "returnCode"
RESPONSE_KEY_DATA = "data"
RESPONSE_KEY_CATS = "cats"
RESPONSE_KEY_WIFI_INFO = "wifiInfo"
RESPONSE_KEY_NOTICE_CONFIGS = "noticeConfigs"
RESPONSE_KEY_INFO = "info"

DATA_KEY_TOKEN = "token"
RESPONSE_KEY_DEVICES = "devices"
RESPONSE_KEY_DEVICE_INFO = "deviceInfo"
RESPONSE_KEY_COMPARE_DATA = "compareData"
RESPONSE_KEY_DEVICE_LOG_TOP5 = "deviceLogTop5"
RESPONSE_KEY_FEEDER_LOG_TOP5 = "feederLogTop5"
RESPONSE_KEY_SCOOPER_LOG_TOP5 = "scooperLogTop5"
RESPONSE_KEY_LOG_TOP5 = "scooperLogTop5"
RESPONSE_KEY_PETS = "pets"
RESPONSE_KEY_RECORDS = "records"

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

TYPE_NONE = "NONE"
DEFAULT_FOOD_OUT_NUMBER = 5
PASSWORD_MAX_LENGTH = 16


class CatlinkC08WorkStatus(StrEnum):
    """Work status enumeration."""

    IDLE = "00"
    RUNNING = "01"
    NEED_RESET = "02"


class CatlinkC08WorkModel(StrEnum):
    """C08 Work model enumeration."""

    AUTO = "00"
    MANUAL = "01"
    SCHEDULED = "02"


class CatlinkC08Action(StrEnum):
    """C08 Action enumeration."""

    RUN = "RUN"
    PAUSE = "PAUSE"
    CANCEL = "CANCEL"


class CatlinkC08Behavior(StrEnum):
    """C08 Behavior enumeration."""

    CLEAN = "CLEAN"
    PAVE = "PAVE"


class CatlinkC08CatLitterType(StrEnum):
    """C08 Cat litter type enumeration."""

    BENTONITE = "00"
    MIXED = "02"


class CatlinkC08KeyLockStatus(StrEnum):
    """C08 Key lock setting enumeration."""

    UNLOCKED = "00"
    LOCKED = "01"


class CatlinkC08IndicatorLightStatus(StrEnum):
    """C08 Indicator light setting enumeration."""

    CLOSED = "CLOSED"
    ALWAYS_OPEN = "ALWAYS_OPEN"


class CatlinkC08KeypadPanelTone(StrEnum):
    """C08 Keypad panel tone setting enumeration."""

    DISABLED = "00"
    ENABLED = "01"


class CatlinkC08KeypadKind(StrEnum):
    """C08 Keypad kind enumeration."""

    DEFAULT = "00"


class CatlinkC08AutoModeSafeTimeOption(Enum):
    """C08 Auto mode safe time option enumeration."""

    MINUTES1 = 1
    MINUTES3 = 3
    MINUTES5 = 5
    MINUTES7 = 7
    MINUTES10 = 10
    MINUTES15 = 15
    MINUTES30 = 30


class CatlinkC08NoticeItem(StrEnum):
    """C08 Notice item enumeration."""

    CAT_CAME = "LITTERBOX_599_CAT_CAME"
    BOX_FULL = "LITTERBOX_599_BOX_FULL"
    REPLACE_GARBAGE_BAG = "REPLACE_GARBAGE_BAG"
    WASH_SCOOPER = "WASH_SCOOPER"
    REPLACE_DEODORANT = "REPLACE_DEODORANT"
    LITTER_NOT_ENOUGH = "LITTERBOX_599_CAT_LITTER_NOT_ENOUGH"
    SANDBOX_NOT_ENOUGH = "LITTERBOX_599_SANDBOX_NOT_ENOUGHT"
    ANTI_PINCH = "LITTERBOX_599_ANTI_PINCH"
    FIRMWARE_UPDATED = "LITTERBOX_599_FIRMWARE_UPDATED"
