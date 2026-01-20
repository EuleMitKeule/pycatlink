"""Data models for CatLink integration."""

from dataclasses import dataclass
from typing import Any

from dataclass_wizard import JSONWizard, json_field

from .const import (
    DEFAULT_API_BASE,
    DEFAULT_LANGUAGE,
    CatlinkC08NoticeItem,
    CatlinkC08WorkModel,
    CatlinkC08WorkStatus,
)


@dataclass
class CatlinkAccountConfig:
    """Configuration for CatLink account."""

    phone: str
    password: str
    phone_international_code: str
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
class CatlinkC08TimingSettings(JSONWizard):
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
class CatlinkC08Sharers(JSONWizard):
    """Sharers for litter box device."""

    id: str | None
    user_id: str | None
    nickname: str | None
    avatar: Any | None
    master: int | None
    mobile: str | None


@dataclass
class CatlinkC08DeviceError(JSONWizard):
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
class CatlinkC08DeviceDetails(JSONWizard):
    """Litter box device details."""

    current_message: str | None
    work_status: CatlinkC08WorkStatus | None
    work_model: CatlinkC08WorkModel | None
    device_type: str | None
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
    timing_settings: list[CatlinkC08TimingSettings] | None
    near_enable_timing: CatlinkC08TimingSettings | None
    sharers: list[CatlinkC08Sharers] | None
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
    device_error_list: list[CatlinkC08DeviceError] | None
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
    final_status: str | None
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
    device_vip_flag: bool | None
    ccare_temp_entrance: Any | None
    ccare_countdown_timestamp: str | None
    last_heart_beat_timestamp: str | None
    high_edition: bool | None


@dataclass
class CatlinkC08DeviceStats(JSONWizard):
    """C08 Device statistics data."""

    date: str | None
    healthStatus: str | None
    healthStatusDescription: str | None
    times: int | None
    weightAvg: float | None
    weightAvgOfYesterday: float | None
    weightUnitTip: str | None
    durationAvg: int | None
    timesCompareYesterday: int | None
    weightAvgCompareYesterday: float | None
    durationAvgCompareYesterday: int | None
    weightStatus: Any | None
    healthCalcBasis: Any | None
    weightCalcBasis: Any | None
    healthWeekCursor: int | None
    weightWeekCursor: int | None
    snAvailable: bool | None
    peed: int | None
    pood: int | None


@dataclass
class CatlinkC08PetStats(JSONWizard):
    """C08 Pet statistics information."""

    id: str | None
    petName: str | None
    avatar: Any | None
    attention: bool | None
    defaultStatus: Any | None
    petNoteCount: Any | None
    gender: int | None
    year: Any | None
    age: int | None
    month: int | None
    birthday: int | None
    breedId: str | None
    breedName: str | None
    weight: float | None
    weightUnit: Any | None
    owner: bool | None
    petDeviceCount: int | None
    collarVersion: Any | None
    collarMac: Any | None
    masterUserName: Any | None
    liveStatus: Any | None
    meetDate: Any | None
    meetDateString: Any | None
    meedDays: int | None
    passDate: Any | None
    passDateString: Any | None
    passDays: int | None
    zodiac: Any | None


@dataclass
class CatlinkC08Log(JSONWizard):
    """C08 Log information."""

    id: str | None
    type: str | None
    time: str | None
    event: str | None
    unrecognized: bool | None
    first_section: str | None
    second_section: str | None
    modify_flag: bool | None
    sn_flag: int | None
    pet_id: str | None


@dataclass
class CatlinkC08LinkedPet(JSONWizard):
    """C08 Linked pet information."""

    pet_id: str | None
    avatar: Any | None
    gender: str | None
    birthday: int | None
    pet_name: str | None
    has_face_info: Any | None
    item_enable: bool | None
    weight: str | None
    breed_id: str | None
    breed_name: Any | None
    create_time: int | None
    master: bool | None


@dataclass
class CatlinkPet(JSONWizard):
    """Pet information."""

    id: str | None
    type: int | None
    pet_name: str | None
    breed_id: str | None
    avatar: Any | None
    gender: int | None
    birthday: int | None
    birthday_string: str | None
    weight: float | None
    pet_food_id: Any | None
    live_status: Any | None
    memory_bg_url: Any | None
    meet_date: Any | None
    pass_date: Any | None
    delete_flag: int | None
    create_time: int | None
    update_time: int | None
    sn_factor: int | None
    body_type: int | None
    pet_food_name: Any | None
    master: Any | None
    owner: int | None
    age: int | None
    breed_name: str | None
    avatar_file: Any | None
    user_id: Any | None
    user_nickname: Any | None
    device_ids: Any | None
    feeder_ids: Any | None
    wecare_ids: Any | None
    camera_ids: Any | None
    pure_ids: Any | None
    collar_ids: Any | None
    litterbox_ids: Any | None
    purepro_ids: Any | None
    feederpro_ids: Any | None
    month: int | None
    collars_count: int | None
    selected: bool | None
    default_status: Any | None
    weight_str: Any | None
    report: Any | None
    unit: Any | None
    enabled_collar: Any | None
    meet_date_string: Any | None
    meed_days: int | None
    pass_date_string: Any | None
    pass_days: int | None
    zodiac: Any | None
    hello_text: Any | None
    have_data_2021: Any | None = json_field(keys="haveData2021")


@dataclass
class CatlinkC08WifiInfo(JSONWizard):
    """C08 Wifi information."""

    rssi: str | None
    wifi_name: str | None
    wifi_status: str | None
    wifi_signal_percent: int | None
    band: Any | None


@dataclass
class CatlinkC08NoticeConfig(JSONWizard):
    """C08 Notice configuration."""

    notice_item: CatlinkC08NoticeItem | None
    notice_item_name: str | None
    notice_switch: bool | None
    disabled: bool | None


@dataclass
class CatlinkC08AboutDevice(JSONWizard):
    """C08 About device information."""

    device_name: str | None
    model: str | None
    sn: Any | None
    mac: str | None
    firmware_version: Any | None
    wifi_single: Any | None
    care_start: int | None
    care_end: int | None
