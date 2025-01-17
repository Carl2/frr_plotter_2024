#!/usr/bin/env python
from pdb import set_trace
from functools import reduce
from pprint import pprint
from icecream import ic
import pandas as pd
from datetime import timedelta
from col.common.monadic import safer_exec,Maybe
from col.common.split_by import split_by
from typing import Callable


def split_on_fn(delimiter: str) -> Callable[[str], Maybe]:

    def split_on(line: str) -> Maybe:
        if line is not None:
            fields = line.split(delimiter)
            if len(fields) > 1:
                return Maybe(fields)
            return Maybe(fields, is_ok=False)
        return Maybe("String is None", is_ok=False)

    return split_on





def parse_time_str(time_str):
    part = split_by(time_str, ["hrs,", "m", ".", "s"])
    hours = convert_to_val(part[0])
    minutes = convert_to_val(part[1])
    seconds = convert_to_val(part[2])
    milli = convert_to_val(part[3])
    return timedelta(hours=hours, minutes=minutes,
                     seconds=seconds, milliseconds=milli)


def merge_lines(init: dict, line)->dict:
    line_nr = init['line_nr']
    output_arr = init['output']
    if line_nr % 2 == 0:
        output_arr[-1] = output_arr[-1] + line
    else:
        output_arr.append(line + "\t")
    line_nr +=1
    return {"line_nr": line_nr, "output": output_arr}





def convert_to_val(val: str) -> int:
    if val is not None and len(val) > 0:
        return int(val)
    return 0

def convert_str_array_to_int(arr: list[str])->list[int]:
    return [convert_to_val(item) for item in arr]


def parse_effort(effort_str):
    ic(effort_str)
    """Parse effort

    The current effort loooks something like
    1 hrs, 9 m 43.929 s 268w @3.30WKG
    or
    57 m 43.731 s 281w @3.50WKG
    So here we can use the

    split_by( 1 hrs, 9 m 43.929 s 268w @3.30WKG,
    ['hrs,', 'm', 's','w','wkg' ]
    )

    """
    part=split_by(effort_str, ['hrs,', 'm','s','w', '@', 'WKG'])
    hours = convert_to_val(part[0])
    minutes = convert_to_val(part[1])
    time_delta = timedelta(hours=hours, minutes=minutes)

    splitter = split_on_fn('.')
    maybe_secods = splitter(line=part[2]).map(convert_str_array_to_int)

    if maybe_secods == True:
        time_delta += timedelta(seconds=maybe_secods.val[0], milliseconds=maybe_secods.val[1])

    watts = int(part[3])
    wkg = float(part[5])
    return watts,wkg,time_delta


def parse_egap(egap_str: str)->timedelta:
    ic(egap_str)
    td = timedelta(seconds = 0)
    if egap_str.lower() != 'Winner':
        hours,minutes,seconds, milli = split_by(egap_str, ['hrs,','m','.','s'])
        ic(hours,minutes,seconds, milli)
        td = timedelta(
            hours=convert_to_val(hours),
            minutes=convert_to_val(minutes),
            seconds=convert_to_val(seconds),
            milliseconds=convert_to_val(milli))
    return td





def make_performance_dataframe(list_fields: list[list[str]]):
    # 0 - stage, 1 - class, 3 - name, 2 - club , 5 - exp, 4 - egap,
    # 6 - effort, 7 - Polka, 8 - sprint , 9 - finish, 10- vbw, 11- upg, 12- total
    header = ['stage', 'class', 'name','club',  'exp', 'egap', 'effort', 'polka', 'sprint', 'finish', 'vbw', 'upg', 'total' ]

    df = pd.DataFrame(data=list_fields, columns=header)
    new_columns = df['effort'].apply(parse_effort).apply(pd.Series)
    new_columns.columns = ['watts', 'wkg', 'time_delta']
    df = pd.concat([df, new_columns], axis=1)

    egap_columns = df['egap'].apply(parse_egap)

    return df

def parse_lines(content: list[str]):
    vals= reduce(merge_lines,content,{"line_nr":1, "output": []})


    len_lst = len(vals['output'])
    print(f"{len_lst}  lines: {vals['line_nr']}" )

    # split upp all the lines into fields.
    split_fn= split_on_fn('\t')
    lst = [ split_fn(line ).val for line in vals['output'] ]
    #ic(lst[0])
    # Now we need some cleaning.
    return(lst)


def parse_file(file_name: str) -> pd.DataFrame:
    with open(file_name, 'r') as file:
        lines = list(map(str.strip, file))

    lst = parse_lines(lines)
    df = make_performance_dataframe(lst)
    return df


if __name__ == '__main__':
    parse_file("tezt.txt")
