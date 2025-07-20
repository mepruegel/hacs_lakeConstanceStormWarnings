"""Binary sensor platform for Lake Constance Storm Checker."""
import logging
from typing import Any, Dict

from homeassistant.components.binary_sensor import BinarySensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the Lake Constance Storm Checker binary sensors."""
    _LOGGER.info("Setting up Lake Constance Storm Checker binary sensors for entry: %s", config_entry.entry_id)
    
    coordinator = hass.data[DOMAIN][config_entry.entry_id]
    _LOGGER.debug("Retrieved coordinator for binary sensor setup")

    entities = [
        LakeConstanceWestWarningBinarySensor(coordinator),
        LakeConstanceCenterWarningBinarySensor(coordinator),
        LakeConstanceEastWarningBinarySensor(coordinator),
        LakeConstanceStormWarningBinarySensor(coordinator),
        LakeConstanceStrongWindWarningBinarySensor(coordinator),
    ]
    _LOGGER.debug("Created %d binary sensor entities", len(entities))
    
    async_add_entities(entities)
    _LOGGER.info("Binary sensor setup completed successfully")


class LakeConstanceWestWarningBinarySensor(CoordinatorEntity, BinarySensorEntity):
    """Representation of a Lake Constance West area warning binary sensor."""

    def __init__(self, coordinator: CoordinatorEntity) -> None:
        """Initialize the binary sensor."""
        _LOGGER.debug("Initializing LakeConstanceWestWarningBinarySensor")
        super().__init__(coordinator)
        self._attr_unique_id = f"{DOMAIN}_west_warning"
        self._attr_name = "Lake Constance West Warning"
        _LOGGER.debug("Binary sensor initialized with unique_id: %s, name: %s", 
                      self._attr_unique_id, self._attr_name)

    @property
    def is_on(self) -> bool:
        """Return true if any warning is active for the west area."""
        if not self.coordinator.data:
            _LOGGER.debug("No coordinator data available, returning False")
            return False
        
        try:
            west_data = self.coordinator.data.get("west")
            if isinstance(west_data, dict):
                status = west_data.get("status", "UnknownStatus")
            elif isinstance(west_data, str):
                status = west_data
            else:
                status = "UnknownStatus"
            
            is_warning = status in ["StrongWindWarning", "StormWarning"]
            _LOGGER.debug("West area warning status: %s (is_warning: %s)", status, is_warning)
            return is_warning
        except Exception as e:
            _LOGGER.error("Error getting west warning status: %s", e)
            return False

    @property
    def icon(self) -> str:
        """Return the icon of the binary sensor."""
        return "mdi:weather-windy" if self.is_on else "mdi:weather-sunny"

    @property
    def extra_state_attributes(self) -> Dict[str, Any]:
        """Return entity specific state attributes."""
        if not self.coordinator.data:
            _LOGGER.debug("No coordinator data available for west warning attributes")
            return {}

        try:
            west_data = self.coordinator.data.get("west")
            if isinstance(west_data, dict):
                _LOGGER.debug("Returning west data as extra state attributes")
                return west_data
            elif isinstance(west_data, str):
                _LOGGER.debug("West data is string, returning as status")
                return {"status": west_data}
            else:
                _LOGGER.debug("West data is unknown type, returning empty")
                return {}
        except Exception as e:
            _LOGGER.error("Error getting west warning attributes: %s", e)
            return {}


class LakeConstanceCenterWarningBinarySensor(CoordinatorEntity, BinarySensorEntity):
    """Representation of a Lake Constance Center area warning binary sensor."""

    def __init__(self, coordinator: CoordinatorEntity) -> None:
        """Initialize the binary sensor."""
        _LOGGER.debug("Initializing LakeConstanceCenterWarningBinarySensor")
        super().__init__(coordinator)
        self._attr_unique_id = f"{DOMAIN}_center_warning"
        self._attr_name = "Lake Constance Center Warning"
        _LOGGER.debug("Binary sensor initialized with unique_id: %s, name: %s", 
                      self._attr_unique_id, self._attr_name)

    @property
    def is_on(self) -> bool:
        """Return true if any warning is active for the center area."""
        if not self.coordinator.data:
            _LOGGER.debug("No coordinator data available, returning False")
            return False
        
        try:
            center_data = self.coordinator.data.get("center")
            if isinstance(center_data, dict):
                status = center_data.get("status", "UnknownStatus")
            elif isinstance(center_data, str):
                status = center_data
            else:
                status = "UnknownStatus"
            
            is_warning = status in ["StrongWindWarning", "StormWarning"]
            _LOGGER.debug("Center area warning status: %s (is_warning: %s)", status, is_warning)
            return is_warning
        except Exception as e:
            _LOGGER.error("Error getting center warning status: %s", e)
            return False

    @property
    def icon(self) -> str:
        """Return the icon of the binary sensor."""
        return "mdi:weather-windy" if self.is_on else "mdi:weather-sunny"

    @property
    def extra_state_attributes(self) -> Dict[str, Any]:
        """Return entity specific state attributes."""
        if not self.coordinator.data:
            _LOGGER.debug("No coordinator data available for center warning attributes")
            return {}

        try:
            center_data = self.coordinator.data.get("center")
            if isinstance(center_data, dict):
                _LOGGER.debug("Returning center data as extra state attributes")
                return center_data
            elif isinstance(center_data, str):
                _LOGGER.debug("Center data is string, returning as status")
                return {"status": center_data}
            else:
                _LOGGER.debug("Center data is unknown type, returning empty")
                return {}
        except Exception as e:
            _LOGGER.error("Error getting center warning attributes: %s", e)
            return {}


class LakeConstanceEastWarningBinarySensor(CoordinatorEntity, BinarySensorEntity):
    """Representation of a Lake Constance East area warning binary sensor."""

    def __init__(self, coordinator: CoordinatorEntity) -> None:
        """Initialize the binary sensor."""
        _LOGGER.debug("Initializing LakeConstanceEastWarningBinarySensor")
        super().__init__(coordinator)
        self._attr_unique_id = f"{DOMAIN}_east_warning"
        self._attr_name = "Lake Constance East Warning"
        _LOGGER.debug("Binary sensor initialized with unique_id: %s, name: %s", 
                      self._attr_unique_id, self._attr_name)

    @property
    def is_on(self) -> bool:
        """Return true if any warning is active for the east area."""
        if not self.coordinator.data:
            _LOGGER.debug("No coordinator data available, returning False")
            return False
        
        try:
            east_data = self.coordinator.data.get("east")
            if isinstance(east_data, dict):
                status = east_data.get("status", "UnknownStatus")
            elif isinstance(east_data, str):
                status = east_data
            else:
                status = "UnknownStatus"
            
            is_warning = status in ["StrongWindWarning", "StormWarning"]
            _LOGGER.debug("East area warning status: %s (is_warning: %s)", status, is_warning)
            return is_warning
        except Exception as e:
            _LOGGER.error("Error getting east warning status: %s", e)
            return False

    @property
    def icon(self) -> str:
        """Return the icon of the binary sensor."""
        return "mdi:weather-windy" if self.is_on else "mdi:weather-sunny"

    @property
    def extra_state_attributes(self) -> Dict[str, Any]:
        """Return entity specific state attributes."""
        if not self.coordinator.data:
            _LOGGER.debug("No coordinator data available for east warning attributes")
            return {}

        try:
            east_data = self.coordinator.data.get("east")
            if isinstance(east_data, dict):
                _LOGGER.debug("Returning east data as extra state attributes")
                return east_data
            elif isinstance(east_data, str):
                _LOGGER.debug("East data is string, returning as status")
                return {"status": east_data}
            else:
                _LOGGER.debug("East data is unknown type, returning empty")
                return {}
        except Exception as e:
            _LOGGER.error("Error getting east warning attributes: %s", e)
            return {}


class LakeConstanceStormWarningBinarySensor(CoordinatorEntity, BinarySensorEntity):
    """Representation of a Lake Constance storm warning binary sensor."""

    def __init__(self, coordinator: CoordinatorEntity) -> None:
        """Initialize the binary sensor."""
        _LOGGER.debug("Initializing LakeConstanceStormWarningBinarySensor")
        super().__init__(coordinator)
        self._attr_unique_id = f"{DOMAIN}_storm_warning"
        self._attr_name = "Lake Constance Storm Warning"
        _LOGGER.debug("Binary sensor initialized with unique_id: %s, name: %s", 
                      self._attr_unique_id, self._attr_name)

    @property
    def is_on(self) -> bool:
        """Return true if any area has a storm warning."""
        if not self.coordinator.data:
            _LOGGER.debug("No coordinator data available, returning False")
            return False
        
        try:
            areas = ["west", "center", "east"]
            for area in areas:
                area_data = self.coordinator.data.get(area)
                if isinstance(area_data, dict):
                    status = area_data.get("status", "UnknownStatus")
                elif isinstance(area_data, str):
                    status = area_data
                else:
                    status = "UnknownStatus"
                
                if status == "StormWarning":
                    _LOGGER.debug("Storm warning detected in %s area", area)
                    return True
            
            _LOGGER.debug("No storm warnings detected in any area")
            return False
        except Exception as e:
            _LOGGER.error("Error checking for storm warnings: %s", e)
            return False

    @property
    def icon(self) -> str:
        """Return the icon of the binary sensor."""
        return "mdi:weather-lightning" if self.is_on else "mdi:weather-sunny"

    @property
    def extra_state_attributes(self) -> Dict[str, Any]:
        """Return entity specific state attributes."""
        if not self.coordinator.data:
            _LOGGER.debug("No coordinator data available for storm warning attributes")
            return {}

        try:
            # Return which areas have storm warnings
            areas_with_storm_warning = []
            areas = ["west", "center", "east"]
            
            for area in areas:
                area_data = self.coordinator.data.get(area)
                if isinstance(area_data, dict):
                    status = area_data.get("status", "UnknownStatus")
                elif isinstance(area_data, str):
                    status = area_data
                else:
                    status = "UnknownStatus"
                
                if status == "StormWarning":
                    areas_with_storm_warning.append(area)
            
            _LOGGER.debug("Areas with storm warning: %s", areas_with_storm_warning)
            return {
                "areas_with_storm_warning": areas_with_storm_warning,
                "full_data": self.coordinator.data
            }
        except Exception as e:
            _LOGGER.error("Error getting storm warning attributes: %s", e)
            return {}


class LakeConstanceStrongWindWarningBinarySensor(CoordinatorEntity, BinarySensorEntity):
    """Representation of a Lake Constance strong wind warning binary sensor."""

    def __init__(self, coordinator: CoordinatorEntity) -> None:
        """Initialize the binary sensor."""
        _LOGGER.debug("Initializing LakeConstanceStrongWindWarningBinarySensor")
        super().__init__(coordinator)
        self._attr_unique_id = f"{DOMAIN}_strong_wind_warning"
        self._attr_name = "Lake Constance Strong Wind Warning"
        _LOGGER.debug("Binary sensor initialized with unique_id: %s, name: %s", 
                      self._attr_unique_id, self._attr_name)

    @property
    def is_on(self) -> bool:
        """Return true if any area has a strong wind warning."""
        if not self.coordinator.data:
            _LOGGER.debug("No coordinator data available, returning False")
            return False
        
        try:
            areas = ["west", "center", "east"]
            for area in areas:
                area_data = self.coordinator.data.get(area)
                if isinstance(area_data, dict):
                    status = area_data.get("status", "UnknownStatus")
                elif isinstance(area_data, str):
                    status = area_data
                else:
                    status = "UnknownStatus"
                
                if status == "StrongWindWarning":
                    _LOGGER.debug("Strong wind warning detected in %s area", area)
                    return True
            
            _LOGGER.debug("No strong wind warnings detected in any area")
            return False
        except Exception as e:
            _LOGGER.error("Error checking for strong wind warnings: %s", e)
            return False

    @property
    def icon(self) -> str:
        """Return the icon of the binary sensor."""
        return "mdi:weather-windy" if self.is_on else "mdi:weather-sunny"

    @property
    def extra_state_attributes(self) -> Dict[str, Any]:
        """Return entity specific state attributes."""
        if not self.coordinator.data:
            _LOGGER.debug("No coordinator data available for strong wind warning attributes")
            return {}

        try:
            # Return which areas have strong wind warnings
            areas_with_strong_wind_warning = []
            areas = ["west", "center", "east"]
            
            for area in areas:
                area_data = self.coordinator.data.get(area)
                if isinstance(area_data, dict):
                    status = area_data.get("status", "UnknownStatus")
                elif isinstance(area_data, str):
                    status = area_data
                else:
                    status = "UnknownStatus"
                
                if status == "StrongWindWarning":
                    areas_with_strong_wind_warning.append(area)
            
            _LOGGER.debug("Areas with strong wind warning: %s", areas_with_strong_wind_warning)
            return {
                "areas_with_strong_wind_warning": areas_with_strong_wind_warning,
                "full_data": self.coordinator.data
            }
        except Exception as e:
            _LOGGER.error("Error getting strong wind warning attributes: %s", e)
            return {} 