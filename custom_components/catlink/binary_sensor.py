"""Binary sensor platform for CatLink integration."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass

from pycatlink.c08 import CatlinkC08Device
from pycatlink.device import CatlinkDevice

from homeassistant.components.binary_sensor import (
    BinarySensorDeviceClass,
    BinarySensorEntity,
    BinarySensorEntityDescription,
)
from homeassistant.const import EntityCategory
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .coordinator import CatlinkDataUpdateCoordinator
from .entity import CatlinkC08EntityDescription, CatlinkEntity, CatlinkEntityDescription
from .models import CatlinkConfigEntry


@dataclass(frozen=True, kw_only=True)
class CatlinkBinarySensorEntityDescription(
    BinarySensorEntityDescription, CatlinkEntityDescription
):
    """Describes a CatLink binary sensor entity."""

    is_on_fn: Callable[[CatlinkDevice], bool | None]


@dataclass(frozen=True, kw_only=True)
class CatlinkC08BinarySensorEntityDescription(
    CatlinkBinarySensorEntityDescription, CatlinkC08EntityDescription
):
    """Describes a CatLink C08 binary sensor entity."""

    is_on_fn: Callable[[CatlinkC08Device], bool | None]  # type: ignore[assignment]


BINARY_SENSORS: tuple[CatlinkBinarySensorEntityDescription, ...] = (
    CatlinkC08BinarySensorEntityDescription(
        key="online",
        translation_key="online",
        device_class=BinarySensorDeviceClass.CONNECTIVITY,
        entity_category=EntityCategory.DIAGNOSTIC,
        is_on_fn=lambda device: device.device_details.online,
    ),
)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: CatlinkConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up CatLink binary sensors from a config entry."""
    coordinator = entry.runtime_data.coordinator

    async_add_entities(
        CatlinkBinarySensor(coordinator, device_id, description)
        for device_id in coordinator.data.devices
        for description in BINARY_SENSORS
        if description.exists_fn(coordinator.data.devices[device_id])
    )


class CatlinkBinarySensor(CatlinkEntity, BinarySensorEntity):
    """Representation of a CatLink binary sensor."""

    entity_description: CatlinkBinarySensorEntityDescription

    def __init__(
        self,
        coordinator: CatlinkDataUpdateCoordinator,
        device_id: str,
        description: CatlinkBinarySensorEntityDescription,
    ) -> None:
        """Initialize the binary sensor."""
        super().__init__(coordinator, device_id)
        self.entity_description = description
        self._attr_unique_id = f"{device_id}_{description.key}"

    @property
    def is_on(self) -> bool | None:
        """Return true if the binary sensor is on."""
        return self.entity_description.is_on_fn(self._device)
