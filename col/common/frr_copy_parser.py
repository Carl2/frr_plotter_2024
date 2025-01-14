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


def make_performance_dataframe(list_fields: list[list[str]]):
    # 0 - stage, 1 - class, 3 - name, 2 - club , 5 - exp, 4 - egap,
    # 6 - effort, 7 - Polka, 8 - sprint , 9 - finish, 10- vbw, 11- upg, 12- total
    header = ['stage', 'class', 'name','club',  'exp', 'egap', 'effort', 'polka', 'sprint', 'finish', 'vbw', 'upg', 'total' ]

    df = pd.DataFrame(data=list_fields, columns=header)
    #df = pd.DataFrame(data=list_fields)
    print(df[df['stage'] > '4'][['stage','name','egap']])
    #print(df[df['index'] == '4'])
    #print(df[0], df[1],df[2],df[3],df[4],df[5],df[6],df[7],df[8], df[9], df[10], df[11], df[12])
    return df





def parse_lines(content: list[str]):
    vals= reduce(merge_lines,content,{"line_nr":1, "output": []})
    split_fn= split_on_fn('\t')

    len_lst = len(vals['output'])
    print(f"{len_lst}  lines: {vals['line_nr']}" )

    # split upp all the lines into fields.
    lst = [ split_fn(line ) for line in vals['output'] ]
    #ic(lst[0])
    # Now we need some cleaning.
    return(lst)


def main():
    with open('tezt.txt', 'r') as file:
        lines = list(map(str.strip, file))

    lst = parse_lines(lines)
    df = make_performance_dataframe(lst)



if __name__ == '__main__':
    main()
