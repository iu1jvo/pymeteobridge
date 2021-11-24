"""Helper Class for Meteobridge module."""
from __future__ import annotations

import datetime as dt
import logging
import math

from pymeteobridgedata.const import UNIT_TYPE_METRIC
from pymeteobridgedata.data import BeaufortDescription

UTC = dt.timezone.utc

_LOGGER = logging.getLogger(__name__)


class Conversions:
    """Converts values."""

    def __init__(self, units: str, homeassistant: bool) -> None:
        """Set initial values."""
        self.units = units
        self.homeassistant = homeassistant

    def temperature(self, value) -> float:
        """Return celcius to Fahrenheit."""
        if value is None:
            return None

        if value is None or self.units == UNIT_TYPE_METRIC or self.homeassistant:
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
            _LOGGER.error("An error occured converting MB Time. Input Value is : %s and Error message is %s", timestamp, str(e))
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


class Calculations:
    """Calculate entity values."""

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

    def beaufort(self, wind_speed: float) -> BeaufortDescription:
        """Retruns data structure with Beaufort values."""
        if wind_speed is None:
            return None

        if wind_speed > 32.7:
            bft = BeaufortDescription(value=12, description="hurricane")
        elif wind_speed >= 28.5:
            bft = BeaufortDescription(value=11, description="violent_storm")
        elif wind_speed >= 24.5:
            bft = BeaufortDescription(value=10, description="storm")
        elif wind_speed >= 20.8:
            bft = BeaufortDescription(value=9, description="strong_gale")
        elif wind_speed >= 17.2:
            bft = BeaufortDescription(value=8, description="fresh_gale")
        elif wind_speed >= 13.9:
            bft = BeaufortDescription(value=7, description="moderate_gale")
        elif wind_speed >= 10.8:
            bft = BeaufortDescription(value=6, description="strong_breeze")
        elif wind_speed >= 8.0:
            bft = BeaufortDescription(value=5, description="fresh_breeze")
        elif wind_speed >= 5.5:
            bft = BeaufortDescription(value=4, description="moderate_breeze")
        elif wind_speed >= 3.4:
            bft = BeaufortDescription(value=3, description="gentle_breeze")
        elif wind_speed >= 1.6:
            bft = BeaufortDescription(value=2, description="light_breeze")
        elif wind_speed >= 0.3:
            bft = BeaufortDescription(value=1, description="light_air")
        else:
            bft = BeaufortDescription(value=0, description="calm")

        return bft

    def feels_like(
        self,
        air_temperature,
        relative_humidity,
        wind_gust,
        heat_index,
        wind_chill
    ) -> float:
        """Calculate the feel like temperature."""
        if (air_temperature is None
                or relative_humidity is None
                or wind_gust is None
                or heat_index is None
                or wind_chill is None):
            return None

        if air_temperature >= 26.67 and relative_humidity >= 40:
            return heat_index

        if air_temperature <= 10 and wind_gust >= 1.34:
            return wind_chill

        return air_temperature
