"""System Wide Constants for pymeteobridge"""
from __future__ import annotations

FIELDS_OBSERVATION = [
    ["temperature", "th0temp-act:0", "float"],
    ["wind_chill", "wind0chill-act:0", "float"],
    ["air_pm_10", "air0pm-act:0", "float"],
    ["air_pm_25", "air1pm-act:0", "float"],
    ["air_pm_1", "air2pm-act:0", "float"],
    ["heat_index", "th0heatindex-act:0", "float"],
    ["humidity", "th0hum-act:0", "float"],
    ["wind_avg", "wind0avgwind-act:0", "float"],
    ["wind_gust", "wind0wind-act:0", "float"],
]

FIELDS_STATION = [
    ["mac", "mbsystem-mac:--", "str"],
    ["swversion", "mbsystem-swversion:--", "float"],
    ["platform", "mbsystem-platform:--", "str"],
    ["station", "mbsystem-station:--", "str"],
    ["timezone", "mbsystem-timezone:--", "str"],
    ["uptime", "mbsystem-uptime:--", "int"],
    ["ip", "mbsystem-ip:--", "str"],
]

UNIT_TYPE_METRIC = "metric"
UNIT_TYPE_IMPERIAL = "imperial"
VALID_UNIT_TYPES = [UNIT_TYPE_IMPERIAL, UNIT_TYPE_METRIC]
