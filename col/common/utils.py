#!/usr/bin/env python
from datetime import datetime,timedelta
from col.common.monadic import Maybe

def convert_to_time_repr(seconds: float):
    return str(timedelta(seconds=seconds))

def convert_to_val(val: str) -> Maybe[int]:
    """Converts a string value to an integer wrapped in a Maybe object.

    If the input string is non-empty and can be converted to an integer,
    it returns a Maybe object containing the integer. If the conversion fails,
    it returns a Maybe object with an error message. If the input string is
    empty or None, it returns a Maybe object containing 0.

    Args:
        val (str): The string value to convert.

    Returns:
        Maybe: A Maybe object containing either the converted integer,
        an error message, or 0.
    """
    if val is not None and len(val) > 0:
        try:
            return Maybe(int(val))
        except Exception as e:
            return Maybe(f"Unable to convert {val} to int", is_ok=False)
    return Maybe(0)
