from pathlib import Path

from helpers import (
    input_as_list,
    time_fxn,
)

@time_fxn()
def total_computation(
    input_file_path: Path
) -> str:
    res = shared_computation(
        input_file_path,
    )
    part_1()
    part_2()
    return 'yay, finished!'

@time_fxn(print_val=False)
def shared_computation(
) -> None:
    ...

@time_fxn()
def part_1(
) -> None:
    ...

@time_fxn()
def part_2(
) -> None:
    ...

if __name__ == "__main__":
    total_computation(
        Path('')
    )
