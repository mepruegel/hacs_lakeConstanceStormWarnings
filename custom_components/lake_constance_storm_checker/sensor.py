"""Sensor platform for Lake Constance Storm Checker."""
from typing import Any, Dict

from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import StateType
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the Lake Constance Storm Checker sensors."""
    coordinator = hass.data[DOMAIN][config_entry.entry_id]

    entities = []
    entities.append(LakeConstanceStatusSensor(coordinator))
    async_add_entities(entities)


class LakeConstanceStatusSensor(CoordinatorEntity, SensorEntity):
    """Representation of a Lake Constance status sensor."""

    def __init__(self, coordinator: CoordinatorEntity) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._attr_unique_id = f"{DOMAIN}_status"
        self._attr_name = "Lake Constance Status"

    @property
    def native_value(self) -> StateType:
        """Return the state of the sensor."""
        if not self.coordinator.data:
            return "No Data"
        
        # Return a simple status based on the data
        if "west" in self.coordinator.data:
            return "Connected"
        return "No Data"

    @property
    def icon(self) -> str:
        """Return the icon of the sensor."""
        return "mdi:weather-cloudy"

    @property
    def extra_state_attributes(self) -> Dict[str, Any]:
        """Return entity specific state attributes."""
        if not self.coordinator.data:
            return {}

        return {
            "data": self.coordinator.data,
        } 