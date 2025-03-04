import unittest
import json
from unittest.mock import patch, mock_open
#from jinja2 import Template, Environment
from datetime import datetime,timedelta
#from game_engine.data.messages import render_message
# from src.game_engine.data.messages import render_message, login_message
from pdb import set_trace
from icecream import ic
from col.common.split_by import split_by

from col.common.frr_copy_parser import parse_lines
# import pytest
# import sys  # For modifying sys.path temporarily if necessary
# import src.game_engine.data.messages as msg
# from src.common.Utils import (safe_run, get_utc_epoch_time)
# from src.common import Msg_types as types
# from src.common import Communication as com
#
from col.common.monadic import Maybe
from col.common.frr_copy_parser import ( parse_effort,
                                         parse_egap, convert_str_array_to_int)
from col.common.utils import split_on_fn

def convert_to_val(val: str) -> int:
    if val is not None and len(val) > 0:
        return int(val)
    return 0

class TestFrrParser(unittest.TestCase):

    def test_split_on(self):
        delim = ","
        splitter = split_on_fn(delim)

        # Test valid input
        input_str = "a,b,c"
        result = splitter(line=input_str)
        self.assertTrue(result.is_ok)
        self.assertEqual(result.val, ['a', 'b', 'c'])

        # Test empty string
        result = splitter(line="")
        self.assertFalse(result.is_ok)

        # # Test string without delimiter
        result = splitter(line="abc")
        self.assertFalse(result.is_ok)

        # Test multiple delimiters
        result = splitter(line="a,b,,c")
        self.assertTrue(result.is_ok)
        self.assertEqual(result.val, ['a', 'b', '', 'c'])

        # Test with spaces
        result = splitter(line=" a , b , c ")
        self.assertTrue(result.is_ok)
        self.assertEqual(result.val, [' a ', ' b ', ' c '])

        # Test with monadic
        def convert_array(sec_arr):
            ic(sec_arr)
            return [convert_to_val(sec_arr[0]), convert_to_val(sec_arr[1])]

        # Using the monadics
        arr = splitter(line="345,12").map(convert_array)
        self.assertTrue(arr.is_ok)

        self.assertEqual(arr.val[0], 345)
        self.assertEqual(arr.val[1], 12)

        #using failed monad
        arr = splitter(line="345")
        self.assertFalse(arr.is_ok)


    def test_convert_array_int(self):
        # Test successful conversions
        self.assertEqual(convert_str_array_to_int(['10', '0', '20']).val, [10, 0, 20])
        self.assertEqual(convert_str_array_to_int(['0']).val, [0])
        self.assertEqual(convert_str_array_to_int(['1', '2', '3']).val, [1, 2, 3])

        # Test empty strings (should convert to 0)
        self.assertEqual(convert_str_array_to_int(['', '5', '']).val, [0, 5, 0])

        # Test None values (should convert to 0)
        self.assertEqual(convert_str_array_to_int([None, '1', None]).val, [0, 1, 0])

        # Test empty array
        result = convert_str_array_to_int([])
        self.assertFalse(result.is_ok)
        self.assertTrue("Failed to convert empty array" in result.val)

        # Test array with non-numeric strings
        result = convert_str_array_to_int(['abc', '123', 'xyz'])
        self.assertEqual(result.val, [0, 123, 0])

        # Test array with mixed valid and invalid content
        self.assertEqual(convert_str_array_to_int(['10', 'abc', '20', '']).val, [10, 0, 20, 0])

        # Test array with whitespace
        self.assertEqual(convert_str_array_to_int([' 42 ', '  1', '2  ']).val, [42, 1, 2])

        # Test with None input
        result = convert_str_array_to_int(None)
        self.assertFalse(result.is_ok)
        self.assertTrue("Failed to convert empty array" in result.val)

    def test_parse_effort(self ):

        string = "1 hrs, 1 m 13.338 s 223w @3.60WKG"
        vals = parse_effort(string)
        self.assertEqual(vals, (223, 3.6, timedelta(seconds=3673, microseconds=338000)))


        vals = parse_effort("1 hrs, 4 m 217w @3.20WKG")
        self.assertEqual(vals,(217,3.2, timedelta(seconds=1*3600+4*60)))

        string = "1 hrs, 13.338 s 223w @3.60WKG"
        self.assertEqual(parse_effort("1 hrs, 4 m 217w @3.20WKG"),(217, 3.2, timedelta(seconds=3840)) )

        self.assertEqual(parse_effort("1 hrs, .338 s 223w @3.60WKG"),
                         (223, 3.6, timedelta(seconds=3600, microseconds=338000)))


        ic(vals)

    def test_parse_egap(self):
        test_cases = [
            ('1 m 3.115 s', timedelta(seconds=63, microseconds=115000)),
            ('32.646 s', timedelta(seconds=32, microseconds=646000)),
            ('1 m', timedelta(minutes=1)),
            ('Winner', timedelta(minutes=0)),
            # Additional test cases
            ('2 hrs, 30 m 15.500 s', timedelta(hours=2,
                                               minutes=30,
                                               seconds=15,
                                               milliseconds=500)),
            ('45 m 20.200 s', timedelta(minutes=45,
                                        seconds=20,
                                        milliseconds=200)),
            ('0 hrs, 0 m 0.000 s', timedelta()),
            ('1.553 s', timedelta(seconds=1, microseconds=553000)),
            # ('10 s', timedelta(seconds=10)),
            ('Winner', timedelta(minutes=0)),
            ('10 s', timedelta(seconds=10)),
            ('1 m .511 s', timedelta(seconds=60, milliseconds=511)),
        ]

        for egap_str, expected in test_cases:
            self.assertEqual(parse_egap(egap_str), expected)

    #Well this wasn't so easy to test. But it should work
    def test_parse_line_no_space(self):
        line = """\
1	M-GHT	Mathias de Paulis Nilsson	SZ"""
        lst = parse_lines([line])
        self.assertEqual(lst, [['1', 'M-GHT', 'Mathias de Paulis Nilsson', 'SZ','']] )

    def test_parse_lines_with_space(self):
        line = """\
1	M-GHT	Calle Olsen [SZ]        SZ	50+"""
        lst = parse_lines([line])
        self.assertEqual(lst, [['1', 'M-GHT', 'Calle Olsen [SZ]', 'SZ', '50+', '']] )
