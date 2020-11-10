import unittest
from StateWeather.utils import RowParser
from StateWeather.constants import CONSTS as c


class LineParserTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.lp = RowParser()
        self.test_line = '   1  88    59    74          53.8       0.00 F       280  9.6 270  17  1.6  93 23 1004.5'
        self.test_line_float = '   1  88.8    59    74          53.8       0.00 F       280  9.6 270  17  1.6  93 23 1004.5'
        self.header_line = '  Dy MxT   MnT   AvT   HDDay  AvDP 1HrP TPcpn WxType PDir AvSp Dir MxS SkyC MxR MnR AvSLP'

    def test_line_type_header(self):
        expeted = c.LINETYPES["HEADER"]
        actual = self.lp.get_line_type(self.header_line)
        self.assertEqual(actual, expeted)
    
    def test_line_type_None(self):
        line = ''       
        actual = self.lp.get_line_type(line)
        self.assertIsNone(actual)

    def test_line_type_None_None(self):
        line = 'XXXXXXXXXXXXXXXXXXXXXXXx'       
        actual = self.lp.get_line_type(line)
        self.assertIsNone(actual)
    def test_get_line_items_None(self):
        line = ' mo  82.9  60.5  71.7    16  58.8       0.00              6.9          5.3'       
        actual = self.lp.get_line_items(line, c.LINETYPES['AGG'])
        self.assertIsNone(actual)

    def test_line_type_data(self):

        expected = c.LINETYPES["DATA"]
        actual = self.lp.get_line_type(self.test_line)
        self.assertEqual(expected, actual)

    def test_line_type_agg(self):
        line ='mo  82.9  60.5  71.7    16  58.8       0.00              6.9          5.3'
        expected = c.LINETYPES["AGG"]
        actual = self.lp.get_line_type(line)
        self.assertEqual(expected, actual)

    def test_line_get_line_as_header(self):
        header = '  Dy MxT   MnT   AvT   HDDay  AvDP 1HrP TPcpn WxType PDir AvSp Dir MxS SkyC MxR MnR AvSLP'
        actual = self.lp.get_line_items(line_type=c.LINETYPES["HEADER"], line=header)
        expected = 0
        self.assertEqual(actual['Dy'], expected)

    def test_process_header_with_None(self):
        actual = self.lp.process_header(None)
        self.assertIsNone(actual)

    def test_process_header_with_One(self):
        expected = {'One': 0}
        actual = self.lp.process_header('One')
        self.assertEqual(expected, actual)

    def test_get_line_items_with_One(self):
        expected = {'One': 0}
        actual = self.lp.get_line_items(line_type=c.LINETYPES["HEADER"], line='One')
        self.assertEqual(expected, actual)   

    def test_get_line_item_as_data(self):
        header = {'Dy':0, 'MxT':1, 'MnT':2}
        expected = {'Dy':1, 'MxT':88, 'MnT':59}
        actual = self.lp.get_line_items(line_type=c.LINETYPES["DATA"], line=self.test_line, header=header)
        
        self.assertEqual(expected['MxT'], actual['MxT'])

    def test_get_line_item_as_data_with_floats(self):
        header = {'Dy':0, 'MxT':1, 'MnT':2}
        expected = {'Dy':1, 'MxT':88.8, 'MnT':59}
        actual = self.lp.get_line_items(line_type=c.LINETYPES["DATA"], line=self.test_line_float, header=header)
        
        self.assertEqual(expected['MxT'], actual['MxT'])

    def test_get_line_item_as_data_no_header(self):
        actual = self.lp.get_line_items(line_type=c.LINETYPES["DATA"], line=self.test_line)
        self.assertIsNone(actual)

    def test_parse_line(self):
        #         12345678901234
        header = '  Dy MxT   MnT'
        data =     '   1  88      '
        expected = '   1  88    x '
        #header = '  Dy MxT   MnT   AvT   HDDay  AvDP 1HrP TPcpn WxType PDir AvSp Dir MxS SkyC MxR MnR AvSLP'
        #data =   '   1  88    59    74          53.8       0.00 F       280  9.6 270  17  1.6  93 23 1004.5'
        actual = self.lp.insert_missing_values(header, data)
        self.assertEqual(expected, actual)
    

    def test_clean_value_str(self):
        actual = self.lp.clean_value('ABC')
        self.assertIsInstance(actual, str)

    def test_clean_value_int(self):
        actual = self.lp.clean_value('123')
        self.assertIsInstance(actual, int)
    
    def test_clean_value_float(self):
        actual = self.lp.clean_value('1.23')
        self.assertIsInstance(actual, float)

    def test_clean_value_nan(self):
        actual = self.lp.clean_value(' 1*')
        self.assertEqual(c.NAN, actual)

    def test_find_next_start_bad_position(self):
        actual = self.lp.find_next_start("XXXXXXX", 7)
        self.assertIsNone(actual)
    
    def test_find_next_start_end(self):
        actual = self.lp.find_next_start("XXXXXXX", 0)
        expected = 6
        self.assertEqual(expected, actual)
    
    def test_find_next_start_bad_nonalpha(self):
        actual = self.lp.find_next_start("* * XX XX", 0)
        expected = 6
        self.assertEqual(expected, actual)




            





             


