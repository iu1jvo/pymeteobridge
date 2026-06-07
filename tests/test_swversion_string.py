import unittest

from pymeteobridgedata.data import DataLoggerDescription
from .const import RAW_DATA

class TestSwversionString(unittest.TestCase):
    def test_swversion_is_string(self):
        raw_data = RAW_DATA

        device = DataLoggerDescription(
            key=raw_data['mac'],
            mac=raw_data['mac'],
            swversion=raw_data['swversion'],
            platform=raw_data['platform'],
            station=raw_data['station'],
            timezone=raw_data['timezone'],
            uptime=int(raw_data['uptime']),
            ip=raw_data['ip'],
            elevation=raw_data['elevation'],
        )

        self.assertIsInstance(device.swversion, str)
        self.assertEqual(device.swversion, raw_data['swversion'])


if __name__ == '__main__':
    unittest.main()
