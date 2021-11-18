"""Dataclasses for pymeteobridge"""
from __future__ import annotations

from dataclasses import dataclass, field

@dataclass
class StationDescription:
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

    temperature: float | None = None
    wind_chill: float | None = None
    air_pm_10: float | None = None
    air_pm_25: float | None = None
    air_pm_1: float | None = None
    heat_index: float | None = None
    humidity: float | None = None
    wind_avg: float | None = None
    wind_gust: float | None = None
