from typing import TypeVar, Generic, Callable
from copy import deepcopy

T = TypeVar('T')
U = TypeVar('U')

class Maybe(Generic[T]):
    def __init__(self, args: T, is_ok: bool = True):
        self.val = args
        self.is_ok: bool = is_ok

    def bind(self, fn: Callable[[T], 'Maybe[U]']) -> 'Maybe[U]':
        if self.is_ok:
            return fn(self.val)
        else:
            return self

    def map(self, fn: Callable[[T], U]) -> 'Maybe[U]':
        """Map a fn f:T->U
        """
        if self.is_ok:
            return Maybe(fn(self.val), True)
        else:
            return self


    def exec(self, fn: Callable[[T], U]) -> 'Maybe[U]':
        if not self.is_ok:
            return self

        result = fn(self.val)

        if isinstance(result, Maybe):
            return result
        else:
            return Maybe(result)

    def __eq__(self, other):
        """
        Compare two Maybe instances for equality.
        """
        if isinstance(other, Maybe):
            return self.is_ok == other.is_ok and self.val == other.val
        elif isinstance(other, bool):
            return self.is_ok == other
        return False

    def __repr__(self):
        return f"Maybe(val={self.val}, is_ok={self.is_ok})"



class TracerResult(Maybe):
      def __init__(self, args: T, trace_log: list = None, is_ok: bool = True):
          super().__init__(args, is_ok)
          self.trace_log = trace_log if trace_log is not None else []

      def bind(self, fn: Callable[[T], 'TracerResult[U]']) -> 'TracerResult[U]':
          if self.is_ok:
              result = fn(self.val)
              new_trace_log = self.trace_log + [f"{fn.__name__}({self.val}) -> {result.val}"]
              return TracerResult(result.val, new_trace_log, result.is_ok)
          else:
              return TracerResult(self.val, self.trace_log, is_ok=False)

      def __repr__(self):
          return f"TracerResult(val={self.val}, trace_log={self.trace_log}, is_ok={self.is_ok})"


def convert(transform_fn: Callable[[T], U]) -> Callable[[T], Maybe[U]]:
    def convert_fn(T) -> Maybe[U]:
        return transform_fn(T)

    return convert_fn




def safer_exec(func: Callable) -> Callable:
    """
    A decorator that wraps a function to safely handle exceptions.

    This decorator catches any exceptions raised by the function, returning
    a Maybe instance with the error value if an exception occurs. If the
    function executes successfully, it wraps the return value in a Maybe
    instance.

    Usage:
        @safer_exec
        def example_function(x: int, y: int) -> int:
            return x / y  # This can raise a ZeroDivisionError

        result = example_function(10, 0)
        print(result)  # Output: Maybe(val=ZeroDivisionError, is_ok=False)

    Args:
        func (Callable): The function to be decorated.

    Returns:
        Callable: The wrapped function that returns a Maybe instance.
    """
    def exec_safe(**kwargs):
        try:
            return Maybe(func(**kwargs))
        except Exception as e:
            return Maybe(args=e, is_ok=False)
    return exec_safe
