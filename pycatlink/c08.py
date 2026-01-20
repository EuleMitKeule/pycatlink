"""Litter box class for CatLink."""

from datetime import time

from pycatlink.client import CatlinkApiClient
from pycatlink.exceptions import CatlinkError
from pycatlink.models import CatlinkDeviceInfo

from .const import (
    API_LITTERBOX_ABOUT_DEVICE,
    API_LITTERBOX_ACTION_COMMAND_V3,
    API_LITTERBOX_C08_INFO,
    API_LITTERBOX_C08_WIFI_INFO,
    API_LITTERBOX_CAT_LIST_SELECTABLE,
    API_LITTERBOX_CAT_LITTER_SETTING,
    API_LITTERBOX_CHANGE_MODE,
    API_LITTERBOX_DEEP_CLEAN_AUTO_BURIAL,
    API_LITTERBOX_DEEP_CLEAN_CONTINUOUS_CLEANING,
    API_LITTERBOX_INDICATOR_LIGHT_SETTING,
    API_LITTERBOX_KEY_LOCK,
    API_LITTERBOX_KEYPAD_TONE,
    API_LITTERBOX_KITTY_MODEL_SWITCH,
    API_LITTERBOX_LINKED_PETS,
    API_LITTERBOX_NOTICE_CONFIG_LIST_C08,
    API_LITTERBOX_NOTICE_CONFIG_SET,
    API_LITTERBOX_PET_WEIGHT_AUTO_UPDATE,
    API_LITTERBOX_SAFE_TIME_SETTING,
    API_LITTERBOX_STATS_CATS,
    API_LITTERBOX_STATS_DATA_COMPARE_V2,
    API_LITTERBOX_STATS_LOG_TOP5,
    PARAMETER_ACTION,
    PARAMETER_BEHAVIOR,
    PARAMETER_DEVICE_ID,
    PARAMETER_ENABLE,
    PARAMETER_KIND,
    PARAMETER_LITTER_TYPE,
    PARAMETER_LOCK_STATUS,
    PARAMETER_NOTICE_ITEM,
    PARAMETER_NOTICE_SWITCH,
    PARAMETER_PANEL_TONE,
    PARAMETER_SAFE_TIME,
    PARAMETER_STATUS,
    PARAMETER_TIMES,
    PARAMETER_WORK_MODEL,
    RESPONSE_KEY_CATS,
    RESPONSE_KEY_COMPARE_DATA,
    RESPONSE_KEY_DATA,
    RESPONSE_KEY_DEVICE_INFO,
    RESPONSE_KEY_INFO,
    RESPONSE_KEY_LOG_TOP5,
    RESPONSE_KEY_NOTICE_CONFIGS,
    RESPONSE_KEY_WIFI_INFO,
    CatlinkC08Action,
    CatlinkC08AutoModeSafeTimeOption,
    CatlinkC08Behavior,
    CatlinkC08CatLitterType,
    CatlinkC08IndicatorLightStatus,
    CatlinkC08KeyLockStatus,
    CatlinkC08KeypadKind,
    CatlinkC08KeypadPanelTone,
    CatlinkC08NoticeItem,
    CatlinkC08WorkModel,
    HttpMethod,
)
from .device import CatlinkDevice
from .models import (
    CatlinkC08AboutDevice,
    CatlinkC08DeviceDetails,
    CatlinkC08DeviceStats,
    CatlinkC08LinkedPet,
    CatlinkC08Log,
    CatlinkC08NoticeConfig,
    CatlinkC08PetStats,
    CatlinkC08SelectablePet,
    CatlinkC08WifiInfo,
)


class CatlinkC08Device(CatlinkDevice):
    """Litter box C08 class for CatLink."""

    def __init__(
        self, device_info: CatlinkDeviceInfo, client: CatlinkApiClient
    ) -> None:
        super().__init__(device_info, client)

        self._device_details: CatlinkC08DeviceDetails | None = None
        self._device_logs: list[CatlinkC08Log] | None = None
        self._device_stats: CatlinkC08DeviceStats | None = None
        self._pet_stats: list[CatlinkC08PetStats] | None = None
        self._linked_pets: list[CatlinkC08LinkedPet] | None = None
        self._selectable_pets: list[CatlinkC08SelectablePet] | None = None
        self._wifi_info: CatlinkC08WifiInfo | None = None
        self._notice_configs: list[CatlinkC08NoticeConfig] | None = None
        self._about_device: CatlinkC08AboutDevice | None = None

    @property
    def device_details(self) -> CatlinkC08DeviceDetails:
        """Return the device details."""
        if self._device_details is None:
            raise CatlinkError("Device details not available")

        return self._device_details

    @property
    def device_logs(self) -> list[CatlinkC08Log]:
        """Return the device logs."""
        if self._device_logs is None:
            raise CatlinkError("Device logs not available")

        return self._device_logs

    @property
    def device_stats(self) -> CatlinkC08DeviceStats:
        """Return the device stats."""
        if self._device_stats is None:
            raise CatlinkError("Device stats not available")

        return self._device_stats

    @property
    def pet_stats(self) -> list[CatlinkC08PetStats]:
        """Return the pet stats."""
        if self._pet_stats is None:
            raise CatlinkError("Pet stats not available")

        return self._pet_stats

    @property
    def linked_pets(self) -> list[CatlinkC08LinkedPet]:
        """Return the linked pets."""
        if self._linked_pets is None:
            raise CatlinkError("Linked pets not available")

        return self._linked_pets

    @property
    def selectable_pets(self) -> list[CatlinkC08SelectablePet]:
        """Return the selectable pets."""
        if self._selectable_pets is None:
            raise CatlinkError("Selectable pets not available")

        return self._selectable_pets

    @property
    def wifi_info(self) -> CatlinkC08WifiInfo:
        """Return the WiFi info."""
        if self._wifi_info is None:
            raise CatlinkError("WiFi info not available")

        return self._wifi_info

    @property
    def notice_configs(self) -> list[CatlinkC08NoticeConfig]:
        """Return the notice configurations."""
        if self._notice_configs is None:
            raise CatlinkError("Notice configurations not available")

        return self._notice_configs

    @property
    def about_device(self) -> CatlinkC08AboutDevice:
        """Return the about device information."""
        if self._about_device is None:
            raise CatlinkError("About device information not available")

        return self._about_device

    async def refresh(self) -> None:
        await super().refresh()

        response = await self._client.request_with_auto_login(
            path=API_LITTERBOX_C08_INFO,
            method=HttpMethod.GET,
            parameters={
                PARAMETER_DEVICE_ID: self.device_info.id,
            },
        )

        self._device_details = CatlinkC08DeviceDetails.from_dict(
            response.get(RESPONSE_KEY_DATA, {}).get(RESPONSE_KEY_DEVICE_INFO, {})
        )

        response = await self._client.request_with_auto_login(
            path=API_LITTERBOX_STATS_LOG_TOP5,
            method=HttpMethod.GET,
            parameters={
                PARAMETER_DEVICE_ID: self.device_info.id,
            },
        )

        self._device_logs = [
            CatlinkC08Log.from_dict(response_element)
            for response_element in response.get(RESPONSE_KEY_DATA, {}).get(
                RESPONSE_KEY_LOG_TOP5, []
            )
        ]

        response = await self._client.request_with_auto_login(
            path=API_LITTERBOX_STATS_DATA_COMPARE_V2,
            method=HttpMethod.GET,
            parameters={
                PARAMETER_DEVICE_ID: self.device_info.id,
            },
        )

        self._device_stats = CatlinkC08DeviceStats.from_dict(
            response.get(RESPONSE_KEY_DATA, {}).get(RESPONSE_KEY_COMPARE_DATA, {})
        )

        response = await self._client.request_with_auto_login(
            path=API_LITTERBOX_STATS_CATS,
            method=HttpMethod.GET,
            parameters={
                PARAMETER_DEVICE_ID: self.device_info.id,
            },
        )

        self._pet_stats = [
            CatlinkC08PetStats.from_dict(response_element)
            for response_element in response.get(RESPONSE_KEY_DATA, {}).get(
                RESPONSE_KEY_CATS, []
            )
        ]

        response = await self._client.request_with_auto_login(
            path=API_LITTERBOX_LINKED_PETS,
            method=HttpMethod.GET,
            parameters={
                PARAMETER_DEVICE_ID: self.device_info.id,
            },
        )

        self._linked_pets = [
            CatlinkC08LinkedPet.from_dict(response_element)
            for response_element in response.get(RESPONSE_KEY_DATA, [])
        ]

        response = await self._client.request_with_auto_login(
            path=API_LITTERBOX_CAT_LIST_SELECTABLE,
            method=HttpMethod.GET,
            parameters={
                PARAMETER_DEVICE_ID: self.device_info.id,
            },
        )

        self._selectable_pets = [
            CatlinkC08SelectablePet.from_dict(response_element)
            for response_element in response.get(RESPONSE_KEY_DATA, {}).get(
                RESPONSE_KEY_CATS, []
            )
        ]

        response = await self._client.request_with_auto_login(
            path=API_LITTERBOX_C08_WIFI_INFO,
            method=HttpMethod.GET,
            parameters={
                PARAMETER_DEVICE_ID: self.device_info.id,
            },
        )

        self._wifi_info = CatlinkC08WifiInfo.from_dict(
            response.get(RESPONSE_KEY_DATA, {}).get(RESPONSE_KEY_WIFI_INFO, {})
        )

        response = await self._client.request_with_auto_login(
            path=API_LITTERBOX_NOTICE_CONFIG_LIST_C08,
            method=HttpMethod.GET,
            parameters={
                PARAMETER_DEVICE_ID: self.device_info.id,
            },
        )

        self._notice_configs = [
            CatlinkC08NoticeConfig.from_dict(response_element)
            for response_element in response.get(RESPONSE_KEY_DATA, {}).get(
                RESPONSE_KEY_NOTICE_CONFIGS, []
            )
        ]

        response = await self._client.request_with_auto_login(
            path=API_LITTERBOX_ABOUT_DEVICE,
            method=HttpMethod.GET,
            parameters={
                PARAMETER_DEVICE_ID: self.device_info.id,
            },
        )

        self._about_device = CatlinkC08AboutDevice.from_dict(
            response.get(RESPONSE_KEY_DATA, {}).get(RESPONSE_KEY_INFO, {})
        )

    async def start_clean(self) -> None:
        """Start cleaning the litter box."""
        await self._issue_command(
            path=API_LITTERBOX_ACTION_COMMAND_V3,
            parameters={
                PARAMETER_ACTION: CatlinkC08Action.RUN,
                PARAMETER_BEHAVIOR: CatlinkC08Behavior.CLEAN,
            },
        )

    async def pause_clean(self) -> None:
        """Pause cleaning the litter box."""
        await self._issue_command(
            path=API_LITTERBOX_ACTION_COMMAND_V3,
            parameters={
                PARAMETER_ACTION: CatlinkC08Action.PAUSE,
                PARAMETER_BEHAVIOR: CatlinkC08Behavior.CLEAN,
            },
        )

    async def cancel_clean(self) -> None:
        """Cancel cleaning the litter box."""
        await self._issue_command(
            path=API_LITTERBOX_ACTION_COMMAND_V3,
            parameters={
                PARAMETER_ACTION: CatlinkC08Action.CANCEL,
                PARAMETER_BEHAVIOR: CatlinkC08Behavior.CLEAN,
            },
        )

    async def start_pave(self) -> None:
        """Start paving the litter box."""
        await self._issue_command(
            path=API_LITTERBOX_ACTION_COMMAND_V3,
            parameters={
                PARAMETER_ACTION: CatlinkC08Action.RUN,
                PARAMETER_BEHAVIOR: CatlinkC08Behavior.PAVE,
            },
        )

    async def pause_pave(self) -> None:
        """Pause paving the litter box."""
        await self._issue_command(
            path=API_LITTERBOX_ACTION_COMMAND_V3,
            parameters={
                PARAMETER_ACTION: CatlinkC08Action.PAUSE,
                PARAMETER_BEHAVIOR: CatlinkC08Behavior.PAVE,
            },
        )

    async def set_work_model(self, work_model: CatlinkC08WorkModel) -> None:
        """Select the device work model."""
        await self._issue_command(
            path=API_LITTERBOX_CHANGE_MODE,
            parameters={
                PARAMETER_WORK_MODEL: work_model,
            },
        )

    async def set_pet_weight_auto_update(self, enable: bool) -> None:
        """Enable or disable automatic pet weight update."""
        await self._issue_command(
            path=API_LITTERBOX_PET_WEIGHT_AUTO_UPDATE,
            parameters={
                PARAMETER_ENABLE: enable,
            },
        )

    async def set_cat_litter_type(self, litter_type: CatlinkC08CatLitterType) -> None:
        """Set the cat litter type."""
        await self._issue_command(
            path=API_LITTERBOX_CAT_LITTER_SETTING,
            parameters={
                PARAMETER_LITTER_TYPE: litter_type,
            },
        )

    async def set_quiet_mode(
        self, enable: bool, start_time: time, end_time: time
    ) -> None:
        """Enable or disable quiet mode."""
        await self._issue_command(
            path=API_LITTERBOX_DEEP_CLEAN_AUTO_BURIAL,
            parameters={
                PARAMETER_ENABLE: enable,
                PARAMETER_TIMES: f"{start_time.strftime('%H:%M')}-{end_time.strftime('%H:%M')}",
            },
        )

    async def set_auto_mode_safe_time(
        self, option: CatlinkC08AutoModeSafeTimeOption
    ) -> None:
        """Set the auto mode safe time option."""
        await self._issue_command(
            path=API_LITTERBOX_SAFE_TIME_SETTING,
            parameters={
                PARAMETER_SAFE_TIME: option,
            },
        )

    async def set_kitty_model(self, enable: bool) -> None:
        """Enable or disable kitty model."""
        await self._issue_command(
            path=API_LITTERBOX_KITTY_MODEL_SWITCH,
            parameters={
                PARAMETER_ENABLE: enable,
            },
        )

    async def set_auto_burial(self, enable: bool) -> None:
        """Enable or disable automatic burial."""
        await self._issue_command(
            path=API_LITTERBOX_DEEP_CLEAN_AUTO_BURIAL,
            parameters={
                PARAMETER_ENABLE: enable,
            },
        )

    async def set_continuous_cleaning(self, enable: bool) -> None:
        """Enable or disable continuous cleaning mode."""
        await self._issue_command(
            path=API_LITTERBOX_DEEP_CLEAN_CONTINUOUS_CLEANING,
            parameters={
                PARAMETER_ENABLE: enable,
            },
        )

    async def set_child_lock(self, enable: bool) -> None:
        """Enable or disable child lock."""
        await self._issue_command(
            path=API_LITTERBOX_KEY_LOCK,
            parameters={
                PARAMETER_LOCK_STATUS: CatlinkC08KeyLockStatus.LOCKED
                if enable
                else CatlinkC08KeyLockStatus.UNLOCKED,
            },
        )

    async def set_indicator_light(self, enable: bool) -> None:
        """Enable or disable indicator light."""
        await self._issue_command(
            path=API_LITTERBOX_INDICATOR_LIGHT_SETTING,
            parameters={
                PARAMETER_STATUS: CatlinkC08IndicatorLightStatus.ALWAYS_OPEN
                if enable
                else CatlinkC08IndicatorLightStatus.CLOSED,
            },
        )

    async def set_keypad_tone(
        self,
        enable: bool,
    ) -> None:
        """Set keypad tone."""
        await self._issue_command(
            path=API_LITTERBOX_KEYPAD_TONE,
            parameters={
                PARAMETER_PANEL_TONE: CatlinkC08KeypadPanelTone.ENABLED
                if enable
                else CatlinkC08KeypadPanelTone.DISABLED,
                PARAMETER_KIND: CatlinkC08KeypadKind.DEFAULT,
            },
        )

    async def set_notification(self, item: CatlinkC08NoticeItem, enable: bool) -> None:
        """Enable or disable notification item."""
        await self._issue_command(
            path=API_LITTERBOX_NOTICE_CONFIG_SET,
            parameters={
                PARAMETER_NOTICE_ITEM: item,
                PARAMETER_NOTICE_SWITCH: enable,
            },
        )
