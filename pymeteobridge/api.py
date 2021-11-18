"""Meteobridge Data Wrapper."""
from __future__ import annotations

import aiohttp
from aiohttp import client_exceptions
import ast
import logging
from typing import Optional

from pymeteobridge.data import StationDescription
from pymeteobridge.const import FIELDS_STATION, UNIT_TYPE_METRIC, VALID_UNIT_TYPES
from pymeteobridge.exceptions import  Invalid,  BadRequest, NotAuthorized
from pymeteobridge.helpers import Conversions

_LOGGER = logging.getLogger(__name__)

class MeteobridgeApiClient:
    """Base Class for the Meteobridge API."""

    req: aiohttp.ClientSession

    def __init__ (
        self,
        username: str,
        password: str,
        ip_address: str,
        units: Optional[str] = UNIT_TYPE_METRIC,
        homeassistant: Optional(bool) = True,
        session: Optional[aiohttp.ClientSession] = None,
    ) -> None:
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

        self.base_url = f"http://{self.username}:{self.password}@{self.ip_address}/cgi-bin/template.cgi?template="
        self._station_data: StationDescription = None

    @property
    def station_data(self) -> StationDescription:
        """Returns Station Data."""
        return self._station_data

    async def initialize(self) -> None:
        """Initialize data tables."""

        data_fields = self.build_endpoint(FIELDS_STATION)
        endpoint = f"{self.base_url}{data_fields}"
        data = await self._api_request(endpoint)

        if data is not None:
            station_data = StationDescription(
                key=data["mac"],
                mac=data["mac"],
                swversion=data["swversion"],
                platform=self.cnv.hw_platform(data["platform"]),
                station=data["station"],
                timezone=data["timezone"],
                uptime=data["uptime"],
                ip=data["ip"],
            )
            self._station_data = station_data

    def build_endpoint(self, data_fields) -> str:
        """Builds the Data End Point."""

        parameters = "{"
        for item in data_fields:
            enc = "'" if item[2] == "str" else ""
            parameters += f"'{item[0]}': {enc}[{item[1]}]{enc}, "

        parameters = parameters[0:-2]
        parameters += "}"
        return parameters

    async def _api_request(
        self,
        url: str
        ) -> None:
        """Get data from Meteobridge API."""
        try:
            async with self.req.get(url) as resp:
                resp.raise_for_status()
                data = await resp.read()
                decoded_content = data.decode("utf-8")
                return ast.literal_eval(decoded_content)

        except client_exceptions.ClientError as err:
            raise BadRequest(f"Error requesting data from Meteobridge: {err}") from None
