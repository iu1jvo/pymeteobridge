"""System Wide Constants for pymeteobridgedata."""
from __future__ import annotations

DEFAULT_TIMEOUT = 10

FIELDS_OBSERVATION = [
    ["utc_time", "epoch", "int"],
    ["air_temperature", "th0temp-act:None", "float"],
    ["sea_level_pressure", "thb0seapress-act:None", "float"],
    ["station_pressure", "thb0press-act:None", "float"],
    ["relative_humidity", "th0hum-act.0:None", "int"],
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
    ["indoor_temperature", "thb0temp-act:None", "float"],
    ["indoor_humidity", "thb0hum-act.0:None", "int"],
    ["air_temperature_dmin", "th0temp-dmin:None", "float"],
    ["air_temperature_dmintime", "th0temp-dmintime=utc:None", "str"],
    ["air_temperature_dmax", "th0temp-dmax:None", "float"],
    ["air_temperature_dmaxtime", "th0temp-dmaxtime=utc:None", "str"],
    ["air_temperature_mmin", "th0temp-mmin:None", "float"],
    ["air_temperature_mmintime", "th0temp-mmintime=utc:None", "str"],
    ["air_temperature_mmax", "th0temp-mmax:None", "float"],
    ["air_temperature_mmaxtime", "th0temp-mmaxtime=utc:None", "str"],
    ["air_temperature_ymin", "th0temp-ymin:None", "float"],
    ["air_temperature_ymintime", "th0temp-ymintime=utc:None", "str"],
    ["air_temperature_ymax", "th0temp-ymax:None", "float"],
    ["air_temperature_ymaxtime", "th0temp-ymaxtime=utc:None", "str"],
    ["temperature_soil_1", "soil0temp-act:None", "float"],
    ["humidity_soil_1", "soil0hum-act.0:None", "int"],
    ["temperature_soil_2", "soil1temp-act:None", "float"],
    ["humidity_soil_2", "soil1hum-act.0:None", "int"],
    ["temperature_soil_3", "soil2temp-act:None", "float"],
    ["humidity_soil_3", "soil2hum-act.0:None", "int"],
    ["temperature_soil_4", "soil3temp-act:None", "float"],
    ["humidity_soil_4", "soil3hum-act.0:None", "int"],
    ["temperature_leaf_1", "leaf0temp-act:None", "float"],
    ["humidity_leaf_1", "leaf0hum-act.0:None", "int"],
    ["temperature_leaf_2", "leaf1temp-act:None", "float"],
    ["humidity_leaf_2", "leaf1hum-act.0:None", "int"],
    ["temperature_leaf_3", "leaf2temp-act:None", "float"],
    ["humidity_leaf_3", "leaf2hum-act.0:None", "int"],
    ["temperature_leaf_4", "leaf3temp-act:None", "float"],
    ["humidity_leaf_4", "leaf3hum-act.0:None", "int"],
]

FIELDS_STATION = [
    ["mac", "mbsystem-mac:None", "str"],
    ["swversion", "mbsystem-swversion:None", "float"],
    ["platform", "mbsystem-platform:None", "str"],
    ["station", "mbsystem-station:None", "str"],
    ["timezone", "mbsystem-timezone:None", "str"],
    ["uptime", "mbsystem-uptime:0", "int"],
    ["ip", "mbsystem-ip:--", "str"],
    ["elevation", "mbsystem-altitude.0:0", "int"],
]

UNIT_TYPE_METRIC = "metric"
UNIT_TYPE_IMPERIAL = "imperial"
VALID_UNIT_TYPES = [UNIT_TYPE_IMPERIAL, UNIT_TYPE_METRIC]
