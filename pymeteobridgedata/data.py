"""Dataclasses for pymeteobridgedata."""
from __future__ import annotations

from dataclasses import dataclass


@dataclass
class DataLoggerDescription:
    """A class describing a stion configuration."""

    key: str
    mac: str | None = None
    swversion: float | None = None
    platform: str | None = None
    station: str | None = None
    timezone: str | None = None
    uptime: int | None = None
    ip: str | None = None


@dataclass
class ObservationDescription:
    """A class describing realtime weather data."""

    key: str

    timestamp: int | None = None
    temperature: float | None = None
    pressure: float | None = None
    windchill: float | None = None
    air_pollution: float | None = None
    air_pm_25: float | None = None
    air_pm_1: float | None = None
    heatindex: float | None = None
    humidity: int | None = None
    windspeedavg: float | None = None
    windgust: float | None = None
    windspeed: float | None = None
    windbearing: int | None = None
    wind_cardinal: str | None = None
    raintoday: float | None = None
    rainrate: float | None = None
    dewpoint: float | None = None
    is_lowbat: bool | None = None
    is_raining: bool | None = None
    is_freezing: bool | None = None
    in_temperature: float | None = None
    in_humidity: int | None = None
    temphigh: float | None = None
    templow: float | None = None
    uvindex: float | None = None
    solarrad: float | None = None
    temp_month_min: float | None = None
    temp_month_max: float | None = None
    temp_year_min: float | None = None
    temp_year_max: float | None = None
    wind_month_max: float | None = None
    wind_year_max: float | None = None
    rain_month_max: float | None = None
    rain_year_max: float | None = None
    rainrate_month_max: float | None = None
    rainrate_year_max: float | None = None
    lightning_count: float | None = None
    lightning_energy: float | None = None
    lightning_distance: float | None = None
    bft_value: int | None = None
    beaufort_description: str | None = None
    trend_temperature: float | None = None
    temperature_trend: str | None = None
    trend_pressure: float | None = None
    pressure_trend: str | None = None
    absolute_pressure: float | None = None
    forecast: str | None = None
    temperature_2: float | None = None
    humidity_2: float | None = None
    heatindex_2: float | None = None
    temperature_3: float | None = None
    humidity_3: float | None = None
    heatindex_3: float | None = None
    temperature_4: float | None = None
    humidity_4: float | None = None
    heatindex_4: float | None = None
    temperature_5: float | None = None
    humidity_5: float | None = None
    heatindex_5: float | None = None
    temperature_6: float | None = None
    humidity_6: float | None = None
    heatindex_6: float | None = None
    temperature_7: float | None = None
    humidity_7: float | None = None
    heatindex_7: float | None = None
    temperature_8: float | None = None
    humidity_8: float | None = None
    heatindex_8: float | None = None


@dataclass
class BeaufortDescription:
    """A class that describes beaufort values."""

    value: int
    description: str
