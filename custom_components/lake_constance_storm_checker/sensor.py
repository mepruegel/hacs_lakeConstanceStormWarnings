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

    entities = []
    entities.append(LakeConstanceStatusSensor(coordinator))
    _LOGGER.debug("Created %d sensor entities", len(entities))
    
    async_add_entities(entities)
    _LOGGER.info("Sensor setup completed successfully")


class LakeConstanceStatusSensor(CoordinatorEntity, SensorEntity):
    """Representation of a Lake Constance status sensor."""

    def __init__(self, coordinator: CoordinatorEntity) -> None:
        """Initialize the sensor."""
        _LOGGER.debug("Initializing LakeConstanceStatusSensor")
        super().__init__(coordinator)
        self._attr_unique_id = f"{DOMAIN}_status"
        self._attr_name = "Lake Constance Status"
        _LOGGER.debug("Sensor initialized with unique_id: %s, name: %s", 
                      self._attr_unique_id, self._attr_name)

    @property
    def native_value(self) -> StateType:
        """Return the state of the sensor."""
        if not self.coordinator.data:
            _LOGGER.debug("No coordinator data available, returning 'No Data'")
            return "No Data"
        
        # Return a simple status based on the data
        if "west" in self.coordinator.data:
            _LOGGER.debug("Data contains 'west' field, returning 'Connected'")
            return "Connected"
        
        _LOGGER.debug("Data does not contain expected fields, returning 'No Data'")
        return "No Data"

    @property
    def icon(self) -> str:
        """Return the icon of the sensor."""
        return "mdi:weather-cloudy"

    @property
    def extra_state_attributes(self) -> Dict[str, Any]:
        """Return entity specific state attributes."""
        if not self.coordinator.data:
            _LOGGER.debug("No coordinator data available for attributes")
            return {}

        _LOGGER.debug("Returning data as extra state attributes")
        return {
            "data": self.coordinator.data,
        } 