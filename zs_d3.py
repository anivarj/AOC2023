import re
import uuid
from pathlib import Path

from helpers import (
    input_as_list,
    time_fxn,
)

def get_all_adj_idx(
    idx_list: list[tuple[int, int]],
    max_num_rows: int,
    max_num_cols: int
) -> list[tuple[int, int]]:
    adj_coords = []
    for idx in idx_list: 
        adj_coords_for_idx = get_all_adjacent_coords(idx)
        for adj_coord in adj_coords_for_idx:
            row_idx, col_idx = adj_coord
            if col_idx >= max_num_cols or row_idx >= max_num_rows:
                continue
            adj_coords.append(adj_coord)
    return adj_coords

def get_all_adjacent_coords(
    idx: tuple[int, int],
) -> list[tuple[int, int]]:
    row_idx, col_idx = idx
    row_range = range(row_idx - 1, row_idx + 2)
    col_range = range(col_idx - 1, col_idx + 2)
    idxs = []
    for row in row_range:
        for col in col_range:
            if row_idx == row and col_idx == col:
                continue
            if row == -1 or col == -1:
                continue
            idxs.append((row, col))
    return idxs

class Symbol:

    def __init__(
        self,
        idx: tuple[int, int]
    ) -> None:
        self.idx = idx
        self.adj_num_uids = set()
        self.adj_num_vals = []

    def set_adj_idx(
        self,
        max_num_rows,
        max_num_cols,
    ) -> None:
        self.all_adj_idxs = get_all_adj_idx(
            idx_list = [self.idx],
            max_num_cols = max_num_cols,
            max_num_rows = max_num_rows
        )

class Number:

    def __init__(
        self,
        value: int,
        start_idx: tuple[int, int],
        length: int,
    ) -> None:
        self.value = value
        self.start_idx = start_idx
        self.length = length
        self.uid = uuid.uuid4()
        self.all_idxs = self.get_all_idx_for_number()

    def get_all_idx_for_number(self)-> list[tuple[int, int]]:
        return [
            (self.start_idx[0], col)
            for col in range(
                self.start_idx[1],
                self.start_idx[1] + self.length
            )
        ]
    
    def set_adj_idx(
        self,
        max_num_rows: int,
        max_num_cols: int,
    ) -> None:
        self.all_adj_idxs = get_all_adj_idx(
            self.all_idxs,
            max_num_cols = max_num_cols,
            max_num_rows = max_num_rows
        )

@time_fxn()
def main(
    input_file_path: Path
) -> str:
    symbols = shared_computation(input_file_path)
    part_1(symbols)
    part_2(symbols)
    return 'yay, finished!'

@time_fxn(print_val=False)
def shared_computation(
    filepath: Path,
) -> list[Symbol]:
    lines = input_as_list(filepath)
    max_row_idx = len(lines)
    max_col_idx = len(lines[0])
    symbols = collect_symbols(lines, max_row_idx, max_col_idx)
    numbers = collect_numbers(lines)
    for symbol in symbols:
        for adj_idx in symbol.all_adj_idxs:
            for number in numbers:
                if all(
                    [
                        adj_idx in number.all_idxs,
                        not number.uid in symbol.adj_num_uids
                    ]
                ):
                    symbol.adj_num_uids.add(number.uid)
                    symbol.adj_num_vals.append(number.value)
    return symbols

def collect_symbols(
    lines: list[str],
    max_row_idx: int,
    max_col_idx: int,
) -> list[Symbol]:
    symbols = []
    for line_idx, line in enumerate(lines):
        for row_idx, char in enumerate(line):
            if not char.isdigit() and not char == '.':
                symbol = Symbol((line_idx, row_idx))
                symbol.set_adj_idx(
                    max_num_rows=max_row_idx,
                    max_num_cols=max_col_idx,
                )
                symbols.append(
                    symbol
                )
    return symbols            

def collect_numbers(
    lines: list[str],
) -> list[Number]:
    numbers = []
    for line_idx, line in enumerate(lines):
        matches = re.finditer(
            pattern = r"\d+",
            string = line,
        )
        for num_match in matches:
            numbers.append(
                Number(
                    value = int(num_match.group(0)),
                    start_idx = (line_idx, num_match.start()),
                    length = num_match.end() - num_match.start()
                )
            )
    return numbers
    
@time_fxn()
def part_1(
    symbols: list[Symbol],
) -> int:
    nums_by_symbol_vals = [
        number for symbol in symbols
        for number in symbol.adj_num_vals
    ]
    return sum(nums_by_symbol_vals)

@time_fxn()
def part_2(
    symbols: list[Symbol],
) -> int:
    gear_ratios = []
    for symbol in symbols:
        if len(symbol.adj_num_vals) == 2:
            first, second = symbol.adj_num_vals
            gear_ratios.append(first * second)
    return sum(gear_ratios)

if __name__ == "__main__":
    main(
        Path('./zs_d3.txt')
    )
