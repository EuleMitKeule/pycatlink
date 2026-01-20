"""Base entity for CatLink integration."""

from collections.abc import Callable
from dataclasses import dataclass
from typing import cast

from pycatlink.c08 import CatlinkC08Device
from pycatlink.device import CatlinkDevice

from homeassistant.helpers.device_registry import CONNECTION_NETWORK_MAC, DeviceInfo
from homeassistant.helpers.entity import EntityDescription
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN, MANUFACTURER
from .coordinator import CatlinkDataUpdateCoordinator


@dataclass(frozen=True, kw_only=True)
class CatlinkEntityDescription(EntityDescription):
    """Describes a CatLink entity."""

    exists_fn: Callable[[CatlinkDevice], bool] = lambda _: True


@dataclass(frozen=True, kw_only=True)
class CatlinkC08EntityDescription(EntityDescription):
    """Describes a CatLink C08 entity."""

    exists_fn: Callable[[CatlinkDevice], bool] = lambda device: isinstance(
        device, CatlinkC08Device
    )


class CatlinkEntity(CoordinatorEntity[CatlinkDataUpdateCoordinator]):
    """Base entity for CatLink devices."""

    _attr_has_entity_name = True

    def __init__(
        self,
        coordinator: CatlinkDataUpdateCoordinator,
        device_id: str,
    ) -> None:
        """Initialize the entity."""
        super().__init__(coordinator)

        self._device_id = device_id

        device_name = (
            f"{self._device.device_info.device_name} ({self._device.device_info.id})"
            if self._device.device_info.device_name
            else self._device.device_info.id
        )
        device_info_dict = {
            "identifiers": {(DOMAIN, cast(str, self._device.device_info.id))},
            "name": device_name,
            "manufacturer": MANUFACTURER,
            "model": self._device.device_info.device_name,
        }

        if self._device.device_info.mac:
            device_info_dict["connections"] = {
                (CONNECTION_NETWORK_MAC, self._device.device_info.mac)
            }

        if isinstance(self._device, CatlinkC08Device):
            if self._device.device_details.firmware_version:
                device_info_dict["sw_version"] = (
                    self._device.device_details.firmware_version
                )

        self._attr_device_info = DeviceInfo(**device_info_dict)

    @property
    def _device(self) -> CatlinkDevice:
        """Return the device from coordinator data."""
        return self.coordinator.data.devices[self._device_id]
