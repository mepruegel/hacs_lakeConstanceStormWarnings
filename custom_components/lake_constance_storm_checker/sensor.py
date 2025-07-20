"""Sensor platform for Lake Constance Storm Checker."""
import logging
from typing import Any, Dict

from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import StateType
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the Lake Constance Storm Checker sensors."""
    _LOGGER.info("Setting up Lake Constance Storm Checker sensors for entry: %s", config_entry.entry_id)
    
    coordinator = hass.data[DOMAIN][config_entry.entry_id]
    _LOGGER.debug("Retrieved coordinator for sensor setup")

    entities = [
        LakeConstanceWestStatusSensor(coordinator),
        LakeConstanceCenterStatusSensor(coordinator),
        LakeConstanceEastStatusSensor(coordinator),
        LakeConstanceLastUpdateSensor(coordinator),
    ]
    _LOGGER.debug("Created %d sensor entities", len(entities))
    
    async_add_entities(entities)
    _LOGGER.info("Sensor setup completed successfully")


class LakeConstanceWestStatusSensor(CoordinatorEntity, SensorEntity):
    """Representation of a Lake Constance West area status sensor."""

    def __init__(self, coordinator: CoordinatorEntity) -> None:
        """Initialize the sensor."""
        _LOGGER.debug("Initializing LakeConstanceWestStatusSensor")
        super().__init__(coordinator)
        self._attr_unique_id = f"{DOMAIN}_west_status"
        self._attr_name = "Lake Constance West Status"
        _LOGGER.debug("Sensor initialized with unique_id: %s, name: %s", 
                      self._attr_unique_id, self._attr_name)

    @property
    def native_value(self) -> StateType:
        """Return the state of the sensor."""
        if not self.coordinator.data:
            _LOGGER.debug("No coordinator data available, returning 'NoData'")
            return "NoData"
        
        try:
            west_data = self.coordinator.data.get("west", {})
            status = west_data.get("status", "UnknownStatus")
            _LOGGER.debug("West area status: %s", status)
            return status
        except Exception as e:
            _LOGGER.error("Error getting west status: %s", e)
            return "Error"

    @property
    def icon(self) -> str:
        """Return the icon of the sensor."""
        status = self.native_value
        icon_map = {
            "noWarning": "mdi:weather-sunny",
            "StrongWindWarning": "mdi:weather-windy",
            "StormWarning": "mdi:weather-lightning",
            "UnknownStatus": "mdi:help-circle",
            "NoData": "mdi:database-off",
            "Error": "mdi:alert-circle",
        }
        return icon_map.get(status, "mdi:help-circle")

    @property
    def extra_state_attributes(self) -> Dict[str, Any]:
        """Return entity specific state attributes."""
        if not self.coordinator.data:
            _LOGGER.debug("No coordinator data available for west attributes")
            return {}

        try:
            west_data = self.coordinator.data.get("west", {})
            _LOGGER.debug("Returning west data as extra state attributes")
            return west_data
        except Exception as e:
            _LOGGER.error("Error getting west attributes: %s", e)
            return {}


class LakeConstanceCenterStatusSensor(CoordinatorEntity, SensorEntity):
    """Representation of a Lake Constance Center area status sensor."""

    def __init__(self, coordinator: CoordinatorEntity) -> None:
        """Initialize the sensor."""
        _LOGGER.debug("Initializing LakeConstanceCenterStatusSensor")
        super().__init__(coordinator)
        self._attr_unique_id = f"{DOMAIN}_center_status"
        self._attr_name = "Lake Constance Center Status"
        _LOGGER.debug("Sensor initialized with unique_id: %s, name: %s", 
                      self._attr_unique_id, self._attr_name)

    @property
    def native_value(self) -> StateType:
        """Return the state of the sensor."""
        if not self.coordinator.data:
            _LOGGER.debug("No coordinator data available, returning 'NoData'")
            return "NoData"
        
        try:
            center_data = self.coordinator.data.get("center", {})
            status = center_data.get("status", "UnknownStatus")
            _LOGGER.debug("Center area status: %s", status)
            return status
        except Exception as e:
            _LOGGER.error("Error getting center status: %s", e)
            return "Error"

    @property
    def icon(self) -> str:
        """Return the icon of the sensor."""
        status = self.native_value
        icon_map = {
            "noWarning": "mdi:weather-sunny",
            "StrongWindWarning": "mdi:weather-windy",
            "StormWarning": "mdi:weather-lightning",
            "UnknownStatus": "mdi:help-circle",
            "NoData": "mdi:database-off",
            "Error": "mdi:alert-circle",
        }
        return icon_map.get(status, "mdi:help-circle")

    @property
    def extra_state_attributes(self) -> Dict[str, Any]:
        """Return entity specific state attributes."""
        if not self.coordinator.data:
            _LOGGER.debug("No coordinator data available for center attributes")
            return {}

        try:
            center_data = self.coordinator.data.get("center", {})
            _LOGGER.debug("Returning center data as extra state attributes")
            return center_data
        except Exception as e:
            _LOGGER.error("Error getting center attributes: %s", e)
            return {}


class LakeConstanceEastStatusSensor(CoordinatorEntity, SensorEntity):
    """Representation of a Lake Constance East area status sensor."""

    def __init__(self, coordinator: CoordinatorEntity) -> None:
        """Initialize the sensor."""
        _LOGGER.debug("Initializing LakeConstanceEastStatusSensor")
        super().__init__(coordinator)
        self._attr_unique_id = f"{DOMAIN}_east_status"
        self._attr_name = "Lake Constance East Status"
        _LOGGER.debug("Sensor initialized with unique_id: %s, name: %s", 
                      self._attr_unique_id, self._attr_name)

    @property
    def native_value(self) -> StateType:
        """Return the state of the sensor."""
        if not self.coordinator.data:
            _LOGGER.debug("No coordinator data available, returning 'NoData'")
            return "NoData"
        
        try:
            east_data = self.coordinator.data.get("east", {})
            status = east_data.get("status", "UnknownStatus")
            _LOGGER.debug("East area status: %s", status)
            return status
        except Exception as e:
            _LOGGER.error("Error getting east status: %s", e)
            return "Error"

    @property
    def icon(self) -> str:
        """Return the icon of the sensor."""
        status = self.native_value
        icon_map = {
            "noWarning": "mdi:weather-sunny",
            "StrongWindWarning": "mdi:weather-windy",
            "StormWarning": "mdi:weather-lightning",
            "UnknownStatus": "mdi:help-circle",
            "NoData": "mdi:database-off",
            "Error": "mdi:alert-circle",
        }
        return icon_map.get(status, "mdi:help-circle")

    @property
    def extra_state_attributes(self) -> Dict[str, Any]:
        """Return entity specific state attributes."""
        if not self.coordinator.data:
            _LOGGER.debug("No coordinator data available for east attributes")
            return {}

        try:
            east_data = self.coordinator.data.get("east", {})
            _LOGGER.debug("Returning east data as extra state attributes")
            return east_data
        except Exception as e:
            _LOGGER.error("Error getting east attributes: %s", e)
            return {}


class LakeConstanceLastUpdateSensor(CoordinatorEntity, SensorEntity):
    """Representation of a Lake Constance last update timestamp sensor."""

    def __init__(self, coordinator: CoordinatorEntity) -> None:
        """Initialize the sensor."""
        _LOGGER.debug("Initializing LakeConstanceLastUpdateSensor")
        super().__init__(coordinator)
        self._attr_unique_id = f"{DOMAIN}_last_update"
        self._attr_name = "Lake Constance Last Update"
        _LOGGER.debug("Sensor initialized with unique_id: %s, name: %s", 
                      self._attr_unique_id, self._attr_name)

    @property
    def native_value(self) -> StateType:
        """Return the state of the sensor."""
        if not self.coordinator.data:
            _LOGGER.debug("No coordinator data available, returning 'NoData'")
            return "NoData"
        
        try:
            # Try to get timestamp from the data
            timestamp = self.coordinator.data.get("timestamp") or self.coordinator.data.get("lastUpdate")
            if timestamp:
                _LOGGER.debug("Last update timestamp: %s", timestamp)
                return timestamp
            else:
                _LOGGER.debug("No timestamp found in data")
                return "NoData"
        except Exception as e:
            _LOGGER.error("Error getting last update: %s", e)
            return "Error"

    @property
    def icon(self) -> str:
        """Return the icon of the sensor."""
        value = self.native_value
        if value in ["NoData", "Error"]:
            return "mdi:database-off"
        return "mdi:clock-outline"

    @property
    def extra_state_attributes(self) -> Dict[str, Any]:
        """Return entity specific state attributes."""
        if not self.coordinator.data:
            _LOGGER.debug("No coordinator data available for last update attributes")
            return {}

        try:
            # Return the full data as attributes for debugging
            _LOGGER.debug("Returning full data as extra state attributes")
            return {"full_data": self.coordinator.data}
        except Exception as e:
            _LOGGER.error("Error getting last update attributes: %s", e)
            return {} 