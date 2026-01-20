"""Sensor platform for CatLink integration."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from datetime import UTC, datetime

from pycatlink.c08 import CatlinkC08Device
from pycatlink.const import CatlinkC08WorkStatus
from pycatlink.device import CatlinkDevice
from pycatlink.models import CatlinkPet

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorEntityDescription,
    SensorStateClass,
)
from homeassistant.const import EntityCategory, UnitOfMass, UnitOfTime
from homeassistant.core import HomeAssistant
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN, MANUFACTURER
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


@dataclass(frozen=True, kw_only=True)
class CatlinkPetSensorEntityDescription(SensorEntityDescription):
    """Describes a CatLink pet sensor entity."""

    value_fn: Callable[[CatlinkPet], str | int | float | datetime | None]


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
    CatlinkC08SensorEntityDescription(
        key="device_time",
        translation_key="device_time",
        device_class=SensorDeviceClass.TIMESTAMP,
        entity_category=EntityCategory.DIAGNOSTIC,
        value_fn=lambda data: (
            datetime.now(UTC).replace(
                hour=data.device_details.hour,
                minute=data.device_details.minute,
                second=0,
                microsecond=0,
            )
            if data.device_details.hour is not None
            and data.device_details.minute is not None
            else None
        ),
    ),
    CatlinkC08SensorEntityDescription(
        key="wifi_rssi",
        translation_key="wifi_rssi",
        device_class=SensorDeviceClass.SIGNAL_STRENGTH,
        native_unit_of_measurement="dBm",
        state_class=SensorStateClass.MEASUREMENT,
        entity_category=EntityCategory.DIAGNOSTIC,
        value_fn=lambda data: (
            int(data.wifi_info.rssi) if data.wifi_info.rssi else None
        ),
    ),
    CatlinkC08SensorEntityDescription(
        key="wifi_name",
        translation_key="wifi_name",
        entity_category=EntityCategory.DIAGNOSTIC,
        value_fn=lambda data: data.wifi_info.wifi_name,
    ),
    CatlinkC08SensorEntityDescription(
        key="wifi_signal_percent",
        translation_key="wifi_signal_percent",
        native_unit_of_measurement="%",
        state_class=SensorStateClass.MEASUREMENT,
        entity_category=EntityCategory.DIAGNOSTIC,
        value_fn=lambda data: data.wifi_info.wifi_signal_percent,
    ),
)

PET_SENSORS: tuple[CatlinkPetSensorEntityDescription, ...] = (
    CatlinkPetSensorEntityDescription(
        key="weight",
        translation_key="pet_weight",
        device_class=SensorDeviceClass.WEIGHT,
        native_unit_of_measurement=UnitOfMass.KILOGRAMS,
        state_class=SensorStateClass.MEASUREMENT,
        value_fn=lambda pet: pet.weight,
    ),
    CatlinkPetSensorEntityDescription(
        key="age",
        translation_key="pet_age",
        device_class=SensorDeviceClass.DURATION,
        native_unit_of_measurement=UnitOfTime.MONTHS,
        state_class=SensorStateClass.MEASUREMENT,
        value_fn=lambda pet: (
            (pet.age * 12) + pet.month
            if pet.age is not None and pet.month is not None
            else None
        ),
    ),
    CatlinkPetSensorEntityDescription(
        key="gender",
        translation_key="pet_gender",
        device_class=SensorDeviceClass.ENUM,
        options=["male", "female", "unknown"],
        value_fn=lambda pet: (
            "male" if pet.gender == 1 else "female" if pet.gender == 2 else "unknown"
        ),
    ),
    CatlinkPetSensorEntityDescription(
        key="breed",
        translation_key="pet_breed",
        value_fn=lambda pet: pet.breed_name,
    ),
    CatlinkPetSensorEntityDescription(
        key="birthday",
        translation_key="pet_birthday",
        device_class=SensorDeviceClass.TIMESTAMP,
        value_fn=lambda pet: (
            datetime.fromtimestamp(pet.birthday / 1000, tz=UTC)
            if pet.birthday
            else None
        ),
    ),
    CatlinkPetSensorEntityDescription(
        key="pet_type",
        translation_key="pet_type",
        device_class=SensorDeviceClass.ENUM,
        options=["cat", "dog", "other"],
        value_fn=lambda pet: (
            "cat" if pet.type == 1 else "dog" if pet.type == 2 else "other"
        ),
    ),
    CatlinkPetSensorEntityDescription(
        key="body_type",
        translation_key="pet_body_type",
        device_class=SensorDeviceClass.ENUM,
        options=["very_thin", "thin", "normal", "heavy", "very_heavy"],
        value_fn=lambda pet: (
            "very_thin"
            if pet.body_type == 0
            else "thin"
            if pet.body_type == 1
            else "normal"
            if pet.body_type == 2
            else "heavy"
            if pet.body_type == 3
            else "very_heavy"
            if pet.body_type == 4
            else "normal"
        ),
    ),
)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: CatlinkConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up CatLink sensors from a config entry."""
    coordinator = entry.runtime_data.coordinator

    entities: list[SensorEntity] = []

    entities.extend(
        CatlinkSensor(coordinator, device_id, description)
        for device_id in coordinator.data.devices
        for description in SENSORS
        if description.exists_fn(coordinator.data.devices[device_id])
    )

    entities.extend(
        CatlinkPetSensor(coordinator, pet_id, description)
        for pet_id in coordinator.data.pets
        for description in PET_SENSORS
    )

    async_add_entities(entities)


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


class CatlinkPetSensor(CoordinatorEntity[CatlinkDataUpdateCoordinator], SensorEntity):
    """Representation of a CatLink pet sensor."""

    entity_description: CatlinkPetSensorEntityDescription
    _attr_has_entity_name = True

    def __init__(
        self,
        coordinator: CatlinkDataUpdateCoordinator,
        pet_id: str,
        description: CatlinkPetSensorEntityDescription,
    ) -> None:
        """Initialize the pet sensor."""
        super().__init__(coordinator)
        self.entity_description = description
        self._pet_id = pet_id
        self._attr_unique_id = f"pet_{pet_id}_{description.key}"

        pet = coordinator.data.pets[pet_id]
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, f"pet_{pet_id}")},
            name=pet.pet_name or f"Pet {pet_id}",
            manufacturer=MANUFACTURER,
            model="Pet",
        )

    @property
    def native_value(self) -> str | int | float | datetime | None:
        """Return the state of the sensor."""
        pet = self.coordinator.data.pets.get(self._pet_id)
        if not pet:
            return None
        return self.entity_description.value_fn(pet)
