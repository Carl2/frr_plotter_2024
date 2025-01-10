#!/usr/bin/env python

from icecream import ic

from typing import (Callable, Tuple,
                    TypeVar, Generic,
                    Optional, Union,
                    List)

from enum import Enum
from dataclasses import dataclass
from copy import copy

# Type variables
S = TypeVar('S')  # State type
A = TypeVar('A')  # Value type

class State(Generic[S, A]):
    def __init__(self, run_state: Callable[[S], Tuple[A, S]]):
        self.run_state = run_state

    def __call__(self, state: S) -> Tuple[A, S]:
        return self.run_state(state)

    def bind(self, f: Callable[[A], 'State[S, A]']) -> 'State[S, A]':
        def new_state(s: S) -> Tuple[A, S]:
            value, next_state = self.run_state(s)
            return f(value).run_state(next_state)
        return State(new_state)

    @staticmethod
    def unit(value: A) -> 'State[S, A]':
        return State(lambda s: (value, s))

    @staticmethod
    def get() -> 'State[S, S]':
        return State(lambda s: (s, s))

    @staticmethod
    def put(new_state: S) -> 'State[S, None]':
        return State(lambda _: (None, new_state))


###########################################################################
#                            End of state monad                           #
###########################################################################
@dataclass
class FieldCapture:
    records: list[list[str]]
    last_line: list[str]
    current_line: int
    lines_to_concat: int

def make_table(file_path: str) -> Optional[List[str]]:
    try:
        with open(file_path, 'r') as txt_file:
            return txt_file.readlines()
    except FileNotFoundError:
        return None


def handle_line(current_line:str)->Callable[[A], 'State[S,A]']:
    def handle_state(current_state: FieldCapture) -> Tuple[A,S]:
        new_state = copy(current_state)
        if new_state.current_line % 2 == new_state.lines_to_concat:
            new_state.records = new_state.last_line + current_line
        else:
            new_state.last_line = current_line










def main():
    initial_state = FieldCapture([],"",0,2)

    lines = make_table("test_record.txt")

    ic(lines)


if __name__ == '__main__':
    main()
