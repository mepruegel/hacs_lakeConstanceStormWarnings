# Lake Constance Storm Checker

A Home Assistant custom component for monitoring storm warnings for Lake Constance (Bodensee) areas. This integration connects to the Lake Constance Storm Checker API to provide real-time storm warning information for the West, Center, and East areas of Lake Constance.

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

### HACS (Recommended)

1. Add this repository to HACS as a custom repository
2. Install the integration through HACS
3. Restart Home Assistant
4. Add the integration through the UI

### Manual Installation

1. Download or clone this repository
2. Copy the `custom_components/lake_constance_storm_checker` folder to your Home Assistant `custom_components` directory
3. Restart Home Assistant
4. Add the integration through the UI

## Configuration

### UI Configuration (Recommended)

1. Go to **Settings** → **Devices & Services**
2. Click **Add Integration**
3. Search for "Lake Constance Storm Checker"
4. Enter your configuration:
   - **Base URL**: The Azure Function base URL (e.g., `https://your-api-endpoint.com`)
   - **API Code**: Your authentication code for the API
5. Configure additional options:
   - **Update Interval**: How often to poll the API (default: 300 seconds)
   - **Custom Names**: Optional custom names for each area

### YAML Configuration

```yaml
# Example configuration.yaml entry
lake_constance_storm_checker:
  base_url: "https://your-api-endpoint.com"
  api_code: "your-api-code-here"
  scan_interval: 300  # 5 minutes
  custom_names:
    west: "Bodensee West"
    center: "Bodensee Mitte"
    east: "Bodensee Ost"
```

## Entities

### Sensors

The integration creates the following sensors:

- `sensor.lake_constance_west_status` - Warning level for West area
- `sensor.lake_constance_center_status` - Warning level for Center area
- `sensor.lake_constance_east_status` - Warning level for East area
- `sensor.lake_constance_last_update` - Last update timestamp

### Binary Sensors

- `binary_sensor.lake_constance_west_warning` - True if any warning active in West
- `binary_sensor.lake_constance_center_warning` - True if any warning active in Center
- `binary_sensor.lake_constance_east_warning` - True if any warning active in East
- `binary_sensor.lake_constance_storm_warning` - True if any area has storm warning
- `binary_sensor.lake_constance_strong_wind_warning` - True if any area has strong wind warning

## Warning Levels

The API returns the following warning levels:

- `noWarning` - No storm warning active (🟢)
- `StrongWindWarning` - Strong wind warning active (🟡)
- `StormWarning` - Storm warning active (🔴)
- `UnknownStatus` - Unknown status (⚪)
- `NoData` - No data available (⚪)
- `Error` - Error occurred (🔴)

## Services

### Refresh Data

Manually refresh the storm warning data:

```yaml
service: lake_constance_storm_checker.refresh
```

### Get Area Status

Get the current status for a specific area:

```yaml
service: lake_constance_storm_checker.get_area_status
data:
  area: west  # Options: west, center, east
```

## API Details

The integration connects to the Lake Constance Storm Checker API using the following endpoint:

```
GET /api/get-latest-status?code={CODE}&partitionKey=lakeConstance&simple=true
```

### Response Format

```json
{
  "partitionKey": "lakeConstance",
  "timestamp": "2025-01-20T17:27:14+0200",
  "west": "noWarning",
  "center": "StrongWindWarning",
  "east": "StormWarning"
}
```

## Troubleshooting

### Common Issues

1. **Connection Error**: Check your base URL and internet connection
2. **Authentication Error**: Verify your API code is correct
3. **No Data**: The API might be temporarily unavailable
4. **Invalid Response**: The API response format might have changed

### Debug Logging

To enable debug logging, add this to your `configuration.yaml`:

```yaml
logger:
  default: info
  logs:
    custom_components.lake_constance_storm_checker: debug
```

### Manual API Test

You can test the API manually using curl:

```bash
curl "https://your-api-endpoint.com/api/get-latest-status?code=YOUR_API_CODE&partitionKey=lakeConstance&simple=true"
```

## Development

### Local Development

1. Clone this repository
2. Install development dependencies: `pip install -r requirements-dev.txt`
3. Run tests: `pytest`
4. Run linting: `pre-commit run --all-files`

### Contributing

1. Fork this repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

For support and questions:

1. Check the [troubleshooting section](#troubleshooting)
2. Search existing [issues](../../issues)
3. Create a new issue with detailed information

## Changelog

### Version 1.0.0
- Initial release
- Support for West, Center, and East areas
- Status and binary sensors
- Manual refresh service
- Area status service
- German and English translations
- Secure configuration storage 