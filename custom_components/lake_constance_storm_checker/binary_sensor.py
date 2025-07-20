"""Binary sensor platform for Lake Constance Storm Checker."""
from typing import Any, Dict

from homeassistant.components.binary_sensor import BinarySensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import (
    DOMAIN,
    AREAS,
    BINARY_SENSOR_TYPE_WARNING,
    BINARY_SENSOR_TYPE_STORM_WARNING,
    BINARY_SENSOR_TYPE_STRONG_WIND_WARNING,
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
    """Set up the Lake Constance Storm Checker binary sensors."""
    coordinator = hass.data[DOMAIN][config_entry.entry_id]
    custom_names = config_entry.data.get("custom_names", {})

    entities = []

    # Add warning sensors for each area
    for area in AREAS:
        entities.append(
            LakeConstanceAreaWarningSensor(
                coordinator, area, custom_names.get(area, "")
            )
        )

    # Add global warning sensors
    entities.append(LakeConstanceStormWarningSensor(coordinator))
    entities.append(LakeConstanceStrongWindWarningSensor(coordinator))

    async_add_entities(entities)


class LakeConstanceAreaWarningSensor(CoordinatorEntity, BinarySensorEntity):
    """Representation of a Lake Constance area warning binary sensor."""

    def __init__(
        self, coordinator: CoordinatorEntity, area: str, custom_name: str
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        self.area = area
        self.custom_name = custom_name
        self._attr_unique_id = f"{coordinator.config_entry_id}_{area}_warning"
        self._attr_name = (
            f"Lake Constance {area.title()} Warning"
            if not custom_name
            else f"{custom_name} Warning"
        )

    @property
    def is_on(self) -> bool:
        """Return true if any warning is active."""
        if not self.coordinator.data:
            return False

        status = self.coordinator.data.get(self.area, WARNING_LEVEL_UNKNOWN)
        return status in [WARNING_LEVEL_STRONG_WIND, WARNING_LEVEL_STORM]

    @property
    def icon(self) -> str:
        """Return the icon of the sensor."""
        if not self.coordinator.data:
            return ICON_UNKNOWN

        status = self.coordinator.data.get(self.area, WARNING_LEVEL_UNKNOWN)
        if status == WARNING_LEVEL_NO_WARNING:
            return ICON_NO_WARNING
        elif status == WARNING_LEVEL_STRONG_WIND:
            return ICON_STRONG_WIND
        elif status == WARNING_LEVEL_STORM:
            return ICON_STORM
        elif status == WARNING_LEVEL_NO_DATA:
            return ICON_NO_DATA
        elif status == WARNING_LEVEL_ERROR:
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
            "status": self.coordinator.data.get(self.area),
            "timestamp": self.coordinator.data.get("timestamp"),
            "partition_key": self.coordinator.data.get("partitionKey"),
        }


class LakeConstanceStormWarningSensor(CoordinatorEntity, BinarySensorEntity):
    """Representation of a global storm warning binary sensor."""

    def __init__(self, coordinator: CoordinatorEntity) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._attr_unique_id = f"{coordinator.config_entry_id}_storm_warning"
        self._attr_name = "Lake Constance Storm Warning"

    @property
    def is_on(self) -> bool:
        """Return true if any area has a storm warning."""
        if not self.coordinator.data:
            return False

        for area in AREAS:
            status = self.coordinator.data.get(area, WARNING_LEVEL_UNKNOWN)
            if status == WARNING_LEVEL_STORM:
                return True
        return False

    @property
    def icon(self) -> str:
        """Return the icon of the sensor."""
        return ICON_STORM if self.is_on else ICON_NO_WARNING

    @property
    def extra_state_attributes(self) -> Dict[str, Any]:
        """Return entity specific state attributes."""
        if not self.coordinator.data:
            return {}

        storm_areas = []
        for area in AREAS:
            status = self.coordinator.data.get(area, WARNING_LEVEL_UNKNOWN)
            if status == WARNING_LEVEL_STORM:
                storm_areas.append(area)

        return {
            "storm_areas": storm_areas,
            "timestamp": self.coordinator.data.get("timestamp"),
            "partition_key": self.coordinator.data.get("partitionKey"),
            "west_status": self.coordinator.data.get("west"),
            "center_status": self.coordinator.data.get("center"),
            "east_status": self.coordinator.data.get("east"),
        }


class LakeConstanceStrongWindWarningSensor(CoordinatorEntity, BinarySensorEntity):
    """Representation of a global strong wind warning binary sensor."""

    def __init__(self, coordinator: CoordinatorEntity) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._attr_unique_id = f"{coordinator.config_entry_id}_strong_wind_warning"
        self._attr_name = "Lake Constance Strong Wind Warning"

    @property
    def is_on(self) -> bool:
        """Return true if any area has a strong wind warning."""
        if not self.coordinator.data:
            return False

        for area in AREAS:
            status = self.coordinator.data.get(area, WARNING_LEVEL_UNKNOWN)
            if status == WARNING_LEVEL_STRONG_WIND:
                return True
        return False

    @property
    def icon(self) -> str:
        """Return the icon of the sensor."""
        return ICON_STRONG_WIND if self.is_on else ICON_NO_WARNING

    @property
    def extra_state_attributes(self) -> Dict[str, Any]:
        """Return entity specific state attributes."""
        if not self.coordinator.data:
            return {}

        strong_wind_areas = []
        for area in AREAS:
            status = self.coordinator.data.get(area, WARNING_LEVEL_UNKNOWN)
            if status == WARNING_LEVEL_STRONG_WIND:
                strong_wind_areas.append(area)

        return {
            "strong_wind_areas": strong_wind_areas,
            "timestamp": self.coordinator.data.get("timestamp"),
            "partition_key": self.coordinator.data.get("partitionKey"),
            "west_status": self.coordinator.data.get("west"),
            "center_status": self.coordinator.data.get("center"),
            "east_status": self.coordinator.data.get("east"),
        } 