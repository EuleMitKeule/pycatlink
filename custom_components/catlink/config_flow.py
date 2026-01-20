"""Config flow for CatLink integration."""

from __future__ import annotations

import logging
from typing import Any

from pycatlink.account import CatlinkAccount
from pycatlink.exceptions import CatlinkError, CatlinkLoginError
from pycatlink.models import CatlinkAccountConfig
import voluptuous as vol

from homeassistant import config_entries
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import HomeAssistantError
from homeassistant.helpers import selector

from .const import (
    CONF_BACKEND_URL,
    CONF_PASSWORD,
    CONF_PHONE,
    CONF_PHONE_INTERNATIONAL_CODE,
    DOMAIN,
    CatlinkBackendUrl,
)

_LOGGER = logging.getLogger(__name__)

STEP_USER_DATA_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_PHONE): str,
        vol.Required(CONF_PASSWORD): str,
        vol.Required(CONF_PHONE_INTERNATIONAL_CODE): str,
        vol.Required(
            CONF_BACKEND_URL, default=CatlinkBackendUrl.EUROAMERICA
        ): selector.SelectSelector(
            selector.SelectSelectorConfig(
                options=list(CatlinkBackendUrl),
                mode=selector.SelectSelectorMode.DROPDOWN,
            )
        ),
    }
)


async def validate_input(hass: HomeAssistant, data: dict[str, Any]) -> dict[str, Any]:
    """Validate the user input allows us to connect.

    Data has the keys from STEP_USER_DATA_SCHEMA with values provided by the user.
    """
    config = CatlinkAccountConfig(
        phone=data[CONF_PHONE],
        password=data[CONF_PASSWORD],
        phone_international_code=data[CONF_PHONE_INTERNATIONAL_CODE],
        api_base=data[CONF_BACKEND_URL],
    )

    account = CatlinkAccount(config)

    try:
        await account.get_devices()
    except CatlinkLoginError as err:
        raise InvalidAuth from err
    except CatlinkError as err:
        _LOGGER.exception("Unexpected exception during authentication")
        raise CannotConnect from err

    return {
        "title": f"CatLink ({config.unique_identifier})",
        "unique_id": config.unique_identifier,
    }


class ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for CatLink."""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> config_entries.ConfigFlowResult:
        """Handle the initial step."""
        errors: dict[str, str] = {}

        if user_input is not None:
            try:
                info = await validate_input(self.hass, user_input)
            except CannotConnect:
                errors["base"] = "cannot_connect"
            except InvalidAuth:
                errors["base"] = "invalid_auth"
            except Exception:  # pylint: disable=broad-except
                _LOGGER.exception("Unexpected exception")
                errors["base"] = "unknown"
            else:
                await self.async_set_unique_id(info["unique_id"])
                self._abort_if_unique_id_configured()

                return self.async_create_entry(
                    title=info["title"],
                    data=user_input,
                )

        return self.async_show_form(
            step_id="user",
            data_schema=STEP_USER_DATA_SCHEMA,
            errors=errors,
        )


class CannotConnect(HomeAssistantError):
    """Error to indicate we cannot connect."""


class InvalidAuth(HomeAssistantError):
    """Error to indicate there is invalid auth."""
