import unittest
import json
from unittest.mock import patch, mock_open
#from jinja2 import Template, Environment
from datetime import datetime
#from game_engine.data.messages import render_message
# from src.game_engine.data.messages import render_message, login_message
from pdb import set_trace


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
