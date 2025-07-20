"""Tests for the Lake Constance Storm Checker integration."""
import pytest
from unittest.mock import AsyncMock, patch

from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntryState
from homeassistant.const import CONF_NAME

from custom_components.lake_constance_storm_checker.const import (
    DOMAIN,
    CONF_BASE_URL,
    CONF_API_CODE,
    CONF_SCAN_INTERVAL,
    DEFAULT_SCAN_INTERVAL,
    PARTITION_KEY,
    API_ENDPOINT,
)


@pytest.fixture
def mock_api_response():
    """Mock API response."""
    return {
        "partitionKey": "lakeConstance",
        "timestamp": "2025-01-20T17:27:14+0200",
        "west": "noWarning",
        "center": "StrongWindWarning",
        "east": "StormWarning",
    }


@pytest.fixture
def config_entry():
    """Create a mock config entry."""
    return {
        "entry_id": "test_entry_id",
        "domain": DOMAIN,
        "title": "Lake Constance Storm Checker",
        "data": {
            CONF_BASE_URL: "https://your-api-endpoint.com",
            CONF_API_CODE: "test-api-code",
            CONF_SCAN_INTERVAL: DEFAULT_SCAN_INTERVAL,
        },
        "options": {},
        "source": "user",
        "version": 1,
        "minor_version": 0,
    }


async def test_load_unload_config_entry(hass: HomeAssistant, config_entry) -> None:
    """Test loading and unloading the config entry."""
    with patch(
        "custom_components.lake_constance_storm_checker.LakeConstanceStormCheckerCoordinator._async_update_data",
        return_value={
            "partitionKey": "lakeConstance",
            "timestamp": "2025-01-20T17:27:14+0200",
            "west": "noWarning",
            "center": "StrongWindWarning",
            "east": "StormWarning",
        },
    ):
        # Load the config entry
        entry = hass.config_entries.async_add_entry(config_entry)
        await hass.async_block_till_done()

        assert entry.state == ConfigEntryState.LOADED
        assert len(hass.states.async_entity_ids("sensor")) == 4
        assert len(hass.states.async_entity_ids("binary_sensor")) == 5

        # Unload the config entry
        await hass.config_entries.async_unload(entry.entry_id)
        await hass.async_block_till_done()

        assert entry.state == ConfigEntryState.NOT_LOADED


async def test_sensor_states(hass: HomeAssistant, config_entry, mock_api_response) -> None:
    """Test that sensors are created with correct states."""
    with patch(
        "custom_components.lake_constance_storm_checker.LakeConstanceStormCheckerCoordinator._async_update_data",
        return_value=mock_api_response,
    ):
        # Load the config entry
        entry = hass.config_entries.async_add_entry(config_entry)
        await hass.async_block_till_done()

        # Check sensor states
        west_sensor = hass.states.get("sensor.lake_constance_west_status")
        assert west_sensor is not None
        assert west_sensor.state == "noWarning"

        center_sensor = hass.states.get("sensor.lake_constance_center_status")
        assert center_sensor is not None
        assert center_sensor.state == "StrongWindWarning"

        east_sensor = hass.states.get("sensor.lake_constance_east_status")
        assert east_sensor is not None
        assert east_sensor.state == "StormWarning"

        # Check binary sensor states
        west_warning = hass.states.get("binary_sensor.lake_constance_west_warning")
        assert west_warning is not None
        assert west_warning.state == "off"

        center_warning = hass.states.get("binary_sensor.lake_constance_center_warning")
        assert center_warning is not None
        assert center_warning.state == "on"

        east_warning = hass.states.get("binary_sensor.lake_constance_east_warning")
        assert east_warning is not None
        assert east_warning.state == "on"

        storm_warning = hass.states.get("binary_sensor.lake_constance_storm_warning")
        assert storm_warning is not None
        assert storm_warning.state == "on"

        strong_wind_warning = hass.states.get("binary_sensor.lake_constance_strong_wind_warning")
        assert strong_wind_warning is not None
        assert strong_wind_warning.state == "on"


async def test_api_error_handling(hass: HomeAssistant, config_entry) -> None:
    """Test handling of API errors."""
    with patch(
        "custom_components.lake_constance_storm_checker.LakeConstanceStormCheckerCoordinator._async_update_data",
        side_effect=Exception("API Error"),
    ):
        # Load the config entry
        entry = hass.config_entries.async_add_entry(config_entry)
        await hass.async_block_till_done()

        # Check that sensors are created but in unknown state
        west_sensor = hass.states.get("sensor.lake_constance_west_status")
        assert west_sensor is not None
        assert west_sensor.state == "UnknownStatus"


async def test_services(hass: HomeAssistant, config_entry, mock_api_response) -> None:
    """Test that services are registered and work correctly."""
    with patch(
        "custom_components.lake_constance_storm_checker.LakeConstanceStormCheckerCoordinator._async_update_data",
        return_value=mock_api_response,
    ):
        # Load the config entry
        entry = hass.config_entries.async_add_entry(config_entry)
        await hass.async_block_till_done()

        # Test refresh service
        with patch.object(
            hass.data[DOMAIN][entry.entry_id], "async_request_refresh"
        ) as mock_refresh:
            await hass.services.async_call(DOMAIN, "refresh")
            await hass.async_block_till_done()
            mock_refresh.assert_called_once()

        # Test get area status service
        with patch("custom_components.lake_constance_storm_checker.services._LOGGER") as mock_logger:
            await hass.services.async_call(
                DOMAIN, "get_area_status", {"area": "west"}
            )
            await hass.async_block_till_done()
            mock_logger.info.assert_called() 