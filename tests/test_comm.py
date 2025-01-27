import unittest
import json
from unittest.mock import patch, mock_open
#from jinja2 import Template, Environment
from datetime import datetime
#from game_engine.data.messages import render_message
# from src.game_engine.data.messages import render_message, login_message
from pdb import set_trace
import pandas as pd
from icecream import ic
from col.plot.plot import filter_by, make_plot_handler
import numpy as np

# import pytest
# import sys  # For modifying sys.path temporarily if necessary
# import src.game_engine.data.messages as msg
# from src.common.Utils import (safe_run, get_utc_epoch_time)
# from src.common import Msg_types as types
# from src.common import Communication as com
#
from col.comm.piper import *
from col.common.monadic import Maybe

###############################################################################
#                                 TestSafeRun                                 #
###############################################################################
# class TestPiper(unittest.TestCase):
#     def test_test(self):
#         self.assertEqual(fun(1), 2)

def make_df():
    data = []
    names = ["Calle Olsen", "Steinar Wagnen", "Erik Berg", "Lars Petter", "Magnus Dahl"]

    # First two riders participate in all stages
    for stage in range(1, 9):
        data.append({"name": names[0], "stage": stage, "position": stage % 3 + 1, "watt": 220 + stage * 5})
        data.append({"name": names[1], "stage": stage, "position": stage % 4 + 2, "watt": 230 + stage * 4})

    # Third rider participates in stages 1-5
    for stage in range(1, 6):
        data.append({"name": names[2], "stage": stage, "position": stage % 3 + 3, "watt": 240 + stage * 3})

    # Fourth rider participates in stages 2-6
    for stage in range(2, 7):
        data.append({"name": names[3], "stage": stage, "position": stage % 3 + 2, "watt": 250 + stage * 2})

    # Fifth rider participates in stages 4-8
    for stage in range(4, 9):
        data.append({"name": names[4], "stage": stage, "position": stage % 3 + 1, "watt": 260 + stage})

    df = pd.DataFrame(data)
    return df


###############################################################################
#                               TestCommon maybe                              #
###############################################################################

class TestMonadics(unittest.TestCase):

    def test_maybe_initialization(self):
        maybe_ok = Maybe(5, True)
        self.assertEqual(maybe_ok.val, 5)
        self.assertTrue(maybe_ok.is_ok)

        maybe_not_ok = Maybe(10, False)
        self.assertEqual(maybe_not_ok.val, 10)
        self.assertFalse(maybe_not_ok.is_ok)

    def test_maybe_bind(self):
        maybe_ok = Maybe(5, True)
        result = maybe_ok.bind(lambda x: Maybe(x + 1))
        self.assertEqual(result.val, 6)
        self.assertTrue(result.is_ok)

        maybe_not_ok = Maybe(10, False)
        result = maybe_not_ok.bind(lambda x: Maybe(x + 1))
        self.assertEqual(result.val, 10)
        self.assertFalse(result.is_ok)

    def test_maybe_map(self):
        maybe_ok = Maybe(5, True)
        result = maybe_ok.map(lambda x: x * 2)
        self.assertEqual(result.val, 10)
        self.assertTrue(result.is_ok)

        maybe_not_ok = Maybe(10, False)
        result = maybe_not_ok.map(lambda x: x * 2)
        self.assertEqual(result.val, 10)
        self.assertFalse(result.is_ok)

    def test_maybe_exec(self):
        maybe_ok = Maybe(5, True)
        result = maybe_ok.exec(lambda x: x + 3)
        self.assertEqual(result.val, 8)
        self.assertTrue(result.is_ok)

        maybe_not_ok = Maybe(10, False)
        result = maybe_not_ok.exec(lambda x: x + 3)
        self.assertEqual(result.val, 10)
        self.assertFalse(result.is_ok)

    def test_maybe_eq(self):
        maybe_a = Maybe(5, True)
        maybe_b = Maybe(5, True)
        self.assertEqual(maybe_a, maybe_b)

        maybe_c = Maybe(5, False)
        self.assertNotEqual(maybe_a, maybe_c)

        self.assertTrue(maybe_a == True)
        self.assertTrue(maybe_c == False)

    def test_maybe_repr(self):
        maybe_ok = Maybe(5, True)
        self.assertEqual(repr(maybe_ok), "Maybe(val=5, is_ok=True)")

        maybe_not_ok = Maybe(10, False)
        self.assertEqual(repr(maybe_not_ok), "Maybe(val=10, is_ok=False)")

    def test_make_plot_handler(self):
        df = make_df()

        # Make a filter function using filter_by
        filter_fn = filter_by(match_field='stage', output_field='name')
        ic(filter_fn(df, 6))
        ic(df)
        handler_fn = make_plot_handler(lambda x: x, filter_fn)
        arr = np.full(5, np.nan)
        out = handler_fn({"data": df, "value": arr, "index": 3}, df)
        ic(out)
