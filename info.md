![Lake Constance Storm Checker](https://raw.githubusercontent.com/mepruegel/hacs_lakeConstanceStormWarnings/main/custom_components/lake_constance_storm_checker/icon.png)

# Lake Constance Storm Checker

A Home Assistant custom component for monitoring storm warnings for Lake Constance (Bodensee) areas.

## Features

- **Real-time Monitoring**: Automatically polls the API every 5 minutes (configurable)
- **Multiple Sensors**: Status sensors for each area (West, Center, East)
- **Binary Sensors**: Warning indicators for each area and global warnings
- **Custom Names**: Option to customize area names
- **Manual Refresh**: Service to manually refresh data
- **Area Status Service**: Get current status for specific areas
- **German & English Support**: Full translation support
- **Secure Configuration**: Secure storage of API credentials

## Installation

1. Install this integration through HACS
2. Restart Home Assistant
3. Add the integration through the UI

## Configuration

1. Go to **Settings** → **Devices & Services**
2. Click **Add Integration**
3. Search for "Lake Constance Storm Checker"
4. Enter your configuration:
   - **Base URL**: The API base URL
   - **API Code**: Your authentication code for the API
5. Configure additional options:
   - **Update Interval**: How often to poll the API (default: 300 seconds)
   - **Custom Names**: Optional custom names for each area

## Entities

### Sensors
- Status sensors for West, Center, and East areas
- Last update timestamp sensor

### Binary Sensors
- Warning indicators for each area
- Global storm and strong wind warning sensors

## Warning Levels

- `noWarning` - No storm warning active (🟢)
- `StrongWindWarning` - Strong wind warning active (🟡)
- `StormWarning` - Storm warning active (🔴)
- `UnknownStatus` - Unknown status (⚪)
- `NoData` - No data available (⚪)
- `Error` - Error occurred (🔴) 