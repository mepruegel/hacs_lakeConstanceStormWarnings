"""The Lake Constance Storm Checker integration."""
import logging
from datetime import timedelta
from typing import Any, Dict

import aiohttp
import voluptuous as vol

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import ConfigEntryNotReady
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import (
    DOMAIN,
    CONF_BASE_URL,
    CONF_API_CODE,
    CONF_SCAN_INTERVAL,
    DEFAULT_SCAN_INTERVAL,
    PARTITION_KEY,
    API_ENDPOINT,
    AREAS,
)
from . import services
from .config_flow import LakeConstanceStormCheckerConfigFlow

_LOGGER = logging.getLogger(__name__)

PLATFORMS: list[Platform] = [Platform.SENSOR, Platform.BINARY_SENSOR]


async def async_setup(hass: HomeAssistant, config: Dict[str, Any]) -> bool:
    """Set up the Lake Constance Storm Checker component."""
    hass.data.setdefault(DOMAIN, {})
    
    # Register config flow
    hass.config_entries.flow.async_register_flow_handler(
        DOMAIN, LakeConstanceStormCheckerConfigFlow
    )
    
    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Lake Constance Storm Checker from a config entry."""
    hass.data.setdefault(DOMAIN, {})

    # Get configuration
    base_url = entry.data[CONF_BASE_URL]
    api_code = entry.data[CONF_API_CODE]
    scan_interval = entry.data.get(CONF_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL)

    # Create coordinator
    coordinator = LakeConstanceStormCheckerCoordinator(
        hass, base_url, api_code, scan_interval
    )

    # Fetch initial data
    try:
        await coordinator.async_config_entry_first_refresh()
    except ConfigEntryNotReady:
        await coordinator.async_shutdown()
        raise

    # Store coordinator
    hass.data[DOMAIN][entry.entry_id] = coordinator

    # Set up platforms
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    # Set up services
    await services.async_setup_services(hass, entry.data)

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    if unload_ok := await hass.config_entries.async_unload_platforms(entry, PLATFORMS):
        coordinator = hass.data[DOMAIN].pop(entry.entry_id)
        await coordinator.async_shutdown()

        # Unload services if no more entries
        if not hass.data[DOMAIN]:
            await services.async_unload_services(hass)

    return unload_ok


class LakeConstanceStormCheckerCoordinator(DataUpdateCoordinator):
    """Class to manage fetching Lake Constance Storm Checker data."""

    def __init__(
        self, hass: HomeAssistant, base_url: str, api_code: str, scan_interval: int
    ) -> None:
        """Initialize."""
        self.base_url = base_url
        self.api_code = api_code
        self.session = async_get_clientsession(hass)

        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=timedelta(seconds=scan_interval),
        )

    async def _async_update_data(self) -> Dict[str, Any]:
        """Update data via API."""
        url = f"{self.base_url}{API_ENDPOINT}"
        params = {
            "code": self.api_code,
            "partitionKey": PARTITION_KEY,
            "simple": "true",
        }

        try:
            async with self.session.get(url, params=params, timeout=10) as response:
                if response.status == 401 or response.status == 403:
                    raise UpdateFailed("Invalid API code")
                elif response.status != 200:
                    raise UpdateFailed(f"API returned status {response.status}")

                data = await response.json()

                # Validate response structure
                required_fields = ["partitionKey", "timestamp", "west", "center", "east"]
                if not all(field in data for field in required_fields):
                    raise UpdateFailed("Invalid response structure")

                # Validate partition key
                if data.get("partitionKey") != PARTITION_KEY:
                    raise UpdateFailed("Invalid partition key")

                return data

        except aiohttp.ClientError as err:
            raise UpdateFailed(f"Connection error: {err}") from err
        except Exception as err:
            raise UpdateFailed(f"Unexpected error: {err}") from err

    async def async_shutdown(self) -> None:
        """Shutdown the coordinator."""
        if hasattr(self, "session"):
            await self.session.close() 