import json
import time
import functools
from pathlib import Path
from typing import Callable, TypeVar, Any, cast

PERF = {}

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

T = TypeVar('T')  # Type variable to capture the return type of the decorated function

def time_fxn(print_val: bool = True):
    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        @functools.wraps(func)
        def wrapper_time_fxn(*args: Any, **kwargs: Any) -> T:
            start_time = time.perf_counter()
            val = func(*args, **kwargs)
            end_time = time.perf_counter()
            run_time = end_time - start_time
            if print_val:
                print(f"Finished {func.__name__!r} in {run_time:.4f} secs with return value {val}")
            else:
                print(f"Finished {func.__name__!r} in {run_time:.4f} secs")
            PERF[f'{func.__name__!r}'] = run_time
            return val
        return cast(Callable[..., T], wrapper_time_fxn)
    return decorator

def log_performance(
    file_name: str,
    perf: dict[str, float],
    file_path: Path = Path('perf.json'),
) -> None:
    with open(file_path, 'r') as f:
        data = json.load(f)
    data[file_name] = perf
    with open(file_path, 'w') as f:
        json.dump(data, f, indent=4)


    

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
