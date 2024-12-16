#!/usr/bin/env python

from datetime import timedelta
from functools import reduce
from pymonad.maybe import Maybe, Just, Nothing
from icecream import ic
import pandas as pd


def create_data(*, header: list[str], data: list[list]) -> pd.DataFrame:
    """Create a DataFrame from header and data where the index is the fourth column."""
    return pd.DataFrame(
        data=data,
        columns=header,
        index=[row[3] for row in data]
    )

def safe_find_fn(find_str: str, start: int = 0) -> callable:
    def find_fn(stringer: str) -> Maybe:
        end = len(stringer)
        pos = stringer.find(find_str, start, end)
        if pos != -1:

            return Just((pos + len(find_str), stringer[start:pos].strip()))
        else:
            return Nothing
    return find_fn


def gen_search_for_fn(search_str: str):
    def search_for(search_phrase: str,
                   next_pos: int = 0) -> Maybe[tuple[int, str]]:
        min_fn = safe_find_fn(search_phrase, next_pos)
        maybe_min = min_fn(search_str)
        if maybe_min.is_just():
            return Just(maybe_min.value)
        return Nothing

    return search_for


def split_by(search_str: str, keywords: list[str]) -> list[str]:
    """Split a string by the given keywords.

    This function searches for occurrences of the specified keywords in the
    provided search string. It returns a list of substrings found between
    those keywords. If a keyword is not found, None is added to the result
    list for that keyword.

    Args:
        search_str (str): The string in which to search for keywords.
        keywords (list[str]): A list of keywords to search for in the search_str.

    Returns:
        list[str]: A list of substrings found between the keywords.
                    If a keyword is not found, None is included in the list.
    """
    search_fn = gen_search_for_fn(search_str)

    def splitter_fn(init: dict, keyword) -> dict:
        search_fn = init[0]['fn']
        pos = init[0]['pos']
        maybe_ok = search_fn(keyword, pos)
        if maybe_ok.is_just():
            next_pos, item = maybe_ok.value
            init.append(item)
            init[0]['pos'] = next_pos
        else:
            init.append(None)

        return init

    output_arr = reduce(splitter_fn, keywords, [{'fn': search_fn, 'pos': 0}])
    return list(output_arr[1:])


if __name__ == '__main__':
    find_fn = safe_find_fn("hrs,")

    next_pos, hour_str = find_fn("1 hrs, 23 m 46.896 s").value

    find_fn = safe_find_fn("m", next_pos)
    next_pos, min_str = find_fn("1 hrs, 23 m 46.896 s").value
    ic(min_str)

    find_fn = safe_find_fn(" s", next_pos)
    next_pos, sec_str = find_fn("1 hrs, 23 m 46.896 s").value
    ic(sec_str)


    search_for = gen_search_for_fn("1 hrs, 46.896 s")
    next_pos, hours = search_for("hrs,").value
    ic(next_pos, hours)
    #set_trace()
    maybe_min = search_for("m", next_pos)
    if maybe_min.is_just():
        next_pos, val = maybe_min.value

    next_pos, seconds = search_for("s", next_pos).value
    ic(hours, seconds)
    # So far so good, but lets construct this so that we get
    # a dictionary with the key of the search pattern.
    # so instead i call split_by(("hrs,","m" "s"), time_str)
    ic(split_by("1 hrs, 23 m 46.896 s", ["hrs,", "m", ".", "s"]))
    ic(split_by("1 hrs, 46.896 s", ["hrs,", "m", "s"]))
    ic(split_by(" 45 m ", ["hrs,", "m", "s"]))
    ic(split_by("+6 m 48.655 s", ["+", "m", "s"]))
    ic(split_by("", ["+", "m", ".", "s"]))
    print("Done")
