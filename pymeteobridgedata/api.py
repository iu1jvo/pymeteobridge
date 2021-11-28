"""Meteobridge Data Wrapper."""
from __future__ import annotations

import ast
import logging
from typing import List, Optional

from aiohttp import ClientSession, ClientTimeout, client_exceptions

from pymeteobridgedata.const import (
    DEFAULT_TIMEOUT,
    FIELDS_OBSERVATION,
    FIELDS_STATION,
    UNIT_TYPE_METRIC,
    VALID_UNIT_TYPES,
)
from pymeteobridgedata.data import (
    BeaufortDescription,
    DataLoggerDescription,
    ObservationDescription,
)
from pymeteobridgedata.exceptions import BadRequest
from pymeteobridgedata.helpers import Calculations, Conversions

_LOGGER = logging.getLogger(__name__)


class MeteobridgeApiClient:
    """Base Class for the Meteobridge API."""

    req: ClientSession

    def __init__(
        self,
        username: str,
        password: str,
        ip_address: str,
        units: Optional[str] = UNIT_TYPE_METRIC,
        extra_sensors: Optional[int] = 0,
        extra_soil_sensors: Optional[int] = 0,
        extra_leaf_sensors: Optional[int] = 0,
        homeassistant: Optional(bool) = True,
        session: Optional[ClientSession] = None,
    ) -> None:
        """Initialize api class."""
        self.username = username
        self.password = password
        self.ip_address = ip_address
        self.units = units
        self.homeassistant = homeassistant
        self.extra_sensors = extra_sensors
        self.extra_soil_sensors = extra_soil_sensors
        self.extra_leaf_sensors = extra_leaf_sensors

        if self.units not in VALID_UNIT_TYPES:
            self.units = UNIT_TYPE_METRIC

        if session is None:
            session = ClientSession()
        self.req = session

        self.cnv = Conversions(self.units, self.homeassistant)
        self.calc = Calculations()

        self.base_url = (f"http://{self.username}:{self.password}@{self.ip_address}"
                         "/cgi-bin/template.cgi?template=")
        self._device_data: DataLoggerDescription = None
        self._is_metric = self.units is UNIT_TYPE_METRIC

    @property
    def device_data(self) -> DataLoggerDescription:
        """Return Device Data."""
        return self._device_data

    async def initialize(self) -> None:
        """Initialize data tables."""
        data_fields = self._build_endpoint(FIELDS_STATION)
        endpoint = f"{self.base_url}{data_fields}"
        result = await self._async_request("get", endpoint)
        data = await self._process_request_result(result, FIELDS_STATION)

        if data is not None:
            device_data = DataLoggerDescription(
                key=data["mac"],
                mac=data["mac"],
                swversion=data["swversion"],
                platform=self.cnv.hw_platform(data["platform"]),
                station=data["station"],
                timezone=data["timezone"],
                uptime=data["uptime"],
                ip=data["ip"],
                elevation=data["elevation"],
            )
            self._device_data = device_data
        return None

    async def update_observations(self) -> None:
        """Update observation data."""
        if self._device_data is None:
            _LOGGER.error("Logger has not been initialized. "
                          "Run initilaize() function first.")
            return

        data_fields = self._build_endpoint(FIELDS_OBSERVATION)
        endpoint = f"{self.base_url}{data_fields}"
        result = await self._async_request("get", endpoint)
        data = await self._process_request_result(result, FIELDS_OBSERVATION)

        if data is not None:
            visibility = self.calc.visibility(
                self._device_data.elevation,
                data["air_temperature"],
                data["relative_humidity"],
                data["dew_point"]
            )
            feels_like = self.calc.feels_like(
                data["air_temperature"],
                data["relative_humidity"],
                data["wind_gust"],
                data["heat_index"],
                data["wind_chill"]
            )
            beaufort_data: BeaufortDescription = self.calc.beaufort(data["wind_avg"])
            entity_data = ObservationDescription(
                key=self._device_data.key,
                utc_time=self.cnv.utc_from_timestamp(data["utc_time"]),
                air_temperature=self.cnv.temperature(data["air_temperature"]),
                sea_level_pressure=self.cnv.pressure(data["sea_level_pressure"]),
                station_pressure=self.cnv.pressure(data["station_pressure"]),
                relative_humidity=data["relative_humidity"],
                precip_accum_local_day=self.cnv.rain(data["precip_accum_local_day"]),
                precip_rate=self.cnv.rain(data["precip_rate"]),
                wind_avg=self.cnv.windspeed(data["wind_avg"]),
                wind_gust=self.cnv.windspeed(data["wind_gust"]),
                wind_direction=data["wind_direction"],
                wind_cardinal=self.calc.wind_direction(data["wind_direction"]),
                beaufort=beaufort_data.value,
                beaufort_description=beaufort_data.description,
                uv=data["uv"],
                uv_description=self.calc.uv_description(data["uv"]),
                solar_radiation=data["solar_radiation"],
                visibility=self.cnv.distance(visibility),
                lightning_strike_last_epoch=self.cnv.utc_from_timestamp(data["lightning_strike_last_epoch"]),
                lightning_strike_count=data["lightning_strike_count"],
                lightning_strike_last_distance=data["lightning_strike_last_distance"],
                heat_index=self.cnv.temperature(data["heat_index"]),
                wind_chill=self.cnv.temperature(data["wind_chill"]),
                feels_like=self.cnv.temperature(feels_like),
                dew_point=self.cnv.temperature(data["dew_point"]),
                trend_temperature=data["trend_temperature"],
                temperature_trend=self.calc.trend_description(data["trend_temperature"]),
                trend_pressure=data["trend_pressure"],
                pressure_trend=self.calc.trend_description(data["trend_pressure"]),
                air_pm_10=data["air_pm_10"],
                air_pm_25=data["air_pm_25"],
                air_pm_1=data["air_pm_1"],
                forecast=data["forecast"],
                indoor_temperature=self.cnv.temperature(data["indoor_temperature"]),
                indoor_humidity=data["indoor_humidity"],
                air_temperature_dmin=self.cnv.temperature(data["air_temperature_dmin"]),
                air_temperature_dmintime=self.cnv.utc_from_mbtime(data["air_temperature_dmintime"]),
                air_temperature_dmax=self.cnv.temperature(data["air_temperature_dmax"]),
                air_temperature_dmaxtime=self.cnv.utc_from_mbtime(data["air_temperature_dmaxtime"]),
                air_temperature_mmin=self.cnv.temperature(data["air_temperature_mmin"]),
                air_temperature_mmintime=self.cnv.utc_from_mbtime(data["air_temperature_mmintime"]),
                air_temperature_mmax=self.cnv.temperature(data["air_temperature_mmax"]),
                air_temperature_mmaxtime=self.cnv.utc_from_mbtime(data["air_temperature_mmaxtime"]),
                air_temperature_ymin=self.cnv.temperature(data["air_temperature_ymin"]),
                air_temperature_ymintime=self.cnv.utc_from_mbtime(data["air_temperature_ymintime"]),
                air_temperature_ymax=self.cnv.temperature(data["air_temperature_ymax"]),
                air_temperature_ymaxtime=self.cnv.utc_from_mbtime(data["air_temperature_ymaxtime"]),
                is_freezing=self.calc.is_freezing(data["air_temperature"]),
                is_raining=self.calc.is_raining(data["precip_rate"]),
                is_lowbat=True if data["is_lowbat"] == 1 else False,
            )

            if self.extra_sensors > 0 or self.extra_soil_sensors or self.extra_leaf_sensors > 0:
                extra_sensors = await self._get_extra_sensor_values()
                sensor_num = 1
                while sensor_num < self.extra_sensors + 1:
                    temp_field = f"temperature_extra_{sensor_num}"
                    setattr(entity_data, temp_field, self.cnv.temperature(extra_sensors[temp_field]))
                    hum_field = f"relative_humidity_extra_{sensor_num}"
                    setattr(entity_data, hum_field, extra_sensors[hum_field])
                    heat_field = f"heat_index_extra_{sensor_num}"
                    setattr(entity_data, heat_field, self.cnv.temperature(extra_sensors[heat_field]))
                    sensor_num += 1
                sensor_num = 1
                while sensor_num < self.extra_soil_sensors + 1:
                    temp_field = f"temperature_soil_{sensor_num}"
                    setattr(entity_data, temp_field, self.cnv.temperature(extra_sensors[temp_field]))
                    hum_field = f"humidity_soil_{sensor_num}"
                    setattr(entity_data, hum_field, extra_sensors[hum_field])
                    sensor_num += 1
                sensor_num = 1
                while sensor_num < self.extra_leaf_sensors + 1:
                    temp_field = f"temperature_leaf_{sensor_num}"
                    setattr(entity_data, temp_field, self.cnv.temperature(extra_sensors[temp_field]))
                    hum_field = f"humidity_leaf_{sensor_num}"
                    setattr(entity_data, hum_field, extra_sensors[hum_field])
                    sensor_num += 1

            return entity_data

        return None

    async def load_unit_system(self) -> None:
        """Return unit of meassurement based on unit system."""
        density_unit = "kg/m^3" if self._is_metric else "lb/ft^3"
        distance_unit = "km" if self._is_metric else "mi"
        length_unit = "m/s" if self._is_metric else "mi/h"
        length_km_unit = "km/h" if self._is_metric else "mi/h"
        pressure_unit = "hPa" if self._is_metric else "inHg"
        precip_unit = "mm" if self._is_metric else "in"

        units_list = {
            "none": None,
            "density": density_unit,
            "distance": distance_unit,
            "length": length_unit,
            "length_km": length_km_unit,
            "pressure": pressure_unit,
            "precipitation": precip_unit,
            "precipitation_rate": f"{precip_unit}/h",
        }

        return units_list

    async def speed_test(self) -> None:
        """Perform Speed Test."""
        _LOGGER.debug("FIELD COUNT: %s", len(FIELDS_OBSERVATION))
        data_fields = self._build_endpoint(FIELDS_OBSERVATION)
        endpoint = f"{self.base_url}{data_fields}"
        data = await self._async_request("get", endpoint)
        result = await self._process_request_result(data, FIELDS_OBSERVATION)

        return result

    async def _get_extra_sensor_values(self) -> None:
        """Return extra sensors if attached."""
        if self.extra_sensors == 0:
            return None

        sensor_array = []
        count = 0
        while count < self.extra_sensors:
            count += 1
            item_array = []
            item_array.append(f"temperature_extra_{count}")
            item_array.append(f"th{count}temp-act:None")
            item_array.append("float")
            sensor_array.append(item_array)
            item_array = []
            item_array.append(f"relative_humidity_extra_{count}")
            item_array.append(f"th{count}hum-act.0:None")
            item_array.append("int")
            sensor_array.append(item_array)
            item_array = []
            item_array.append(f"heat_index_extra_{count}")
            item_array.append(f"th{count}heatindex-act.1:None")
            item_array.append("float")
            sensor_array.append(item_array)

        # Soil Sensors
        count = 0
        while count < self.extra_soil_sensors:
            count += 1
            item_array = []
            item_array.append(f"temperature_soil_{count}")
            item_array.append(f"soil{count}temp-act:None")
            item_array.append("float")
            sensor_array.append(item_array)
            item_array = []
            item_array.append(f"humidity_soil_{count}")
            item_array.append(f"soil{count}hum-act.0:None")
            item_array.append("int")
            sensor_array.append(item_array)

        # Leaf Sensors
        count = 0
        while count < self.extra_leaf_sensors:
            count += 1
            item_array = []
            item_array.append(f"temperature_leaf_{count}")
            item_array.append(f"leaf{count}temp-act:None")
            item_array.append("float")
            sensor_array.append(item_array)
            item_array = []
            item_array.append(f"humidity_leaf_{count}")
            item_array.append(f"leaf{count}hum-act.0:None")
            item_array.append("int")
            sensor_array.append(item_array)

        data_fields = self._build_endpoint(sensor_array)
        endpoint = f"{self.base_url}{data_fields}"
        result = await self._async_request("get", endpoint)
        data = await self._process_request_result(result, sensor_array)
        return data

    def _build_endpoint(self, data_fields) -> str:
        """Build Data End Point."""
        parameters = ""
        for item in data_fields:
            parameters += f"[{item[1]}];"

        parameters = parameters[0:-1]
        parameters += "&contenttype=text/plain;charset=iso-8859-1"

        return parameters

    async def _process_request_result(self, result: str, data_fields) -> List:
        """Process result from Request."""
        if result is None:
            return None

        items = result.split(";")
        data = "{"
        index = 0
        for data_field in data_fields:
            enc = "'" if data_field[2] == "str" else ""
            data += f"'{data_field[0]}': {enc}{items[index]}{enc}, "
            index += 1
        data = data[0:-2]
        data += "}"

        return ast.literal_eval(data)

    async def _async_request(
        self,
        method: str,
        endpoint: str,
    ) -> dict:
        """Make a request against the SmartWeather API."""
        use_running_session = self.req and not self.req.closed

        if use_running_session:
            session = self.req
        else:
            session = ClientSession(timeout=ClientTimeout(total=DEFAULT_TIMEOUT))

        try:
            async with session.request(method, endpoint) as resp:
                resp.raise_for_status()
                data = await resp.read()
                decoded_content = data.decode("utf-8")
                return decoded_content

        except client_exceptions.ClientError as err:
            raise BadRequest(f"Error requesting data from Meteobridge: {err}") from None

        finally:
            if not use_running_session:
                await session.close()
