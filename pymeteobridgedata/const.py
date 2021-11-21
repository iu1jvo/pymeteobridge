"""System Wide Constants for pymeteobridgedata."""
from __future__ import annotations

FIELDS_OBSERVATION = [
    ["utc_time", "epoch", "int"],
    ["air_temperature", "th0temp-act:None", "float"],
    ["sea_level_pressure", "thb0seapress-act:None", "float"],
    ["station_pressure", "thb0press-act:None", "float"],
    ["relative_humidity", "th0hum-act:None", "int"],
    ["precip_rate", "rain0rate-act:None", "float"],
    ["precip_accum_local_day", "rain0total-daysum:None", "float"],
    ["wind_avg", "wind0avgwind-act:None", "float"],
    ["wind_gust", "wind0wind-max1:None", "float"],
    ["wind_direction", "wind0dir-avg5.0:None", "int"],
    ["uv", "uv0index-act:None", "float"],
    ["solar_radiation", "sol0rad-act:None", "float"],
    ["lightning_strike_last_epoch", "lgt0total-lasttime=epoch:None", "float"],
    ["lightning_strike_count", "lgt0total-act.0:None", "float"],
    ["lightning_strike_last_distance", "lgt0dist-act.0:None", "float"],
    ["heat_index", "th0heatindex-act:None", "float"],
    ["dew_point", "th0dew-act:None", "float"],
    ["wind_chill", "wind0chill-act:None", "float"],
    ["trend_temperature", "th0temp-delta10:None", "float"],
    ["trend_pressure", "thb0seapress-delta10:None", "float"],
    ["air_pm_10", "air0pm-act:None", "float"],
    ["air_pm_25", "air1pm-act:None", "float"],
    ["air_pm_1", "air2pm-act:None", "float"],
    ["is_lowbat", "th0lowbat-act.0:None", "int"],
    ["forecast", "forecast-text:None", "str"],
]

FIELDS_STATION = [
    ["mac", "mbsystem-mac:--", "str"],
    ["swversion", "mbsystem-swversion:--", "float"],
    ["platform", "mbsystem-platform:--", "str"],
    ["station", "mbsystem-station:--", "str"],
    ["timezone", "mbsystem-timezone:--", "str"],
    ["uptime", "mbsystem-uptime:--", "int"],
    ["ip", "mbsystem-ip:--", "str"],
    ["elevation", "mbsystem-altitude:--", "int"],
]

UNIT_TYPE_METRIC = "metric"
UNIT_TYPE_IMPERIAL = "imperial"
VALID_UNIT_TYPES = [UNIT_TYPE_IMPERIAL, UNIT_TYPE_METRIC]
