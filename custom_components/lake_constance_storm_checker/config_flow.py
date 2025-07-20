"""Config flow for Lake Constance Storm Checker integration."""
import logging
import aiohttp
import voluptuous as vol
from typing import Any, Dict, Optional

from homeassistant import config_entries
from homeassistant.core import HomeAssistant
from homeassistant.data_entry_flow import FlowResult
from homeassistant.exceptions import HomeAssistantError
from homeassistant.const import CONF_NAME

from .const import (
    DOMAIN,
    CONF_BASE_URL,
    CONF_API_CODE,
    CONF_SCAN_INTERVAL,
    CONF_CUSTOM_NAMES,
    DEFAULT_SCAN_INTERVAL,
    DEFAULT_BASE_URL,
    PARTITION_KEY,
    API_ENDPOINT,
    AREAS,
)

_LOGGER = logging.getLogger(__name__)


class LakeConstanceStormCheckerConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Lake Constance Storm Checker."""

    VERSION = 1

    def __init__(self) -> None:
        """Initialize the config flow."""
        self._data: Dict[str, Any] = {}

    async def async_step_user(
        self, user_input: Optional[Dict[str, Any]] = None
    ) -> FlowResult:
        """Handle the initial step."""
        errors = {}

        if user_input is not None:
            try:
                # Validate the input
                base_url = user_input[CONF_BASE_URL].rstrip("/")
                api_code = user_input[CONF_API_CODE].strip()

                if not api_code:
                    errors["base"] = "invalid_auth"
                else:
                    # Test the connection
                    await self._test_connection(base_url, api_code)
                    
                    # Store the data for the next step
                    self._data = {
                        CONF_BASE_URL: base_url,
                        CONF_API_CODE: api_code,
                    }
                    
                    return await self.async_step_options()

            except CannotConnect:
                errors["base"] = "cannot_connect"
            except InvalidAuth:
                errors["base"] = "invalid_auth"
            except Exception:  # pylint: disable=broad-except
                _LOGGER.exception("Unexpected exception")
                errors["base"] = "unknown"

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required(
                        CONF_BASE_URL, default=""
                    ): str,
                    vol.Required(CONF_API_CODE): str,
                }
            ),
            errors=errors,
        )

    async def async_step_options(
        self, user_input: Optional[Dict[str, Any]] = None
    ) -> FlowResult:
        """Handle the options step."""
        errors = {}

        if user_input is not None:
            try:
                # Validate scan interval
                scan_interval = user_input.get(CONF_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL)
                if scan_interval < 60:  # Minimum 1 minute
                    errors["base"] = "invalid_scan_interval"
                else:
                    # Create the config entry
                    config_data = {
                        **self._data,
                        CONF_SCAN_INTERVAL: scan_interval,
                        CONF_CUSTOM_NAMES: {
                            area: user_input.get(f"custom_name_{area}", "")
                            for area in AREAS
                        },
                    }

                    return self.async_create_entry(
                        title="Lake Constance Storm Checker",
                        data=config_data,
                    )

            except Exception:  # pylint: disable=broad-except
                _LOGGER.exception("Unexpected exception")
                errors["base"] = "unknown"

        # Build the schema for custom names
        schema_dict = {
            vol.Optional(CONF_SCAN_INTERVAL, default=DEFAULT_SCAN_INTERVAL): int,
        }
        
        for area in AREAS:
            schema_dict[vol.Optional(f"custom_name_{area}")] = str

        return self.async_show_form(
            step_id="options",
            data_schema=vol.Schema(schema_dict),
            errors=errors,
        )

    async def _test_connection(self, base_url: str, api_code: str) -> None:
        """Test the connection to the API."""
        url = f"{base_url}{API_ENDPOINT}"
        params = {
            "code": api_code,
            "partitionKey": PARTITION_KEY,
            "simple": "true",
        }

        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, params=params, timeout=10) as response:
                    if response.status == 401 or response.status == 403:
                        raise InvalidAuth()
                    elif response.status != 200:
                        raise CannotConnect()
                    
                    data = await response.json()
                    
                    # Validate the response structure
                    required_fields = ["partitionKey", "timestamp", "west", "center", "east"]
                    if not all(field in data for field in required_fields):
                        raise InvalidResponse()
                    
                    # Validate partition key
                    if data.get("partitionKey") != PARTITION_KEY:
                        raise InvalidResponse()

        except aiohttp.ClientError as err:
            _LOGGER.error("Connection error: %s", err)
            raise CannotConnect() from err
        except Exception as err:
            _LOGGER.error("Unexpected error during connection test: %s", err)
            raise CannotConnect() from err


class CannotConnect(HomeAssistantError):
    """Error to indicate we cannot connect."""


class InvalidAuth(HomeAssistantError):
    """Error to indicate there is invalid auth."""


class InvalidResponse(HomeAssistantError):
    """Error to indicate invalid response from API.""" 