# Changelog

## v0.1.22 - 2026-06-07

- Merge pull request #2 from iu1jvo/1-fix-return-swversion-as-string-instead-float (16c71a2)
- relese workflow updated to OIDC. (53fedc1)
- fix: resolve swversion type and modernize test infrastructure (76cd6ca)
- chore: update release workflows and package metadata - Update github actions images - Add bump-version workflow for setup.cfg and CHANGELOG.md - Mark package as Production/Stable (was Beta) - Add support for Python 3.11-3.14 - Add maintainer info (Giuliano Favro) (9ba7be8)
- Merge pull request #2 from iu1jvo/main (58928c3)
- Update Changelog.md (c22f8c3)
- Bump to 0.1.21 (6c4176f)
- Added sensors to retrieve the backup battery status: - Rain Sensor Battery - Temperature/Humidity Sensor Battery - Wind Sensor Battery In case of full integrated meteo station the values are the same. None is returned if the sensors do not exist. (66569eb)
- Added PyCharme folder exlusion in .gitignore (dc343f9)
- Bump to 0.1.20 and ensure / is at the end of external ip (abd0e2a)
- Added possibility to use external address to connect. Bump to 0.1.19 (3959a78)
- Bump to 0.1.18 (edf0003)
- Added Rain last 24 hours (d84fb40)
- Final 0.1.17 release (10cbea1)
- Bump to 0.1.17 (de391cc)
- using wind_chill from Meteobridge (74dc0cd)
- clean up (b0c64fc)
- Final 0.1.16 changes (e6c38d2)
- Fixing https://github.com/briis/meteobridge/issues/18 (5c298e2)
- Added some help for debugging (7dff8cb)
- Bumping to 0.1.16 (613664a)
- 0.1.16 changes (00f8c33)
- Handling bad data errors (9fdb6ef)
- Bumping to V0.1.15 (57e3471)
- 0.1.15 Changes (497b3a1)
- Adding rain month and year. Fixing https://github.com/briis/meteobridge/issues/19 (f05e8b4)
- Fixing https://github.com/briis/meteobridge/issues/18 (462a6e1)
- Added AQI level (c38b66f)
- Bump to 0.1.13 (240dbc4)
- Optimized beaufort function (3278d8d)
- Corrected comments (ea01c28)
- Removed obsolete code (7a08d97)
- PEP formatting (9f1aa26)
- Corrected README options (1132dd1)
- Reconfigured Conversion Functions (281c36d)
- Calculate Wind Chill to ensure availability (ce7912a)
- Raise Badrequest when no station data (286d04a)
- Added error handling for build method (1726c61)
- Removing "" if string data is Empty (521be04)
- Added Air Quality Description (0a2aada)
- Added Wet Bulb Temperature (4e49342)
- Bump to 0.1.12 (7f62584)
- Added Air Density field (14222f6)
- Adjusting station data (fd8a554)
- Added 0 values to empty station data (717a2b0)
- Bump to V0.1.11 (bfad69a)
- Added leaf and soil sensors (ca3a531)
- Bumped to 0.1.10 (2d59fc7)
- Removed unused code (d65084b)
- Ensuring right names (25ccfaa)
- Testing (1fd816f)
- Fixing extra sensor updates (0727404)
- Debug (9644cb3)
- Some debugging (e05d8df)
- Fixing soil and leaf numbering (2024ca7)
- Changed number scheme for extra sensors (7b1a138)
- Bumped to 0.1.9 (e87d1bc)
- Added leaf and soil sensors (dbf94c9)
- Bumped to 0.1.8 (5ed0b03)
- Added more error handling to mbtime_to_utc (7fd24d2)
- Bumped to 1.7 (08b5d3e)
- Error handling for MB Time conversion (0ad56df)
- Updating README (d3739cc)
- Bump to V0.1.6 (0f19035)
- Humidity returned as integer (3db39cb)
- PEP formatting (28f201a)
- Bump to 0.1.5 (2541a56)
- Added indoor temp and humidity (1bf5999)
- Bumped to V0.1.4 (b8b7d11)
- Optimized the Request routine for more speed (63ce8fa)
- Bump to 0.1.3 (4c25d32)
- Fixing NoneType convert error (5122312)
- Bumped to 0.1.2 (f5064a3)
- Changed feels_like formula (f92c93d)
- Updated docs with new parameter (199a10f)
- Code commenting (b1d6abc)
- Rounding on temperature value (c519e5a)
- Rounding feelslike temp (d8959c9)
- Removed unused data field (1909546)
- Added feels like temperature (ac33b33)
- Change to station_pressure (0b16cb6)
- Optimized speed, removed unused data (f555116)
- Merge branch 'main' of https://github.com/briis/pymeteobridge (16f57a6)
- Added Speed Test (e1c9f84)
- Corrected spelling error (3a8c0ab)
- Removed non realtime sensors (3e9651c)
- Removed non essential sensors (6ce8ee2)
- Bumped to 0.1.1 (dea4187)
- Added unit_system function (60d651f)
- Merge branch 'main' of https://github.com/briis/pymeteobridge (13b6de8)
- flake8 cleanup (15b269a)
- Corrected spelling error (71f96ac)
- Updated documentation (1a3c59b)
- Bumped to V0.1.0 (984b8ae)
- Renamed to pymeteobridgedata (86bf4d1)
- Updated docs, changed station to device (5c65227)
- Code cleanup (2892682)
- Added unit conversion (e6dadd2)
- Added observation data (bcffa05)
- Adding initial observation data (77445f8)
- Completed station information (44a83bd)
- Added initial test environment (00ccb67)
- Added setup.cfg (32f26cb)
- Created pymeteobridge (571cae1)
- Initial commit (5c7bca6)

# Changelog

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
