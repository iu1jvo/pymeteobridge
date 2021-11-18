"""System Wide Constants for pymeteobridge"""
from __future__ import annotations

FIELDS_STATION = [
    ["mac", "mbsystem-mac:-", "str"],
    ["swversion", "mbsystem-swversion:-", "float"],
    ["platform", "mbsystem-platform:-", "str"],
    ["station", "mbsystem-station:-", "str"],
    ["timezone", "mbsystem-timezone:-", "str"],
    ["uptime", "mbsystem-uptime:-", "int"],
    ["ip", "mbsystem-ip:-", "str"],
]

UNIT_TYPE_METRIC = "metric"
UNIT_TYPE_IMPERIAL = "imperial"
VALID_UNIT_TYPES = [UNIT_TYPE_IMPERIAL, UNIT_TYPE_METRIC]
