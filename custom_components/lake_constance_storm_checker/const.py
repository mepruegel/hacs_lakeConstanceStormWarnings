"""Constants for the Lake Constance Storm Checker integration."""
from typing import Final

# Domain
DOMAIN: Final = "lake_constance_storm_checker"

# Configuration keys
CONF_BASE_URL: Final = "base_url"
CONF_API_CODE: Final = "api_code"
CONF_SCAN_INTERVAL: Final = "scan_interval"
CONF_CUSTOM_NAMES: Final = "custom_names"

# Default values
DEFAULT_SCAN_INTERVAL: Final = 300  # 5 minutes
DEFAULT_BASE_URL: Final = "https://your-api-endpoint.com"

# API constants
PARTITION_KEY: Final = "lakeConstance"
API_ENDPOINT: Final = "/api/get-latest-status"

# Warning levels
WARNING_LEVEL_NO_WARNING: Final = "noWarning"
WARNING_LEVEL_STRONG_WIND: Final = "StrongWindWarning"
WARNING_LEVEL_STORM: Final = "StormWarning"
WARNING_LEVEL_UNKNOWN: Final = "UnknownStatus"
WARNING_LEVEL_NO_DATA: Final = "NoData"
WARNING_LEVEL_ERROR: Final = "Error"

# Areas
AREAS: Final = ["west", "center", "east"]

# Sensor types
SENSOR_TYPE_STATUS: Final = "status"
SENSOR_TYPE_LAST_UPDATE: Final = "last_update"

# Binary sensor types
BINARY_SENSOR_TYPE_WARNING: Final = "warning"
BINARY_SENSOR_TYPE_STORM_WARNING: Final = "storm_warning"
BINARY_SENSOR_TYPE_STRONG_WIND_WARNING: Final = "strong_wind_warning"

# Icons
ICON_NO_WARNING: Final = "mdi:weather-sunny"
ICON_STRONG_WIND: Final = "mdi:weather-windy"
ICON_STORM: Final = "mdi:weather-lightning"
ICON_UNKNOWN: Final = "mdi:help-circle"
ICON_NO_DATA: Final = "mdi:database-off"
ICON_ERROR: Final = "mdi:alert-circle"

# Services
SERVICE_REFRESH: Final = "refresh"
SERVICE_GET_AREA_STATUS: Final = "get_area_status"

# Service data keys
SERVICE_DATA_AREA: Final = "area" 