# Changelog

This document will cover all major changes to the module.

## v0.1.22 - 2026-06-07

### Changes
- Merge pull request #2 from iu1jvo/1-fix-return-swversion-as-string-instead-float (16c71a2)
- relese workflow updated to OIDC. (53fedc1)
- fix: resolve swversion type and modernize test infrastructure (76cd6ca)
- chore: update release workflows and package metadata - Update github actions images - Add bump-version workflow for setup.cfg and CHANGELOG.md - Mark package as Production/Stable (was Beta) - Add support for Python 3.11-3.14 - Add maintainer info (Giuliano Favro) (9ba7be8)
- Merge pull request #2 from iu1jvo/main (58928c3)
- Update Changelog.md (c22f8c3)

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
