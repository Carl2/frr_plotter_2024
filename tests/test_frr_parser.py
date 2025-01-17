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

# import pytest
# import sys  # For modifying sys.path temporarily if necessary
# import src.game_engine.data.messages as msg
# from src.common.Utils import (safe_run, get_utc_epoch_time)
# from src.common import Msg_types as types
# from src.common import Communication as com
#
from col.common.monadic import Maybe
from col.common.frr_copy_parser import split_on_fn, parse_effort, parse_egap

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



    def test_parse_effort(self ):

        string = "1 hrs, 1 m 13.338 s 223w @3.60WKG"
        vals = parse_effort(string)
        self.assertEqual(vals, (223, 3.6, timedelta(seconds=3673, microseconds=338000)))


        vals = parse_effort("1 hrs, 4 m 217w @3.20WKG")
        self.assertEqual(vals,(217,3.2, timedelta(seconds=1*3600+4*60)))


    def test_parse_egap(self):
        # Test various formats of egap strings
        ic(parse_egap('10 s'))
        ic(parse_egap('1 m .511 s'))
        ic(parse_egap('1.553 s'))
        test_cases = [
            ('1 m 3.115 s', timedelta(seconds=63, microseconds=115000)),
            ('32.646 s', timedelta(seconds=32, microseconds=646000)),
            ('1 m', timedelta(minutes=1)),
            ('Winner', timedelta(minutes=0)),
            # Additional test cases
            ('2 hrs, 30 m 15.500 s', timedelta(hours=2, minutes=30, seconds=15, milliseconds=500)),
            ('45 m 20.200 s', timedelta(minutes=45, seconds=20, milliseconds=200)),
            ('0 hrs, 0 m 0.000 s', timedelta()),
            ('1.553 s', timedelta(seconds=1, microseconds=553000)),
            #('1 m .511 s', timedelta(minutes=1, milliseconds=511000)),
            #('10 s', timedelta(seconds=10)),
            ('Winner', timedelta(minutes=0)),
        ]

        for egap_str, expected in test_cases:
            self.assertEqual(parse_egap(egap_str), expected)
