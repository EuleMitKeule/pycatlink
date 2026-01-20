"""Constants for the CatLink integration."""

from enum import StrEnum

DOMAIN = "catlink"

CONF_PHONE = "phone"
CONF_PHONE_INTERNATIONAL_CODE = "phone_international_code"
CONF_PASSWORD = "password"
CONF_BACKEND_URL = "backend_url"

MANUFACTURER = "CatLink"

UPDATE_INTERVAL = 60


class CatlinkBackendUrl(StrEnum):
    """CatLink backend URLs."""

    EUROAMERICA = "https://app-usa.catlinks.cn/api/"
    CHINA = "https://app-sh.catlinks.cn/api/"
    SINGAPORE = "https://app-sgp.catlinks.cn/api/"
    GLOBAL = "https://app.catlinks.cn/api/"


class CatlinkLitterBoxWorkModel(StrEnum):
    """Work mode enum for CatLink litter box devices."""

    AUTO = "automatic"
    MANUAL = "manual"
    SCHEDULED = "scheduled"


class CatlinkScooperWorkMode(StrEnum):
    """Work mode enum for CatLink scooper devices."""

    AUTO = "automatic"
    MANUAL = "manual"
    SCHEDULED = "scheduled"
    EMPTY = "empty"
