"""Data models for CatLink integration."""

from dataclasses import dataclass
from typing import Any

from dataclass_wizard import JSONWizard

from .const import (
    DEFAULT_API_BASE,
    DEFAULT_LANGUAGE,
    DEFAULT_PHONE_INTERNATIONAL_CODE,
    CatlinkWorkModel,
    CatlinkWorkStatus,
)


@dataclass
class CatlinkAccountConfig:
    """Configuration for CatLink account."""

    phone: str
    password: str
    phone_international_code: str = DEFAULT_PHONE_INTERNATIONAL_CODE
    api_base: str = DEFAULT_API_BASE
    language: str = DEFAULT_LANGUAGE
    token: str | None = None

    @property
    def unique_identifier(self) -> str:
        """Return the unique id of the account."""
        return f"{self.phone_international_code}-{self.phone}"


@dataclass
class CatlinkDeviceInfo(JSONWizard):
    """Device information."""

    id: str | None
    mac: str | None
    model: str | None
    device_type: str | None
    device_name: str | None
    current_error_message: str | None


@dataclass
class CatlinkDeviceDetails(JSONWizard):
    """Device details."""

    current_message: str | None
    work_status: CatlinkWorkStatus | None
    work_model: CatlinkWorkModel | None


@dataclass
class CatlinkFeederDeviceDetails(CatlinkDeviceDetails, JSONWizard):
    """Feeder device details."""

    weight: int | None
    error: str | None
    food_out_status: str | None


@dataclass
class CatlinkTimingSettings(JSONWizard):
    """Timing settings for litter box device."""

    id: str | None
    device_id: str | None
    customer_id: str | None
    timing_hour: str | None
    timing_min: str | None
    status: int | None
    repeat: str | None
    create_time: int | None
    update_time: int | None


@dataclass
class CatlinkSharers(JSONWizard):
    """Sharers for litter box device."""

    id: str | None
    user_id: str | None
    nickname: str | None
    avatar: Any | None
    master: int | None
    mobile: str | None


@dataclass
class CatlinkDeviceError(JSONWizard):
    """Device error information."""

    errkey: str | None
    err_desc: str | None
    title: str | None
    reason: str | None
    solution: str | None
    url: str | None
    solution_url: str | None
    error_check_tips: list[str] | None


@dataclass
class CatlinkLitterBoxDeviceDetails(CatlinkDeviceDetails, JSONWizard):
    """Litter box device details."""

    device_type: Any | None
    iot_id: Any | None
    device_id: str | None
    mac: str | None
    device_name: str | None
    master: int | None
    default_status: int | None
    current_message_type: Any | None
    error_alert_flag: bool | None
    run_status: Any | None
    indicator_light: str | None
    paneltone: str | None
    warningtone: str | None
    safe_time: str | None
    alarm_status: Any | None
    temperature: Any | None
    humidity: Any | None
    weight: Any | None
    cat_litter_weight: float | None
    key_lock: str | None
    timing_settings: list[CatlinkTimingSettings] | None
    near_enable_timing: CatlinkTimingSettings | None
    sharers: list[CatlinkSharers] | None
    quiet_enable: bool | None
    quiet_times: Any | None
    firmware_version: str | None
    model: str | None
    timezone_id: str | None
    gmt: str | None
    cat_litter_pave_second: int | None
    current_threshold: Any | None
    induction_times: str | None
    manual_times: str | None
    timer_times: str | None
    clear_times: str | None
    deodorant_countdown: int | None
    litter_countdown: int | None
    show_buy_btn: Any | None
    good_url: Any | None
    mall_code: Any | None
    auto_update_pet_weight: bool | None
    all_timing_toggle: bool | None
    online: bool | None
    pro_model: Any | None
    support_weight_calibration: bool | None
    empty_status: str | None
    clean_status: str | None
    device_error_list: list[CatlinkDeviceError] | None
    error_jump_type: int | None
    litter_type: int | None
    toilet_use_times: Any | None
    toilet_setting_times: Any | None
    empty_state: bool | None
    hour: int | None
    minute: int | None
    garbage_status: str | None
    click_able: Any | None
    real_model: str | None
    toilet_slice_flag: bool | None
    full_times: int | None
    full_close_times: int | None
    box_full_sensitivity: int | None
    voice_enable: int | None
    five_min_burial: Any | None
    auto_burial: bool | None
    continuous_cleaning: bool | None
    multi_cat_reg: int | None
    multi_cat_buy_flag: int | None
    deodorant_enable: bool | None
    replace_garbage_bag: Any | None
    device_weight: Any | None
    kitten_model: bool | None
    fresh_sys_install: Any | None
    auto_switch: Any | None
    timer_switch: Any | None
    sand_pave_level: Any | None
    sand_box_install: Any | None
    off_screen_duration: Any | None
    sandbox_balance: Any | None
    cat_litter_balance: Any | None
    final_status: Any | None
    soft_model: Any | None
    total_clean_times: Any | None
    infrared_switch: Any | None
    dn: Any | None
    watermark: Any | None
    atmosphere_light_switch: Any | None
    camera_switch: Any | None
    fill_light: Any | None
    curtain_status_switch: Any | None
    experience_plan_switch: Any | None
    visual_cloud_storage_record_vo: Any | None
    device_vip_flag: Any | None
    ccare_countdown_timestamp: str | None
    last_heart_beat_timestamp: str | None
    high_edition: bool | None
    ccare_temp_entrance: bool | None
