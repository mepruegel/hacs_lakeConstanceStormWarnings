"""The Lake Constance Storm Checker integration."""
import logging
from datetime import timedelta
from typing import Any, Dict

import aiohttp

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
    DEFAULT_SCAN_INTERVAL,
    PARTITION_KEY,
    API_ENDPOINT,
)

_LOGGER = logging.getLogger(__name__)

PLATFORMS: list[Platform] = [Platform.SENSOR]


async def async_setup(hass: HomeAssistant, config: Dict[str, Any]) -> bool:
    """Set up the Lake Constance Storm Checker component."""
    hass.data.setdefault(DOMAIN, {})
    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Lake Constance Storm Checker from a config entry."""
    hass.data.setdefault(DOMAIN, {})

    # Get configuration
    base_url = entry.data[CONF_BASE_URL]
    api_code = entry.data[CONF_API_CODE]

    # Create coordinator
    coordinator = LakeConstanceStormCheckerCoordinator(
        hass, base_url, api_code
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

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    if unload_ok := await hass.config_entries.async_unload_platforms(entry, PLATFORMS):
        coordinator = hass.data[DOMAIN].pop(entry.entry_id)
        await coordinator.async_shutdown()

    return unload_ok


class LakeConstanceStormCheckerCoordinator(DataUpdateCoordinator):
    """Class to manage fetching Lake Constance Storm Checker data."""

    def __init__(
        self, hass: HomeAssistant, base_url: str, api_code: str
    ) -> None:
        """Initialize."""
        self.base_url = base_url
        self.api_code = api_code
        self.session = async_get_clientsession(hass)

        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=timedelta(seconds=DEFAULT_SCAN_INTERVAL),
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
                return data

        except aiohttp.ClientError as err:
            raise UpdateFailed(f"Connection error: {err}") from err
        except Exception as err:
            raise UpdateFailed(f"Unexpected error: {err}") from err

    async def async_shutdown(self) -> None:
        """Shutdown the coordinator."""
        if hasattr(self, "session"):
            await self.session.close() 