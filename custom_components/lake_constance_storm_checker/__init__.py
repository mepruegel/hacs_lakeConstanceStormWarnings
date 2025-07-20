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
    _LOGGER.info("Setting up Lake Constance Storm Checker component")
    hass.data.setdefault(DOMAIN, {})
    _LOGGER.debug("Component setup completed successfully")
    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Lake Constance Storm Checker from a config entry."""
    _LOGGER.info("Setting up Lake Constance Storm Checker from config entry: %s", entry.entry_id)
    hass.data.setdefault(DOMAIN, {})

    # Get configuration
    base_url = entry.data[CONF_BASE_URL]
    api_code = entry.data[CONF_API_CODE]
    _LOGGER.debug("Configuration loaded - Base URL: %s, API Code: %s", 
                  base_url, "***" if api_code else "None")

    # Create coordinator
    _LOGGER.debug("Creating coordinator with scan interval: %s seconds", DEFAULT_SCAN_INTERVAL)
    coordinator = LakeConstanceStormCheckerCoordinator(
        hass, base_url, api_code
    )

    # Fetch initial data
    try:
        _LOGGER.debug("Fetching initial data")
        await coordinator.async_config_entry_first_refresh()
        _LOGGER.info("Initial data fetch completed successfully")
    except ConfigEntryNotReady:
        _LOGGER.error("Failed to fetch initial data, config entry not ready")
        await coordinator.async_shutdown()
        raise

    # Store coordinator
    hass.data[DOMAIN][entry.entry_id] = coordinator
    _LOGGER.debug("Coordinator stored in hass.data for entry: %s", entry.entry_id)

    # Set up platforms
    _LOGGER.debug("Setting up platforms: %s", PLATFORMS)
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    _LOGGER.info("Platform setup completed successfully")

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    _LOGGER.info("Unloading Lake Constance Storm Checker config entry: %s", entry.entry_id)
    
    if unload_ok := await hass.config_entries.async_unload_platforms(entry, PLATFORMS):
        coordinator = hass.data[DOMAIN].pop(entry.entry_id)
        _LOGGER.debug("Shutting down coordinator for entry: %s", entry.entry_id)
        await coordinator.async_shutdown()
        _LOGGER.info("Config entry unloaded successfully")
    else:
        _LOGGER.warning("Failed to unload platforms for entry: %s", entry.entry_id)

    return unload_ok


class LakeConstanceStormCheckerCoordinator(DataUpdateCoordinator):
    """Class to manage fetching Lake Constance Storm Checker data."""

    def __init__(
        self, hass: HomeAssistant, base_url: str, api_code: str
    ) -> None:
        """Initialize."""
        _LOGGER.debug("Initializing LakeConstanceStormCheckerCoordinator")
        self.base_url = base_url
        self.api_code = api_code
        self.session = async_get_clientsession(hass)
        _LOGGER.debug("Coordinator initialized with base_url: %s", base_url)

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

        _LOGGER.debug("Fetching data from API - URL: %s", url)
        _LOGGER.debug("Request parameters: %s", {k: v if k != "code" else "***" for k, v in params.items()})

        try:
            async with self.session.get(url, params=params, timeout=10) as response:
                _LOGGER.debug("API response status: %s", response.status)
                
                if response.status == 401 or response.status == 403:
                    _LOGGER.error("Authentication failed - API returned status %s", response.status)
                    raise UpdateFailed("Invalid API code")
                elif response.status != 200:
                    _LOGGER.error("API request failed - Status: %s", response.status)
                    raise UpdateFailed(f"API returned status {response.status}")

                data = await response.json()
                _LOGGER.debug("Successfully received data from API: %s", data)
                return data

        except aiohttp.ClientError as err:
            _LOGGER.error("Connection error during API request: %s", err)
            raise UpdateFailed(f"Connection error: {err}") from err
        except Exception as err:
            _LOGGER.error("Unexpected error during API request: %s", err, exc_info=True)
            raise UpdateFailed(f"Unexpected error: {err}") from err

    async def async_shutdown(self) -> None:
        """Shutdown the coordinator."""
        _LOGGER.debug("Shutting down coordinator")
        if hasattr(self, "session"):
            await self.session.close()
            _LOGGER.debug("Session closed successfully") 