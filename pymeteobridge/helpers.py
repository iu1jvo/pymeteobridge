"""Helper Class for Meteobridge module."""
from __future__ import annotations

import logging

from pymeteobridge.const import UNIT_TYPE_METRIC

_LOGGER = logging.getLogger(__name__)

class Conversions:
    """Converts values."""
    def __init__(self, units: str, homeassistant: bool) -> None:
        self.units = units
        self.homeassistant = homeassistant

    def hw_platform(self, platform: str) -> str:
        """Return the meteobridge HW Platform."""

        if platform is None:
            return None

        if platform == "CARAMBOLA2":
            return "Meteobridge Pro"

        if platform == "VOCORE2":
            return "Meteobridge Nano"

        return platform

        
