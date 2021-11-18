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
    