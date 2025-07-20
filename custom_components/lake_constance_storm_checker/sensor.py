"""Sensor platform for Lake Constance Storm Checker."""
from datetime import datetime
from typing import Any, Dict, Optional

from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import StateType
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import (
    DOMAIN,
    AREAS,
    CONF_CUSTOM_NAMES,
    SENSOR_TYPE_STATUS,
    SENSOR_TYPE_LAST_UPDATE,
    WARNING_LEVEL_NO_WARNING,
    WARNING_LEVEL_STRONG_WIND,
    WARNING_LEVEL_STORM,
    WARNING_LEVEL_UNKNOWN,
    WARNING_LEVEL_NO_DATA,
    WARNING_LEVEL_ERROR,
    ICON_NO_WARNING,
    ICON_STRONG_WIND,
    ICON_STORM,
    ICON_UNKNOWN,
    ICON_NO_DATA,
    ICON_ERROR,
)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the Lake Constance Storm Checker sensors."""
    coordinator = hass.data[DOMAIN][config_entry.entry_id]
    custom_names = config_entry.data.get(CONF_CUSTOM_NAMES, {})

    entities = []

    # Add status sensors for each area
    for area in AREAS:
        entities.append(
            LakeConstanceStatusSensor(
                coordinator, area, custom_names.get(area, "")
            )
        )

    # Add last update sensor
    entities.append(LakeConstanceLastUpdateSensor(coordinator))

    async_add_entities(entities)


class LakeConstanceStatusSensor(CoordinatorEntity, SensorEntity):
    """Representation of a Lake Constance area status sensor."""

    def __init__(
        self, coordinator: CoordinatorEntity, area: str, custom_name: str
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        self.area = area
        self.custom_name = custom_name
        self._attr_unique_id = f"{DOMAIN}_{area}_status"
        self._attr_name = (
            f"Lake Constance {area.title()} Status"
            if not custom_name
            else f"{custom_name} Status"
        )

    @property
    def native_value(self) -> StateType:
        """Return the state of the sensor."""
        if not self.coordinator.data:
            return WARNING_LEVEL_UNKNOWN

        return self.coordinator.data.get(self.area, WARNING_LEVEL_UNKNOWN)

    @property
    def icon(self) -> str:
        """Return the icon of the sensor."""
        value = self.native_value
        if value == WARNING_LEVEL_NO_WARNING:
            return ICON_NO_WARNING
        elif value == WARNING_LEVEL_STRONG_WIND:
            return ICON_STRONG_WIND
        elif value == WARNING_LEVEL_STORM:
            return ICON_STORM
        elif value == WARNING_LEVEL_NO_DATA:
            return ICON_NO_DATA
        elif value == WARNING_LEVEL_ERROR:
            return ICON_ERROR
        else:
            return ICON_UNKNOWN

    @property
    def extra_state_attributes(self) -> Dict[str, Any]:
        """Return entity specific state attributes."""
        if not self.coordinator.data:
            return {}

        return {
            "area": self.area,
            "custom_name": self.custom_name,
            "timestamp": self.coordinator.data.get("timestamp"),
            "partition_key": self.coordinator.data.get("partitionKey"),
        }


class LakeConstanceLastUpdateSensor(CoordinatorEntity, SensorEntity):
    """Representation of the last update timestamp sensor."""

    def __init__(self, coordinator: CoordinatorEntity) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._attr_unique_id = f"{DOMAIN}_last_update"
        self._attr_name = "Lake Constance Last Update"

    @property
    def native_value(self) -> Optional[datetime]:
        """Return the state of the sensor."""
        if not self.coordinator.data:
            return None

        timestamp_str = self.coordinator.data.get("timestamp")
        if not timestamp_str:
            return None

        try:
            # Parse the timestamp string to datetime
            # Format: "2025-01-20T17:27:14+0200"
            return datetime.fromisoformat(timestamp_str.replace("+0200", "+02:00"))
        except (ValueError, TypeError):
            return None

    @property
    def icon(self) -> str:
        """Return the icon of the sensor."""
        return "mdi:clock-outline"

    @property
    def extra_state_attributes(self) -> Dict[str, Any]:
        """Return entity specific state attributes."""
        if not self.coordinator.data:
            return {}

        return {
            "partition_key": self.coordinator.data.get("partitionKey"),
            "west_status": self.coordinator.data.get("west"),
            "center_status": self.coordinator.data.get("center"),
            "east_status": self.coordinator.data.get("east"),
        } 