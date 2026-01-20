"""CatLink integration."""

import logging

from pycatlink.account import CatlinkAccount
from pycatlink.models import CatlinkAccountConfig

from homeassistant.const import Platform
from homeassistant.core import HomeAssistant

from .const import (
    CONF_BACKEND_URL,
    CONF_PASSWORD,
    CONF_PHONE,
    CONF_PHONE_INTERNATIONAL_CODE,
)
from .coordinator import CatlinkDataUpdateCoordinator
from .models import CatlinkConfigEntry, CatlinkData

_LOGGER = logging.getLogger(__name__)

PLATFORMS: list[Platform] = [
    Platform.BINARY_SENSOR,
    Platform.BUTTON,
    Platform.SELECT,
    Platform.SENSOR,
    Platform.SWITCH,
]


async def async_setup_entry(hass: HomeAssistant, entry: CatlinkConfigEntry) -> bool:
    """Set up CatLink from a config entry."""
    phone = entry.data[CONF_PHONE]
    password = entry.data[CONF_PASSWORD]
    international_code = entry.data[CONF_PHONE_INTERNATIONAL_CODE]
    backend_url = entry.data[CONF_BACKEND_URL]

    config = CatlinkAccountConfig(
        phone=phone,
        password=password,
        phone_international_code=international_code,
        api_base=backend_url,
    )
    account = CatlinkAccount(config)

    coordinator = CatlinkDataUpdateCoordinator(hass, account, entry)

    await coordinator.async_config_entry_first_refresh()

    entry.runtime_data = CatlinkData(account=account, coordinator=coordinator)

    _LOGGER.info("Discovered %d CatLink device(s)", len(coordinator.data.devices))

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    coordinator.async_update_listeners()

    return True


async def async_unload_entry(hass: HomeAssistant, entry: CatlinkConfigEntry) -> bool:
    """Unload a config entry."""
    return await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
