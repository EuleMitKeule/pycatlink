"""Switch platform for CatLink integration."""

from __future__ import annotations

from collections.abc import Awaitable, Callable
from dataclasses import dataclass
from datetime import time
import logging
from typing import Any

from pycatlink.c08 import CatlinkC08Device
from pycatlink.const import (
    CatlinkC08IndicatorLightStatus,
    CatlinkC08KeyLockStatus,
    CatlinkC08KeypadPanelTone,
    CatlinkC08NoticeItem,
)
from pycatlink.device import CatlinkDevice

from homeassistant.components.switch import SwitchEntity, SwitchEntityDescription
from homeassistant.const import EntityCategory
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.event import async_call_later

from .coordinator import CatlinkDataUpdateCoordinator
from .entity import CatlinkC08EntityDescription, CatlinkEntity, CatlinkEntityDescription
from .models import CatlinkConfigEntry

_LOGGER = logging.getLogger(__name__)


@dataclass(frozen=True, kw_only=True)
class CatlinkSwitchEntityDescription(SwitchEntityDescription, CatlinkEntityDescription):
    """Describes a CatLink switch entity."""

    is_on_fn: Callable[[CatlinkDevice], bool | None]
    set_fn: Callable[[CatlinkDevice, bool], Awaitable[None]]


@dataclass(frozen=True, kw_only=True)
class CatlinkC08SwitchEntityDescription(
    CatlinkSwitchEntityDescription, CatlinkC08EntityDescription
):
    """Describes a CatLink C08 switch entity."""

    is_on_fn: Callable[[CatlinkC08Device], bool | None]
    set_fn: Callable[[CatlinkC08Device, bool], Awaitable[None]]


SWITCHES: tuple[CatlinkSwitchEntityDescription, ...] = (
    CatlinkC08SwitchEntityDescription(
        key="auto_burial",
        translation_key="auto_burial",
        entity_category=EntityCategory.CONFIG,
        is_on_fn=lambda device: device.device_details.auto_burial,
        set_fn=lambda device, enable: device.set_auto_burial(enable),
    ),
    CatlinkC08SwitchEntityDescription(
        key="child_lock",
        translation_key="child_lock",
        entity_category=EntityCategory.CONFIG,
        is_on_fn=lambda device: device.device_details.key_lock
        == CatlinkC08KeyLockStatus.LOCKED,
        set_fn=lambda device, enable: device.set_child_lock(enable),
    ),
    CatlinkC08SwitchEntityDescription(
        key="continuous_cleaning",
        translation_key="continuous_cleaning",
        entity_category=EntityCategory.CONFIG,
        is_on_fn=lambda device: device.device_details.continuous_cleaning,
        set_fn=lambda device, enable: device.set_continuous_cleaning(enable),
    ),
    CatlinkC08SwitchEntityDescription(
        key="indicator_light",
        translation_key="indicator_light",
        entity_category=EntityCategory.CONFIG,
        is_on_fn=lambda device: device.device_details.indicator_light
        == CatlinkC08IndicatorLightStatus.ALWAYS_OPEN,
        set_fn=lambda device, enable: device.set_indicator_light(enable),
    ),
    CatlinkC08SwitchEntityDescription(
        key="keypad_tone",
        translation_key="keypad_tone",
        entity_category=EntityCategory.CONFIG,
        is_on_fn=lambda device: device.device_details.paneltone
        == CatlinkC08KeypadPanelTone.ENABLED,
        set_fn=lambda device, enable: device.set_keypad_tone(enable),
    ),
    CatlinkC08SwitchEntityDescription(
        key="kitty_model",
        translation_key="kitty_model",
        entity_category=EntityCategory.CONFIG,
        is_on_fn=lambda device: device.device_details.kitten_model,
        set_fn=lambda device, enable: device.set_kitty_model(enable),
    ),
    CatlinkC08SwitchEntityDescription(
        key="pet_weight_auto_update",
        translation_key="pet_weight_auto_update",
        entity_category=EntityCategory.CONFIG,
        is_on_fn=lambda device: device.device_details.auto_update_pet_weight,
        set_fn=lambda device, enable: device.set_pet_weight_auto_update(enable),
    ),
    CatlinkC08SwitchEntityDescription(
        key="quiet_mode",
        translation_key="quiet_mode",
        entity_category=EntityCategory.CONFIG,
        is_on_fn=lambda device: device.device_details.quiet_enable,
        set_fn=lambda device, enable: device.set_quiet_mode(
            enable,
            time.fromisoformat(device.device_details.quiet_times.split("-")[0])
            if device.device_details.quiet_times and "-" in device.device_details.quiet_times
            else time(22, 0),
            time.fromisoformat(device.device_details.quiet_times.split("-")[1])
            if device.device_details.quiet_times and "-" in device.device_details.quiet_times
            else time(8, 0),
        ),
    ),
    CatlinkC08SwitchEntityDescription(
        key="notification_cat_came",
        translation_key="notification_cat_came",
        entity_category=EntityCategory.CONFIG,
        is_on_fn=lambda device: (
            notice_config := next(
                (
                    item
                    for item in device.notice_configs
                    if item.notice_item == CatlinkC08NoticeItem.CAT_CAME
                ),
                None,
            )
        )
        and notice_config.notice_switch,
        set_fn=lambda device, enable: device.set_notification(
            CatlinkC08NoticeItem.CAT_CAME, enable
        ),
    ),
    CatlinkC08SwitchEntityDescription(
        key="notification_box_full",
        translation_key="notification_box_full",
        entity_category=EntityCategory.CONFIG,
        is_on_fn=lambda device: (
            notice_config := next(
                (
                    item
                    for item in device.notice_configs
                    if item.notice_item == CatlinkC08NoticeItem.BOX_FULL
                ),
                None,
            )
        )
        and notice_config.notice_switch,
        set_fn=lambda device, enable: device.set_notification(
            CatlinkC08NoticeItem.BOX_FULL, enable
        ),
    ),
    CatlinkC08SwitchEntityDescription(
        key="notification_replace_garbage_bag",
        translation_key="notification_replace_garbage_bag",
        entity_category=EntityCategory.CONFIG,
        is_on_fn=lambda device: (
            notice_config := next(
                (
                    item
                    for item in device.notice_configs
                    if item.notice_item == CatlinkC08NoticeItem.REPLACE_GARBAGE_BAG
                ),
                None,
            )
        )
        and notice_config.notice_switch,
        set_fn=lambda device, enable: device.set_notification(
            CatlinkC08NoticeItem.REPLACE_GARBAGE_BAG, enable
        ),
    ),
    CatlinkC08SwitchEntityDescription(
        key="notification_wash_scooper",
        translation_key="notification_wash_scooper",
        entity_category=EntityCategory.CONFIG,
        is_on_fn=lambda device: (
            notice_config := next(
                (
                    item
                    for item in device.notice_configs
                    if item.notice_item == CatlinkC08NoticeItem.WASH_SCOOPER
                ),
                None,
            )
        )
        and notice_config.notice_switch,
        set_fn=lambda device, enable: device.set_notification(
            CatlinkC08NoticeItem.WASH_SCOOPER, enable
        ),
    ),
    CatlinkC08SwitchEntityDescription(
        key="notification_replace_deodorant",
        translation_key="notification_replace_deodorant",
        entity_category=EntityCategory.CONFIG,
        is_on_fn=lambda device: (
            notice_config := next(
                (
                    item
                    for item in device.notice_configs
                    if item.notice_item == CatlinkC08NoticeItem.REPLACE_DEODORANT
                ),
                None,
            )
        )
        and notice_config.notice_switch,
        set_fn=lambda device, enable: device.set_notification(
            CatlinkC08NoticeItem.REPLACE_DEODORANT, enable
        ),
    ),
    CatlinkC08SwitchEntityDescription(
        key="notification_litter_not_enough",
        translation_key="notification_litter_not_enough",
        entity_category=EntityCategory.CONFIG,
        is_on_fn=lambda device: (
            notice_config := next(
                (
                    item
                    for item in device.notice_configs
                    if item.notice_item == CatlinkC08NoticeItem.LITTER_NOT_ENOUGH
                ),
                None,
            )
        )
        and notice_config.notice_switch,
        set_fn=lambda device, enable: device.set_notification(
            CatlinkC08NoticeItem.LITTER_NOT_ENOUGH, enable
        ),
    ),
    CatlinkC08SwitchEntityDescription(
        key="notification_sandbox_not_enough",
        translation_key="notification_sandbox_not_enough",
        entity_category=EntityCategory.CONFIG,
        is_on_fn=lambda device: (
            notice_config := next(
                (
                    item
                    for item in device.notice_configs
                    if item.notice_item == CatlinkC08NoticeItem.SANDBOX_NOT_ENOUGH
                ),
                None,
            )
        )
        and notice_config.notice_switch,
        set_fn=lambda device, enable: device.set_notification(
            CatlinkC08NoticeItem.SANDBOX_NOT_ENOUGH, enable
        ),
    ),
    CatlinkC08SwitchEntityDescription(
        key="notification_anti_pinch",
        translation_key="notification_anti_pinch",
        entity_category=EntityCategory.CONFIG,
        is_on_fn=lambda device: (
            notice_config := next(
                (
                    item
                    for item in device.notice_configs
                    if item.notice_item == CatlinkC08NoticeItem.ANTI_PINCH
                ),
                None,
            )
        )
        and notice_config.notice_switch,
        set_fn=lambda device, enable: device.set_notification(
            CatlinkC08NoticeItem.ANTI_PINCH, enable
        ),
    ),
    CatlinkC08SwitchEntityDescription(
        key="notification_firmware_updated",
        translation_key="notification_firmware_updated",
        entity_category=EntityCategory.CONFIG,
        is_on_fn=lambda device: (
            notice_config := next(
                (
                    item
                    for item in device.notice_configs
                    if item.notice_item == CatlinkC08NoticeItem.FIRMWARE_UPDATED
                ),
                None,
            )
        )
        and notice_config.notice_switch,
        set_fn=lambda device, enable: device.set_notification(
            CatlinkC08NoticeItem.FIRMWARE_UPDATED, enable
        ),
    ),
)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: CatlinkConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up CatLink switches from a config entry."""
    coordinator = entry.runtime_data.coordinator

    async_add_entities(
        CatlinkSwitch(coordinator, device_id, description)
        for device_id in coordinator.data.devices
        for description in SWITCHES
        if description.exists_fn(coordinator.data.devices[device_id])
    )


class CatlinkSwitch(CatlinkEntity, SwitchEntity):
    """Representation of a CatLink switch."""

    entity_description: CatlinkSwitchEntityDescription

    def __init__(
        self,
        coordinator: CatlinkDataUpdateCoordinator,
        device_id: str,
        description: CatlinkSwitchEntityDescription,
    ) -> None:
        """Initialize the switch."""
        super().__init__(coordinator, device_id)
        self.entity_description = description
        self._attr_unique_id = f"{device_id}_{description.key}"

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        self._attr_is_on = self.entity_description.is_on_fn(self._device)
        super()._handle_coordinator_update()

    async def async_turn_on(self, **kwargs: Any) -> None:
        """Turn the switch on."""
        await self.entity_description.set_fn(self._device, True)
        self._attr_is_on = True
        self.async_write_ha_state()
        # await self.coordinator.async_request_refresh()

        async def _request_refresh(_):
            await self.coordinator.async_request_refresh()

        async_call_later(self.hass, 10, _request_refresh)

    async def async_turn_off(self, **kwargs: Any) -> None:
        """Turn the switch off."""
        await self.entity_description.set_fn(self._device, False)
        self._attr_is_on = False
        self.async_write_ha_state()
        # await self.coordinator.async_request_refresh()

        async def _request_refresh(_):
            await self.coordinator.async_request_refresh()

        async_call_later(self.hass, 10, _request_refresh)
