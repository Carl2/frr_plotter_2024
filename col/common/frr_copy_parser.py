#!/usr/bin/env python
from pdb import set_trace
from functools import reduce
from pprint import pprint
from icecream import ic
import pandas as pd

def merge_lines(init: dict, line)->dict:
    line_nr = init['line_nr']
    output_arr = init['output']
    #set_trace()
    if line_nr % 2 == 0:
        output_arr[-1] = output_arr[-1] + line
    else:
        output_arr.append(line + "\t")
    line_nr +=1
    return {"line_nr": line_nr, "output": output_arr}


def split_on_fn(delimiter:str):
    def split_on(line: str):
        fields = line.split(delimiter)
        return fields
    return split_on


def clean_performance_fields(list_fields: list[list[str]]):
    df = pd.DataFrame(data=list_fields)
    # index 0 - stage, 1 - class, 2 - club

    print(df[6])






def parse_lines(content: list[str]):
    vals= reduce(merge_lines,content,{"line_nr":1, "output": []})
    split_fn= split_on_fn('\t')

    len_lst = len(vals['output'])
    print(f"{len_lst}  lines: {vals['line_nr']}" )

    # split upp all the lines into fields.
    lst = [ split_fn(line ) for line in vals['output'] ]
    ic(lst[0])
    # Now we need some cleaning.
    return(lst)


def main():
    with open('tezt.txt', 'r') as file:
        lines = list(map(str.strip, file))

    lst = parse_lines(lines)
    clean_performance_fields(lst)

if __name__ == '__main__':
    main()
