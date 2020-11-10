from StateWeather.utils import RowParser
from StateWeather.spreaddata import SpreadData
import unittest

from StateWeather import spreaddata

class SpreaddataTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.data = SpreadData()
        self.lp = RowParser()

    def test_get_min_spread(self):
        header = {'Dy':0, 'MxT':1, 'MnT':2}
        self.data.key_map = {'Day': 'Dy', 'Max':'MxT', 'Min': 'MnT'}
        raw = '  Dy MxT   MnT   '
        
        line = '   1  88    59    74          53.8       0.00 F       280  9.6 270  17  1.6  93 23 1004.5'
        line_2 = '   2  88    60    74          53.8       0.00 F       280  9.6 270  17  1.6  93 23 1004.5'
        self.data.header = header
        self.data.raw_header = raw
        self.lp.process_line(raw, self.data, self.data.get_min_spread)
        self.lp.process_line(line, self.data, self.data.get_min_spread)
        self.lp.process_line(line_2, self.data, self.data.get_min_spread)
        expected = 28
        self.assertEqual(expected, self.data.min_spread)
        
    def test_get_min_spread_day(self):
        header = {'Dy':0, 'MxT':1, 'MnT':2}
        self.data.key_map = {'Day': 'Dy', 'Max':'MxT', 'Min': 'MnT'}
        raw = '  Dy MxT   MnT   '
        
        line = '   1  88    59    74          53.8       0.00 F       280  9.6 270  17  1.6  93 23 1004.5'
        line_2 = '   2  88    60    74          53.8       0.00 F       280  9.6 270  17  1.6  93 23 1004.5'
        self.data.header = header
        self.data.raw_header = raw
        self.lp.process_line(raw, self.data, self.data.get_min_spread)
        self.lp.process_line(line, self.data, self.data.get_min_spread)
        self.lp.process_line(line_2, self.data, self.data.get_min_spread)
        expected = 2
        self.assertEqual(expected, self.data.min_day)
