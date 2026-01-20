"""Data models for the CatLink integration."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from pycatlink.account import CatlinkAccount
from pycatlink.device import CatlinkDevice
from pycatlink.models import CatlinkAccountConfig, CatlinkPet

from homeassistant.config_entries import ConfigEntry

if TYPE_CHECKING:
    from .coordinator import CatlinkDataUpdateCoordinator


@dataclass
class CatlinkData:
    """Data for the CatLink integration."""

    account: CatlinkAccount
    coordinator: CatlinkDataUpdateCoordinator


@dataclass
class CatlinkCoordinatorData:
    """Data fetched by the coordinator."""

    account_config: CatlinkAccountConfig
    devices: dict[str, CatlinkDevice]
    pets: dict[str, CatlinkPet]


type CatlinkConfigEntry = ConfigEntry[CatlinkData]
