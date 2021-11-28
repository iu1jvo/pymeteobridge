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
    elevation: str | None = None


@dataclass
class ObservationDescription:
    """A class describing realtime weather data."""

    key: str

    utc_time: str | None = None
    air_temperature: float | None = None
    station_pressure: float | None = None
    sea_level_pressure: float | None = None
    relative_humidity: int | None = None
    precip_accum_local_day: float | None = None
    precip_rate: float | None = None
    wind_avg: float | None = None
    wind_direction: int | None = None
    wind_cardinal: str | None = None
    wind_gust: float | None = None
    beaufort: int | None = None
    beaufort_description: str | None = None
    solar_radiation: float | None = None
    uv: float | None = None
    uv_description: str | None = None
    lightning_strike_last_epoch: int | None = None
    lightning_strike_last_distance: int | None = None
    lightning_strike_count: int | None = None
    feels_like: float | None = None
    heat_index: float | None = None
    wind_chill: float | None = None
    dew_point: float | None = None
    feels_like: float | None = None
    visibility: float | None = None
    trend_temperature: float | None = None
    temperature_trend: str | None = None
    trend_pressure: float | None = None
    pressure_trend: str | None = None
    air_pm_10: float | None = None
    air_pm_25: float | None = None
    air_pm_1: float | None = None
    forecast: str | None = None
    indoor_temperature: float | None = None
    indoor_humidity: int | None = None
    air_temperature_dmin: float | None = None
    air_temperature_dmintime: str | None = None
    air_temperature_dmax: float | None = None
    air_temperature_dmaxtime: str | None = None
    air_temperature_mmin: float | None = None
    air_temperature_mmintime: str | None = None
    air_temperature_mmax: float | None = None
    air_temperature_mmaxtime: str | None = None
    air_temperature_ymin: float | None = None
    air_temperature_ymintime: str | None = None
    air_temperature_ymax: float | None = None
    air_temperature_ymaxtime: str | None = None
    is_lowbat: bool | None = None
    is_freezing: bool | None = None
    is_raining: bool | None = None
    temperature_extra_1: float | None = None
    relative_humidity_extra_1: float | None = None
    heat_index_extra_1: float | None = None
    temperature_extra_2: float | None = None
    relative_humidity_extra_2: float | None = None
    heat_index_extra_2: float | None = None
    temperature_extra_3: float | None = None
    relative_humidity_extra_3: float | None = None
    heat_index_extra_3: float | None = None
    temperature_extra_4: float | None = None
    relative_humidity_extra_4: float | None = None
    heat_index_extra_4: float | None = None
    temperature_extra_5: float | None = None
    relative_humidity_extra_5: float | None = None
    heat_index_extra_5: float | None = None
    temperature_extra_6: float | None = None
    relative_humidity_extra_6: float | None = None
    heat_index_extra_6: float | None = None
    temperature_extra_7: float | None = None
    relative_humidity_extra_7: float | None = None
    heat_index_extra_7: float | None = None
    temperature_soil_1: float | None = None
    humidity_soil_1: float | None = None
    temperature_soil_2: float | None = None
    humidity_soil_2: float | None = None
    temperature_soil_3: float | None = None
    humidity_soil_3: float | None = None
    temperature_soil_4: float | None = None
    humidity_soil_4: float | None = None
    temperature_leaf_1: float | None = None
    humidity_leaf_1: float | None = None
    temperature_leaf_2: float | None = None
    humidity_leaf_2: float | None = None
    temperature_leaf_3: float | None = None
    humidity_leaf_3: float | None = None
    temperature_leaf_4: float | None = None
    humidity_leaf_4: float | None = None


@dataclass
class BeaufortDescription:
    """A class that describes beaufort values."""

    value: int
    description: str
