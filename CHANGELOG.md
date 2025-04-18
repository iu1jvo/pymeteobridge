# Change Log

This document will cover all major changes to the module.

## [0.1.21] - 2025-03-08

### Changes
- Added sensors to retrieve the weather station battery status, the sensors are:
  - Main Wind sensor battery
  - Main Temperature/Humidity sensor battery
  - Main Rain sensor battery

## [0.1.17] - 2022-01-08

### Changes

- Wind Chill was until now a Calculated value, as the Meteobridge had issues with WeatherFlow stations and Wind Chill calculations. As this is now fixed, we use the wind_chill value from the Meteobridge station.


## [0.1.16] - 2021-12-16

### Changes

- Added error handling to data processing function, to ensure program does not crash, but instead raises a retry exception.

### Fixed

- Fixing error thrown when wind values are not present.


## [0.1.15] - 2021-12-15

### Changes

- Added `precip_accum_month` and `precip_accum_year` data points. Showing accumulated rain for the current month and for current year.

### Fixed

- If no Wind Values were returned (for whaytever reason) the Beaufort Values would not be filled and causing a crash. Now returning empty values.


## [0.1.14] - 2021-12-06

### Changes

- Added AQI PM2.5 level calculation. Requires a new module called `python-aqi`.
