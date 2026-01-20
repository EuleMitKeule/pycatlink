"""Sensor platform for CatLink integration."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from datetime import UTC, datetime

from pycatlink.c08 import CatlinkC08Device
from pycatlink.const import CatlinkC08WorkStatus
from pycatlink.device import CatlinkDevice

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorEntityDescription,
    SensorStateClass,
)
from homeassistant.const import EntityCategory, UnitOfMass, UnitOfTime
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .coordinator import CatlinkDataUpdateCoordinator
from .entity import CatlinkC08EntityDescription, CatlinkEntity, CatlinkEntityDescription
from .models import CatlinkConfigEntry

WORK_STATUS_MAP = {
    CatlinkC08WorkStatus.IDLE: "idle",
    CatlinkC08WorkStatus.RUNNING: "running",
    CatlinkC08WorkStatus.NEED_RESET: "need_reset",
}


@dataclass(frozen=True, kw_only=True)
class CatlinkSensorEntityDescription(SensorEntityDescription, CatlinkEntityDescription):
    """Describes a CatLink sensor entity."""

    value_fn: Callable[[CatlinkDevice], str | int | float | datetime | None]


@dataclass(frozen=True, kw_only=True)
class CatlinkC08SensorEntityDescription(
    CatlinkSensorEntityDescription, CatlinkC08EntityDescription
):
    """Describes a CatLink C08 sensor entity."""

    value_fn: Callable[[CatlinkC08Device], str | int | float | datetime | None]


SENSORS: tuple[CatlinkSensorEntityDescription, ...] = (
    CatlinkC08SensorEntityDescription(
        key="current_message",
        translation_key="current_message",
        value_fn=lambda data: data.device_details.current_message,
    ),
    CatlinkC08SensorEntityDescription(
        key="work_status",
        translation_key="work_status",
        device_class=SensorDeviceClass.ENUM,
        options=["idle", "running", "need_reset"],
        value_fn=lambda data: (
            WORK_STATUS_MAP.get(data.device_details.work_status)
            if data.device_details.work_status
            else None
        ),
    ),
    CatlinkC08SensorEntityDescription(
        key="cat_litter_weight",
        translation_key="cat_litter_weight",
        device_class=SensorDeviceClass.WEIGHT,
        native_unit_of_measurement=UnitOfMass.KILOGRAMS,
        state_class=SensorStateClass.MEASUREMENT,
        value_fn=lambda data: data.device_details.cat_litter_weight,
    ),
    CatlinkC08SensorEntityDescription(
        key="last_heartbeat",
        translation_key="last_heartbeat",
        device_class=SensorDeviceClass.TIMESTAMP,
        entity_category=EntityCategory.DIAGNOSTIC,
        value_fn=lambda data: (
            datetime.fromtimestamp(
                int(data.device_details.last_heart_beat_timestamp) / 1000,
                tz=UTC,
            )
            if data.device_details.last_heart_beat_timestamp
            else None
        ),
    ),
    CatlinkC08SensorEntityDescription(
        key="litter_countdown",
        translation_key="litter_countdown",
        device_class=SensorDeviceClass.DURATION,
        native_unit_of_measurement=UnitOfTime.DAYS,
        state_class=SensorStateClass.MEASUREMENT,
        value_fn=lambda data: (
            data.device_details.litter_countdown
            if data.device_details.litter_countdown is not None
            else None
        ),
    ),
    CatlinkC08SensorEntityDescription(
        key="induction_times",
        translation_key="induction_times",
        state_class=SensorStateClass.TOTAL_INCREASING,
        value_fn=lambda data: data.device_details.induction_times,
    ),
    CatlinkC08SensorEntityDescription(
        key="manual_times",
        translation_key="manual_times",
        state_class=SensorStateClass.TOTAL_INCREASING,
        value_fn=lambda data: data.device_details.manual_times,
    ),
    CatlinkC08SensorEntityDescription(
        key="deodorant_countdown",
        translation_key="deodorant_countdown",
        device_class=SensorDeviceClass.DURATION,
        native_unit_of_measurement=UnitOfTime.DAYS,
        state_class=SensorStateClass.MEASUREMENT,
        value_fn=lambda data: data.device_details.deodorant_countdown,
    ),
    CatlinkC08SensorEntityDescription(
        key="timezone_id",
        translation_key="timezone_id",
        entity_category=EntityCategory.DIAGNOSTIC,
        value_fn=lambda data: data.device_details.timezone_id,
    ),
    CatlinkC08SensorEntityDescription(
        key="cat_litter_pave_second",
        translation_key="cat_litter_pave_second",
        device_class=SensorDeviceClass.DURATION,
        native_unit_of_measurement=UnitOfTime.SECONDS,
        state_class=SensorStateClass.MEASUREMENT,
        entity_category=EntityCategory.DIAGNOSTIC,
        value_fn=lambda data: data.device_details.cat_litter_pave_second,
    ),
    CatlinkC08SensorEntityDescription(
        key="timer_times",
        translation_key="timer_times",
        state_class=SensorStateClass.TOTAL,
        value_fn=lambda data: (
            int(data.device_details.timer_times)
            if data.device_details.timer_times is not None
            else None
        ),
    ),
    CatlinkC08SensorEntityDescription(
        key="clear_times",
        translation_key="clear_times",
        state_class=SensorStateClass.TOTAL,
        value_fn=lambda data: (
            int(data.device_details.clear_times)
            if data.device_details.clear_times is not None
            else None
        ),
    ),
    CatlinkC08SensorEntityDescription(
        key="full_times",
        translation_key="full_times",
        state_class=SensorStateClass.TOTAL,
        value_fn=lambda data: data.device_details.full_times,
    ),
    CatlinkC08SensorEntityDescription(
        key="full_close_times",
        translation_key="full_close_times",
        state_class=SensorStateClass.TOTAL,
        entity_category=EntityCategory.DIAGNOSTIC,
        value_fn=lambda data: data.device_details.full_close_times,
    ),
    CatlinkC08SensorEntityDescription(
        key="box_full_sensitivity",
        translation_key="box_full_sensitivity",
        entity_category=EntityCategory.DIAGNOSTIC,
        value_fn=lambda data: data.device_details.box_full_sensitivity,
    ),
)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: CatlinkConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up CatLink sensors from a config entry."""
    coordinator = entry.runtime_data.coordinator

    async_add_entities(
        CatlinkSensor(coordinator, device_id, description)
        for device_id in coordinator.data.devices
        for description in SENSORS
        if description.exists_fn(coordinator.data.devices[device_id])
    )


class CatlinkSensor(CatlinkEntity, SensorEntity):
    """Representation of a CatLink sensor."""

    entity_description: CatlinkSensorEntityDescription

    def __init__(
        self,
        coordinator: CatlinkDataUpdateCoordinator,
        device_id: str,
        description: CatlinkSensorEntityDescription,
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator, device_id)
        self.entity_description = description
        self._attr_unique_id = f"{device_id}_{description.key}"

    @property
    def native_value(self) -> str | int | float | datetime | None:
        """Return the state of the sensor."""
        return self.entity_description.value_fn(self._device)
