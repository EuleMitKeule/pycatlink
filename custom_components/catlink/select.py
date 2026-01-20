"""Select platform for CatLink integration."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from datetime import datetime, time
from typing import Any

from pycatlink.c08 import CatlinkC08Device
from pycatlink.const import (
    CatlinkC08AutoModeSafeTimeOption,
    CatlinkC08CatLitterType,
    CatlinkC08WorkModel,
)
from pycatlink.device import CatlinkDevice

from homeassistant.components.select import SelectEntity, SelectEntityDescription
from homeassistant.const import EntityCategory
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import CatlinkLitterBoxWorkModel
from .entity import CatlinkC08EntityDescription, CatlinkEntity, CatlinkEntityDescription
from .models import CatlinkConfigEntry

C08_WORK_MODEL_MAP = {
    CatlinkC08WorkModel.AUTO: CatlinkLitterBoxWorkModel.AUTO,
    CatlinkC08WorkModel.MANUAL: CatlinkLitterBoxWorkModel.MANUAL,
    CatlinkC08WorkModel.SCHEDULED: CatlinkLitterBoxWorkModel.SCHEDULED,
}

C08_WORK_MODEL_REVERSE_MAP = {v: k for k, v in C08_WORK_MODEL_MAP.items()}

C08_AUTO_MODE_SAFE_TIME_MAP = {
    CatlinkC08AutoModeSafeTimeOption.MINUTES1: "1_minute",
    CatlinkC08AutoModeSafeTimeOption.MINUTES3: "3_minutes",
    CatlinkC08AutoModeSafeTimeOption.MINUTES5: "5_minutes",
    CatlinkC08AutoModeSafeTimeOption.MINUTES7: "7_minutes",
    CatlinkC08AutoModeSafeTimeOption.MINUTES10: "10_minutes",
    CatlinkC08AutoModeSafeTimeOption.MINUTES15: "15_minutes",
    CatlinkC08AutoModeSafeTimeOption.MINUTES30: "30_minutes",
}

C08_AUTO_MODE_SAFE_TIME_REVERSE_MAP = {
    v: k for k, v in C08_AUTO_MODE_SAFE_TIME_MAP.items()
}

C08_CAT_LITTER_TYPE_MAP = {
    CatlinkC08CatLitterType.BENTONITE: "bentonite",
    CatlinkC08CatLitterType.MIXED: "mixed",
}

C08_CAT_LITTER_TYPE_REVERSE_MAP = {v: k for k, v in C08_CAT_LITTER_TYPE_MAP.items()}

TIME_OPTIONS = [f"{h:02d}:{m:02d}" for h in range(24) for m in range(0, 60, 15)]


@dataclass(frozen=True, kw_only=True)
class CatlinkSelectEntityDescription(SelectEntityDescription, CatlinkEntityDescription):
    """Describes a CatLink select entity."""

    current_fn: Callable[[CatlinkDevice], str | None]
    select_fn: Callable[[Any, str], Any]


@dataclass(frozen=True, kw_only=True)
class CatlinkC08SelectEntityDescription(
    CatlinkSelectEntityDescription, CatlinkC08EntityDescription
):
    """Describes a CatLink C08 select entity."""

    current_fn: Callable[[CatlinkC08Device], str | None]


SELECTS: tuple[CatlinkSelectEntityDescription, ...] = (
    CatlinkC08SelectEntityDescription(
        key="work_model",
        translation_key="work_model",
        entity_category=EntityCategory.CONFIG,
        options=list(CatlinkLitterBoxWorkModel),
        current_fn=lambda data: (
            C08_WORK_MODEL_MAP.get(data.device_details.work_model)
            if data.device_details.work_model
            else None
        ),
        select_fn=lambda device, option: device.set_work_model(
            C08_WORK_MODEL_REVERSE_MAP[CatlinkLitterBoxWorkModel(option)]
        ),
    ),
    CatlinkC08SelectEntityDescription(
        key="auto_mode_safe_time",
        translation_key="auto_mode_safe_time",
        entity_category=EntityCategory.CONFIG,
        options=list(C08_AUTO_MODE_SAFE_TIME_MAP.values()),
        current_fn=lambda data: (
            C08_AUTO_MODE_SAFE_TIME_MAP.get(
                CatlinkC08AutoModeSafeTimeOption(int(data.device_details.safe_time))
            )
            if data.device_details.safe_time
            else None
        ),
        select_fn=lambda device, option: device.set_auto_mode_safe_time(
            C08_AUTO_MODE_SAFE_TIME_REVERSE_MAP[option]
        ),
    ),
    CatlinkC08SelectEntityDescription(
        key="cat_litter_type",
        translation_key="cat_litter_type",
        entity_category=EntityCategory.CONFIG,
        options=list(C08_CAT_LITTER_TYPE_MAP.values()),
        current_fn=lambda data: (
            C08_CAT_LITTER_TYPE_MAP.get(
                CatlinkC08CatLitterType(f"{data.device_details.litter_type:02}")
            )
            if data.device_details.litter_type
            else None
        ),
        select_fn=lambda device, option: device.set_cat_litter_type(
            C08_CAT_LITTER_TYPE_REVERSE_MAP[option]
        ),
    ),
    CatlinkC08SelectEntityDescription(
        key="quiet_mode_start_time",
        translation_key="quiet_mode_start_time",
        entity_category=EntityCategory.CONFIG,
        options=TIME_OPTIONS,
        current_fn=lambda data: (
            data.device_details.quiet_times.split("-")[0]
            if data.device_details.quiet_times
            and "-" in data.device_details.quiet_times
            else None
        ),
        select_fn=lambda device, option: device.set_quiet_mode(
            device.device_details.quiet_mode_enable
            if device.device_details.quiet_mode_enable is not None
            else False,
            datetime.time.fromisoformat(option),
            datetime.time.fromisoformat(device.device_details.quiet_times.split("-")[1])
            if device.device_details.quiet_times
            and "-" in device.device_details.quiet_times
            else time(8, 0),
        ),
    ),
    CatlinkC08SelectEntityDescription(
        key="quiet_mode_end_time",
        translation_key="quiet_mode_end_time",
        entity_category=EntityCategory.CONFIG,
        options=TIME_OPTIONS,
        current_fn=lambda data: (
            data.device_details.quiet_times.split("-")[1]
            if data.device_details.quiet_times
            and "-" in data.device_details.quiet_times
            else None
        ),
        select_fn=lambda device, option: device.set_quiet_mode(
            device.device_details.quiet_mode_enable
            if device.device_details.quiet_mode_enable is not None
            else False,
            datetime.time.fromisoformat(device.device_details.quiet_times.split("-")[0])
            if device.device_details.quiet_times
            and "-" in device.device_details.quiet_times
            else time(22, 0),
            datetime.time.fromisoformat(option),
        ),
    ),
)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: CatlinkConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up CatLink selects from a config entry."""
    coordinator = entry.runtime_data.coordinator

    async_add_entities(
        CatlinkSelect(coordinator, device_id, description)
        for device_id in coordinator.data.devices
        for description in SELECTS
        if description.exists_fn(coordinator.data.devices[device_id])
    )


class CatlinkSelect(CatlinkEntity, SelectEntity):
    """Representation of a CatLink select."""

    entity_description: CatlinkSelectEntityDescription

    def __init__(
        self,
        coordinator,
        device_id: str,
        description: CatlinkSelectEntityDescription,
    ) -> None:
        """Initialize the select."""
        super().__init__(coordinator, device_id)
        self.entity_description = description
        self._attr_unique_id = f"{device_id}_{description.key}"
        self._attr_options = description.options or []

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        self._attr_current_option = self.entity_description.current_fn(self._device)
        super()._handle_coordinator_update()

    async def async_select_option(self, option: str) -> None:
        """Change the selected option."""
        await self.entity_description.select_fn(self._device, option)
        self._attr_current_option = option
        self.async_write_ha_state()
        await self.coordinator.async_request_refresh()
