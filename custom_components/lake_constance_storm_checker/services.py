"""Services for Lake Constance Storm Checker."""
import logging
from typing import Any, Dict

from homeassistant.core import HomeAssistant, ServiceCall
from homeassistant.helpers import config_validation as cv
from homeassistant.helpers.typing import ConfigType
import voluptuous as vol

from .const import (
    DOMAIN,
    SERVICE_REFRESH,
    SERVICE_GET_AREA_STATUS,
    SERVICE_DATA_AREA,
    AREAS,
)

_LOGGER = logging.getLogger(__name__)

# Service schemas
SERVICE_REFRESH_SCHEMA = cv.make_entity_service_schema({})

SERVICE_GET_AREA_STATUS_SCHEMA = vol.Schema(
    {
        vol.Required(SERVICE_DATA_AREA): str,
    }
)


async def async_setup_services(hass: HomeAssistant, config: ConfigType) -> None:
    """Set up the services for Lake Constance Storm Checker."""

    async def async_refresh_data(service: ServiceCall) -> None:
        """Refresh the storm warning data."""
        _LOGGER.info("Manual refresh requested for Lake Constance Storm Checker")
        
        # Get all coordinators
        coordinators = hass.data.get(DOMAIN, {})
        
        for entry_id, coordinator in coordinators.items():
            try:
                await coordinator.async_request_refresh()
                _LOGGER.info("Successfully refreshed data for entry %s", entry_id)
            except Exception as err:
                _LOGGER.error("Failed to refresh data for entry %s: %s", entry_id, err)

    async def async_get_area_status(service: ServiceCall) -> None:
        """Get the current status for a specific area."""
        area = service.data.get(SERVICE_DATA_AREA, "").lower()
        
        if area not in AREAS:
            _LOGGER.error("Invalid area specified: %s. Valid areas are: %s", area, AREAS)
            return
        
        _LOGGER.info("Getting status for area: %s", area)
        
        # Get all coordinators
        coordinators = hass.data.get(DOMAIN, {})
        
        for entry_id, coordinator in coordinators.items():
            try:
                if coordinator.data:
                    status = coordinator.data.get(area, "UnknownStatus")
                    timestamp = coordinator.data.get("timestamp", "Unknown")
                    _LOGGER.info(
                        "Area %s status: %s (timestamp: %s) for entry %s",
                        area, status, timestamp, entry_id
                    )
                else:
                    _LOGGER.warning("No data available for entry %s", entry_id)
            except Exception as err:
                _LOGGER.error("Failed to get area status for entry %s: %s", entry_id, err)

    # Register services
    hass.services.async_register(
        DOMAIN,
        SERVICE_REFRESH,
        async_refresh_data,
        schema=SERVICE_REFRESH_SCHEMA,
    )

    hass.services.async_register(
        DOMAIN,
        SERVICE_GET_AREA_STATUS,
        async_get_area_status,
        schema=SERVICE_GET_AREA_STATUS_SCHEMA,
    )


async def async_unload_services(hass: HomeAssistant) -> None:
    """Unload the services for Lake Constance Storm Checker."""
    hass.services.async_remove(DOMAIN, SERVICE_REFRESH)
    hass.services.async_remove(DOMAIN, SERVICE_GET_AREA_STATUS) 