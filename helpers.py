import time
import functools
from pathlib import Path
from typing import Callable

def input_as_list(
    filepath: Path,
) -> list[str]:
    """Return a text file as a list of strings.
    """
    with open(filepath) as f:
        output = [
            line.rstrip()
            for line in f.readlines()
        ]
    return output

def time_fxn(func: Callable):
    """Print the time required to run the decorated fxn.
    """
    @functools.wraps(func)
    def wrapper_time_fxn(*args, **kwargs):
        start_time = time.perf_counter()
        val = func(*args, **kwargs)
        end_time = time.perf_counter()
        run_time = end_time - start_time
        print(f"Finished {func.__name__!r} in {run_time:.4f} secs with return value {val}")
        return val
    return wrapper_time_fxn

CHAR_MAP = {
    'one': '1',
    'two': '2',
    'three': '3',
    'four': '4',
    'five': '5',
    'six': '6',
    'seven': '7',
    'eight': '8',
    'nine': '9',
}
