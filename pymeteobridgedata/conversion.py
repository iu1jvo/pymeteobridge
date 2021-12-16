"""Helper Class for Meteobridge module."""
from __future__ import annotations

import datetime as dt
import logging
import math
import aqi

from pymeteobridgedata.const import UNIT_TYPE_METRIC
from pymeteobridgedata.data import BeaufortDescription

UTC = dt.timezone.utc

_LOGGER = logging.getLogger(__name__)


class Conversions:
    """Convert and Calculate values."""

    def __init__(self, units: str, homeassistant: bool) -> None:
        """Set initial values."""
        self.units = units
        self.homeassistant = homeassistant

    def temperature(self, value) -> float:
        """Return celcius to Fahrenheit."""
        if value is None:
            return None

        if self.units == UNIT_TYPE_METRIC or self.homeassistant:
            return round(value, 1)
        return round(value * 1.8 + 32, 1)

    def pressure(self, value) -> float:
        """Return inHg from mb/hPa."""
        if value is None:
            return None

        if value is None or self.units == UNIT_TYPE_METRIC:
            return value
        return round(value * 0.029530, 1)

    def rain(self, value) -> float:
        """Convert rain units."""
        if value is None:
            return None

        if self.units == UNIT_TYPE_METRIC:
            return round(value, 2)
        return round(value * 0.03937007874, 2)

    def density(self, value) -> float:
        """Convert air density."""
        if value is None:
            return None

        if self.units == UNIT_TYPE_METRIC:
            return round(value, 1)

        return round(value * 0.06243, 1)

    def distance(self, value) -> float:
        """Conert km to mi."""
        if value is None:
            return None

        if self.units == UNIT_TYPE_METRIC:
            return round(value, 1)

        return round(value * 0.6213688756, 1)

    def windspeed(self, value, wind_unit_kmh: bool = False) -> float:
        """Return miles per hour from m/s."""
        if value is None:
            return value

        if self.units == UNIT_TYPE_METRIC:
            if wind_unit_kmh:
                return round(value * 3.6, 1)
            return round(value, 1)

        return round(value * 2.236936292, 1)

    def utc_from_timestamp(self, timestamp: int) -> dt.datetime:
        """Return UTC time from a timestamp."""
        if timestamp is None:
            return None
        return dt.datetime.utcfromtimestamp(timestamp).replace(tzinfo=UTC)

    def utc_from_mbtime(self, timestamp: str) -> dt.datetime:
        """Return UTC time from a Metobridge timestamp."""
        if timestamp is None or len(timestamp) == 0:
            return None

        try:
            dt_obj = dt.datetime.strptime(timestamp, "%Y%m%d%H%M%S")
            return dt_obj.replace(tzinfo=UTC)
        except Exception as e:
            _LOGGER.error("An error occured converting MB Time. Input Value is : %s and Error message is %s",
                          timestamp, str(e))
            return None

    def hw_platform(self, platform: str) -> str:
        """Return the meteobridge HW Platform."""
        if platform is None:
            return None

        if platform == "CARAMBOLA2":
            return "Meteobridge Pro"

        if platform == "VOCORE2":
            return "Meteobridge Nano"

        return platform

    def is_raining(self, rain_rate):
        """Return true if it is raining."""
        if rain_rate is None:
            return None
        return rain_rate > 0

    def is_freezing(self, temperature):
        """Return true if temperature below 0."""
        if temperature is None:
            return None
        return temperature < 0

    def trend_description(self, value: float) -> str:
        """Return trend description based on value."""
        if value is None:
            return None

        if value > 0:
            return "rising"
        if value < 0:
            return "falling"
        return "steady"

    def visibility(
        self,
        elevation,
        air_temperature,
        relative_humidity,
        dewpoint
    ) -> float:
        """Return calculated visibility."""
        if (elevation is None
                or air_temperature is None
                or relative_humidity is None
                or dewpoint is None):
            return None

        elevation_min = float(2)
        if elevation > 2:
            elevation_min = float(elevation)

        max_visibility = float(3.56972 * math.sqrt(elevation_min))
        percent_reduction_a = float((1.13 * abs(air_temperature - dewpoint) - 1.15) / 10)
        if percent_reduction_a > 1:
            percent_reduction = float(1)
        elif percent_reduction_a < 0.025:
            percent_reduction = float(0.025)
        else:
            percent_reduction = percent_reduction_a

        visibility_km = float(max_visibility * percent_reduction)

        return visibility_km

    def uv_description(self, uv: float) -> str:
        """Return Description based on uv value."""
        if uv is None:
            return None

        if uv >= 10.5:
            return "extreme"
        if uv >= 7.5:
            return "very-high"
        if uv >= 5.5:
            return "high"
        if uv >= 2.5:
            return "moderate"
        if uv > 0:
            return "low"

        return "none"

    def wind_direction(self, wind_bearing: int) -> str:
        """Return Wind Directions String from Wind Bearing."""
        if wind_bearing is None:
            return None

        direction_array = [
            "n",
            "nne",
            "ne",
            "ene",
            "e",
            "ese",
            "se",
            "sse",
            "s",
            "ssw",
            "sw",
            "wsw",
            "w",
            "wnw",
            "nw",
            "nnw",
            "n",
        ]
        return direction_array[int((wind_bearing + 11.25) / 22.5)]

    def beaufort_value(self, wind_speed: float) -> BeaufortDescription:
        """Return Beaufort Value and Description."""
        if wind_speed is None:
            return BeaufortDescription(value=0, description="None")

        mapping_text = {
            "32.7": [12, "hurricane"],
            "28.5": [11, "violent_storm"],
            "24.5": [10, "storm"],
            "20.8": [9, "strong_gale"],
            "17.2": [8, "fresh_gale"],
            "13.9": [7, "moderate_gale"],
            "10.8": [6, "strong_breeze"],
            "8.0": [5, "fresh_breeze"],
            "5.5": [4, "moderate_breeze"],
            "3.4": [3, "gentle_breeze"],
            "1.6": [2, "light_breeze"],
            "0.3": [1, "light_air"],
            "-1": [0, "calm"],
        }
        for k, v in mapping_text.items():
            if wind_speed > float(k):
                return BeaufortDescription(value=v[0], description=v[1])
        return None

    def feels_like(self, temperature, humidity, windspeed):
        """Calculate apparent temperature."""
        if temperature is None or humidity is None or windspeed is None:
            return None

        e_value = (
            humidity * 0.06105 * math.exp((17.27 * temperature) / (237.7 + temperature))
        )
        feelslike_c = temperature + 0.348 * e_value - 0.7 * windspeed - 4.25
        return self.temperature(feelslike_c)

    def air_density(self, temperature: float, station_pressure: float) -> float:
        """Return Air Density."""
        if temperature is None or station_pressure is None:
            return None

        kelvin = temperature + 273.15
        r_specific = 287.058
        decimals = 2

        air_dens = (station_pressure * 100) / (r_specific * kelvin)

        if self.units != UNIT_TYPE_METRIC:
            air_dens = air_dens * 0.06243
            decimals = 4

        return round(air_dens, decimals)

    def wetbulb(self, temp: float, humidity: int, pressure: float) -> float:
        """Return Wet Bulb Temperature.

        Converted from a JS formula made by Gary W Funk
        """
        if temp is None or humidity is None or pressure is None:
            return None

        t = float(temp)
        rh = float(humidity)
        p = float(pressure)

        # Variables
        edifference = 1
        twguess = 0
        previoussign = 1
        incr = 10
        es = 6.112 * math.exp(17.67 * t / (t + 243.5))
        e2 = es * (rh / 100)

        while abs(edifference) > 0.005:
            ewguess = 6.112 * math.exp((17.67 * twguess) / (twguess + 243.5))
            eguess = ewguess - p * (t - twguess) * 0.00066 * (1 + (0.00115 * twguess))
            edifference = e2 - eguess
            if edifference == 0:
                break

            if edifference < 0:
                cursign = -1
                if cursign != previoussign:
                    previoussign = cursign
                    incr = incr / 10
                else:
                    incr = incr
            else:
                cursign = 1
                if cursign != previoussign:
                    previoussign = cursign
                    incr = incr / 10
                else:
                    incr = incr

            twguess = twguess + incr * previoussign

        return twguess

    def aqi_level(self, pm25_value: float) -> int:
        """Return PM2.5 AQI Level."""
        if pm25_value is None:
            return None
        return aqi.to_iaqi(aqi.POLLUTANT_PM25, pm25_value, algo=aqi.ALGO_EPA)

    def aqi_description(self, pm25_havg: float) -> str:
        """Return PM2.5 hourly Air Quality."""
        if pm25_havg is None:
            return None

        if pm25_havg > 109:
            return "severe"
        elif pm25_havg > 54:
            return "very_poor"
        elif pm25_havg > 29:
            return "poor"
        elif pm25_havg > 14:
            return "moderate"
        elif pm25_havg > 6:
            return "fine"
        else:
            return "excellent"

    def wind_chill(self, temperature: float, wind_speed: float) -> float:
        """Return Wind Cill Factor."""
        if temperature is None or wind_speed is None:
            return None

        wind_speed_kmh = wind_speed * 3.6

        twc = (13.12 + 0.6215 * temperature - 11.37 * math.pow(wind_speed_kmh, 0.16)
               + 0.3965 * temperature * math.pow(wind_speed_kmh, 0.16))

        return twc
