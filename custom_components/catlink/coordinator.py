"""Data update coordinator for CatLink."""

from datetime import timedelta
import logging

from pycatlink.account import CatlinkAccount
from pycatlink.c08 import CatlinkC08Device
from pycatlink.device import CatlinkDevice
from pycatlink.exceptions import CatlinkError
from pycatlink.models import CatlinkPet

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import DOMAIN, UPDATE_INTERVAL
from .models import CatlinkCoordinatorData

_LOGGER = logging.getLogger(__name__)


class CatlinkDataUpdateCoordinator(DataUpdateCoordinator[CatlinkCoordinatorData]):
    """Class to manage fetching CatLink device data."""

    def __init__(
        self, hass: HomeAssistant, account: CatlinkAccount, config_entry: ConfigEntry
    ) -> None:
        """Initialize the coordinator."""
        super().__init__(
            hass,
            logger=_LOGGER,
            name=DOMAIN,
            update_interval=timedelta(seconds=UPDATE_INTERVAL),
            config_entry=config_entry,
        )
        self.account = account
        self.devices: list[CatlinkDevice] = []
        self.pets: list = []

    async def async_config_entry_first_refresh(self) -> None:
        """Fetch initial data."""
        self.devices = await self.account.get_devices()
        self.pets = await self.account.get_pets()
        await super().async_config_entry_first_refresh()

    async def _async_update_data(self) -> CatlinkCoordinatorData:
        """Fetch data from CatLink API."""
        data: dict[str, CatlinkDevice] = {}

        try:
            for device in self.devices:
                if not isinstance(device, CatlinkC08Device):
                    continue

                if not device.device_info.id:
                    _LOGGER.warning(
                        "Skipping device with missing ID: %s",
                        device.device_info,
                    )
                    continue

                await device.refresh()

                data[device.device_info.id] = device

            pets_data: dict[str, CatlinkPet] = {}
            for pet in self.pets:
                if pet.id:
                    pets_data[pet.id] = pet

            return CatlinkCoordinatorData(
                account_config=self.account.config,
                devices=data,
                pets=pets_data,
            )
        except CatlinkError as err:
            raise UpdateFailed(f"Error communicating with CatLink API: {err}") from err
