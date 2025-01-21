#!/usr/bin/env python
from col.common.frr_copy_parser import parse_file
from pdb import set_trace
from icecream import ic

def main():
    df=parse_file("tezt.txt")
    ic(df)


if __name__ == '__main__':
    main()
