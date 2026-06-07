"""Python wrapper for Meteobridge Data Logger."""

from pymeteobridgedata.exceptions import BadRequest, Invalid, NotAuthorized
from pymeteobridgedata.data import ObservationDescription, DataLoggerDescription

__all__ = [
    "Invalid",
    "NotAuthorized",
    "BadRequest",
    "MeteobridgeApiClient",
    "ObservationDescription",
    "DataLoggerDescription",
]


def __getattr__(name: str):
    if name == "MeteobridgeApiClient":
        from pymeteobridgedata.api import MeteobridgeApiClient

        return MeteobridgeApiClient
    raise AttributeError(f"module {__name__} has no attribute {name}")
