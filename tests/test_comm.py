import unittest
import json
from unittest.mock import patch, mock_open
from jinja2 import Template, Environment
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

###############################################################################
#                                 TestSafeRun                                 #
###############################################################################
class TestPiper(unittest.TestCase):
    def test_test(self):
        self.assertEqual(fun(1), 2)
