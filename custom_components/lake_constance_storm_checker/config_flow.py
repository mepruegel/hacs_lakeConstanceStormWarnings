"""Config flow for Lake Constance Storm Checker integration."""
import logging
import aiohttp
import voluptuous as vol
from typing import Any, Dict, Optional

from homeassistant import config_entries
from homeassistant.core import HomeAssistant
from homeassistant.data_entry_flow import FlowResult
from homeassistant.exceptions import HomeAssistantError

from .const import (
    DOMAIN,
    CONF_BASE_URL,
    CONF_API_CODE,
    DEFAULT_BASE_URL,
    PARTITION_KEY,
    API_ENDPOINT,
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
                    
                    # Create the config entry
                    config_data = {
                        CONF_BASE_URL: base_url,
                        CONF_API_CODE: api_code,
                    }

                    return self.async_create_entry(
                        title="Lake Constance Storm Checker",
                        data=config_data,
                    )

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
                        CONF_BASE_URL, default=DEFAULT_BASE_URL
                    ): str,
                    vol.Required(CONF_API_CODE): str,
                }
            ),
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