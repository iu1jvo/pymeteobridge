"""Meteobridge Data Wrapper."""
from __future__ import annotations

import ast
import logging
from typing import Optional

import aiohttp
from aiohttp import client_exceptions

from pymeteobridgedata.const import (
    FIELDS_OBSERVATION,
    FIELDS_STATION,
    UNIT_TYPE_METRIC,
    VALID_UNIT_TYPES,
)
from pymeteobridgedata.data import (
    BeaufortDescription,
    ObservationDescription,
    DataLoggerDescription,
)
from pymeteobridgedata.exceptions import BadRequest
from pymeteobridgedata.helpers import Calculations, Conversions

_LOGGER = logging.getLogger(__name__)


class MeteobridgeApiClient:
    """Base Class for the Meteobridge API."""

    req: aiohttp.ClientSession

    def __init__(
        self,
        username: str,
        password: str,
        ip_address: str,
        units: Optional[str] = UNIT_TYPE_METRIC,
        homeassistant: Optional(bool) = True,
        session: Optional[aiohttp.ClientSession] = None,
    ) -> None:
        """Initialize api class."""
        self.username = username
        self.password = password
        self.ip_address = ip_address
        self.units = units
        self.homeassistant = homeassistant

        if self.units not in VALID_UNIT_TYPES:
            self.units = UNIT_TYPE_METRIC

        if session is None:
            session = aiohttp.ClientSession()
        self.req = session
        self.cnv = Conversions(self.units, self.homeassistant)
        self.calc = Calculations()

        self.base_url = f"http://{self.username}:{self.password}@{self.ip_address}/cgi-bin/template.cgi?template="
        self._device_data: DataLoggerDescription = None

    @property
    def device_data(self) -> DataLoggerDescription:
        """Return Device Data."""
        return self._device_data

    async def initialize(self) -> None:
        """Initialize data tables."""
        data_fields = self.build_endpoint(FIELDS_STATION)
        endpoint = f"{self.base_url}{data_fields}"
        data = await self._api_request(endpoint)

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
            )
            self._device_data = device_data
        return None

    async def update_observations(self) -> None:
        """Update observation data."""
        if self._device_data is None:
            _LOGGER.error("Logger has not been initialized. Run initilaize() function first.")
            return

        data_fields = self.build_endpoint(FIELDS_OBSERVATION)
        endpoint = f"{self.base_url}{data_fields}"
        data = await self._api_request(endpoint)

        if data is not None:
            beaufort: BeaufortDescription = self.calc.beaufort(data["windspeedavg"])
            entity_data = ObservationDescription(
                key=self._device_data.key,
                timestamp=self.cnv.utc_from_timestamp(data["timestamp"]),
                temperature=self.cnv.temperature(data["temperature"]),
                is_freezing=self.calc.is_freezing(data["temperature"]),
                pressure=self.cnv.pressure(data["pressure"]),
                air_pollution=data["air_pm_10"],
                air_pm_25=data["air_pm_25"],
                air_pm_1=data["air_pm_1"],
                heatindex=self.cnv.temperature(data["heatindex"]),
                humidity=data["humidity"],
                windspeedavg=self.cnv.windspeed(data["windspeedavg"]),
                windgust=self.cnv.windspeed(data["windgust"]),
                windchill=self.cnv.temperature(data["windchill"]),
                windbearing=data["windbearing"],
                wind_cardinal=self.calc.wind_direction(data["windbearing"]),
                raintoday=self.cnv.rain(data["raintoday"]),
                rainrate=self.cnv.rain(data["rainrate"]),
                is_raining=self.calc.is_raining(data["rainrate"]),
                dewpoint=self.cnv.temperature(data["dewpoint"]),
                is_lowbat=True if data["is_lowbat"] == 1 else False,
                in_temperature=self.cnv.temperature(data["in_temperature"]),
                in_humidity=data["in_humidity"],
                temphigh=self.cnv.temperature(data["temphigh"]),
                templow=self.cnv.temperature(data["templow"]),
                uvindex=data["uvindex"],
                solarrad=data["solarrad"],
                temp_month_min=self.cnv.temperature(data["temp_month_min"]),
                temp_month_max=self.cnv.temperature(data["temp_month_max"]),
                temp_year_min=self.cnv.temperature(data["temp_year_min"]),
                wind_month_max=self.cnv.windspeed(data["wind_month_max"]),
                wind_year_max=self.cnv.windspeed(data["wind_year_max"]),
                rain_month_max=self.cnv.rain(data["rain_month_max"]),
                rain_year_max=self.cnv.rain(data["rain_year_max"]),
                rainrate_month_max=self.cnv.rain(data["rainrate_month_max"]),
                rainrate_year_max=self.cnv.rain(data["rainrate_year_max"]),
                lightning_count=data["lightning_count"],
                lightning_energy=data["lightning_energy"],
                lightning_distance=data["lightning_distance"],
                bft_value=beaufort.value,
                beaufort_description=beaufort.description,
                trend_temperature=data["trend_temperature"],
                temperature_trend=self.calc.trend_description(data["trend_temperature"]),
                trend_pressure=data["trend_pressure"],
                pressure_trend=self.calc.trend_description(data["trend_pressure"]),
                absolute_pressure=self.cnv.pressure(data["absolute_pressure"]),
                forecast=data["forecast"],
                temperature_2=self.cnv.temperature(data["temperature_2"]),
                humidity_2=data["humidity_2"],
                heatindex_2=self.cnv.temperature(data["heatindex_2"]),
                temperature_3=self.cnv.temperature(data["temperature_3"]),
                humidity_3=data["humidity_3"],
                heatindex_3=self.cnv.temperature(data["heatindex_3"]),
                temperature_4=self.cnv.temperature(data["temperature_4"]),
                humidity_4=data["humidity_4"],
                heatindex_4=self.cnv.temperature(data["heatindex_4"]),
                temperature_5=self.cnv.temperature(data["temperature_5"]),
                humidity_5=data["humidity_5"],
                heatindex_5=self.cnv.temperature(data["heatindex_5"]),
                temperature_6=self.cnv.temperature(data["temperature_6"]),
                humidity_6=data["humidity_6"],
                heatindex_6=self.cnv.temperature(data["heatindex_6"]),
                temperature_7=self.cnv.temperature(data["temperature_7"]),
                humidity_7=data["humidity_7"],
                heatindex_7=self.cnv.temperature(data["heatindex_7"]),
                temperature_8=self.cnv.temperature(data["temperature_8"]),
                humidity_8=data["humidity_8"],
                heatindex_8=self.cnv.temperature(data["heatindex_8"]),
            )

            return entity_data
        return None

    def build_endpoint(self, data_fields) -> str:
        """Build Data End Point."""
        parameters = "{"
        for item in data_fields:
            enc = "'" if item[2] == "str" else ""
            parameters += f"'{item[0]}':+{enc}[{item[1]}]{enc},+"

        parameters = parameters[0:-2]
        parameters += "}+&contenttype=text/plain;charset=iso-8859-1"

        return parameters

    async def _api_request(self, url: str) -> None:
        """Get data from Meteobridge API."""
        try:
            async with self.req.get(url) as resp:
                resp.raise_for_status()
                data = await resp.read()
                decoded_content = data.decode("utf-8")

                return ast.literal_eval(decoded_content)

        except client_exceptions.ClientError as err:
            raise BadRequest(f"Error requesting data from Meteobridge: {err}") from None
