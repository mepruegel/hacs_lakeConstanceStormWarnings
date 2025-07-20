"""Constants for the Lake Constance Storm Checker integration."""
from typing import Final

# Domain
DOMAIN: Final = "lake_constance_storm_checker"

# Configuration keys
CONF_BASE_URL: Final = "base_url"
CONF_API_CODE: Final = "api_code"

# Default values
DEFAULT_SCAN_INTERVAL: Final = 300  # 5 minutes
DEFAULT_BASE_URL: Final = "https://your-api-endpoint.com"

# API constants
PARTITION_KEY: Final = "lakeConstance"
API_ENDPOINT: Final = "/api/get-latest-status"

# Logging constants
LOG_NAME: Final = "lake_constance_storm_checker"
LOG_PREFIX: Final = "[Lake Constance Storm Checker]" 