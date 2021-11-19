# Python Wrapper for Meteobridge Datalogger

![Latest PyPI version](https://img.shields.io/pypi/v/pymeteobridge) ![Supported Python](https://img.shields.io/pypi/pyversions/pymeteobridge)

This module communicates with a [Meteobridge Datalogger](https://www.meteobridge.com/wiki/index.php/Home) using a [their Template Script](https://www.meteobridge.com/wiki/index.php/Add-On_Services).

The module is primarily written for the purpose of being used in Home Assistant for the Custom Integration called `meteobridge` but might be used for other purposes also.

When this is done, it will replace the previous module [`pymeteobridgeio`](https://github.com/briis/pymeteobridgeio)

## Install

`pymeteobridge` is avaible on PyPi:

```bash
pip install pymeteobridge
```

## Usage

This library is primarily designed to be used in an async context.

The main interface for the library is the `pymeteobridge.MeteobridgeApiClient`. This interface takes 4 options:

* `username`: (required) The username to login to your Meteobridge device. Default this *meteobridge*.
* `password`: (required) The password for your meteobridge device.
* `ip_address`: (required) IP Address of the Meteobridge device.
* `units`: (optional) Valid options here are *metric* or *imperial*. Metebridge devices always deliver data in metric units, so conversion will only take place if if metric is not selected. Default value is **metric**
* `homeassistant`: (optional) Valid options are *True* or *False*. If set to True, there will be some unit types that will not be converted, as Home Assistant will take care of that. Default value is **True**

### Example Python script

```python
import asyncio
import logging
import time

from pymeteobridge import MeteobridgeApiClient, Invalid, NotAuthorized, BadRequest
from pymeteobridge.data import DataLoggerDescription, ObservationDescription

_LOGGER = logging.getLogger(__name__)

async def main() -> None:
    logging.basicConfig(level=logging.DEBUG)
    start = time.time()

    meteobridge = MeteobridgeApiClient(USERNAME, PASSWORD, IP_ADDRESS, homeassistant=False, units="imperial")
    try:
        await meteobridge.initialize()

    except Invalid as err:
        _LOGGER.debug(err)
    except NotAuthorized as err:
        _LOGGER.debug(err)
    except BadRequest as err:
        _LOGGER.debug(err)

    data: DataLoggerDescription = meteobridge.device_data
    if data is not None:
        for field in data.__dataclass_fields__:
            value = getattr(data, field)
            print(field,"-", value)

    data: ObservationDescription = await meteobridge.update_observations()
    if data is not None:
        for field in data.__dataclass_fields__:
            value = getattr(data, field)
            print(field,"-", value)


    end = time.time()

    await meteobridge.req.close()

    _LOGGER.info("Execution time: %s seconds", end - start)

asyncio.run(main())
```
