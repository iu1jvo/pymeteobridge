"""pymeteobridgedata exception definitions."""


class MeteobridgeError(Exception):
    """Base class for all other WeatherFlow errors."""


class ClientError(MeteobridgeError):
    """Base Class for all other Unifi Protect client errors."""


class BadRequest(ClientError):
    """Invalid request from API Client."""


class Invalid(ClientError):
    """Invalid return from Authorization Request."""


class NotAuthorized(ClientError):
    """Wrong Username or Password."""
