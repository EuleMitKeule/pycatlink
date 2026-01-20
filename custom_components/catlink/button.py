"""Button platform for CatLink integration."""

from __future__ import annotations

from collections.abc import Awaitable, Callable
from dataclasses import dataclass

from pycatlink.c08 import CatlinkC08Device
from pycatlink.device import CatlinkDevice

from homeassistant.components.button import ButtonEntity, ButtonEntityDescription
from homeassistant.const import EntityCategory
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .coordinator import CatlinkDataUpdateCoordinator
from .entity import CatlinkC08EntityDescription, CatlinkEntity, CatlinkEntityDescription
from .models import CatlinkConfigEntry


@dataclass(frozen=True, kw_only=True)
class CatlinkButtonEntityDescription(ButtonEntityDescription, CatlinkEntityDescription):
    """Describes a CatLink C08 button entity."""

    press_fn: Callable[[CatlinkDevice], Awaitable[None]]


@dataclass(frozen=True, kw_only=True)
class CatlinkC08ButtonEntityDescription(
    CatlinkButtonEntityDescription, CatlinkC08EntityDescription
):
    """Describes a CatLink C08 button entity."""

    press_fn: Callable[[CatlinkC08Device], Awaitable[None]]


BUTTONS: tuple[CatlinkButtonEntityDescription, ...] = (
    CatlinkC08ButtonEntityDescription(
        key="start_litter_leveling",
        translation_key="start_litter_leveling",
        press_fn=lambda device: device.start_pave(),
    ),
    CatlinkC08ButtonEntityDescription(
        key="pause_litter_leveling",
        translation_key="pause_litter_leveling",
        press_fn=lambda device: device.pause_pave(),
    ),
    CatlinkC08ButtonEntityDescription(
        key="start_cleaning",
        translation_key="start_cleaning",
        press_fn=lambda device: device.start_clean(),
    ),
    CatlinkC08ButtonEntityDescription(
        key="pause_cleaning",
        translation_key="pause_cleaning",
        press_fn=lambda device: device.pause_clean(),
    ),
    CatlinkC08ButtonEntityDescription(
        key="cancel_cleaning",
        translation_key="cancel_cleaning",
        press_fn=lambda device: device.cancel_clean(),
    ),
    CatlinkC08ButtonEntityDescription(
        key="refresh",
        translation_key="refresh",
        entity_category=EntityCategory.DIAGNOSTIC,
        press_fn=lambda device: device.refresh(),
    ),
)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: CatlinkConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up CatLink buttons from a config entry."""
    coordinator = entry.runtime_data.coordinator

    async_add_entities(
        CatlinkButton(coordinator, device_id, description)
        for device_id in coordinator.data.devices
        for description in BUTTONS
        if description.exists_fn(coordinator.data.devices[device_id])
    )


class CatlinkButton(CatlinkEntity, ButtonEntity):
    """Representation of a CatLink button."""

    entity_description: CatlinkButtonEntityDescription

    def __init__(
        self,
        coordinator: CatlinkDataUpdateCoordinator,
        device_id: str,
        description: CatlinkButtonEntityDescription,
    ) -> None:
        """Initialize the button."""
        super().__init__(coordinator, device_id)
        self.entity_description = description
        self._attr_unique_id = f"{device_id}_{description.key}"

    async def async_press(self) -> None:
        """Press the button."""
        await self.entity_description.press_fn(self._device)
        await self.coordinator.async_request_refresh()
