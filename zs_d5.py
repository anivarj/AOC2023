from pathlib import Path

from tqdm import tqdm

from helpers import (
    input_as_list,
    time_fxn,
    PERF,
    log_performance,
)

SEQUENCES = [
    'seed-to-soil',
    'soil-to-fertilizer',
    'fertilizer-to-water',
    'water-to-light',
    'light-to-temperature',
    'temperature-to-humidity',
    'humidity-to-location'
]

def parse_maps(
    string_input: list[str],
) -> dict[str, tuple[int, int]]:
    maps = {}
    start = 0
    parse = string_input[2:]
    for line_idx, line in enumerate(parse):
        if len(line) > 0 and not line[0].isdigit():
            start = line_idx
        if len(line) == 0 or line_idx == len(parse) - 1:
            end = line_idx
            if line_idx == len(parse) - 1:
                end = line_idx + 1
            maps[parse[start].split(' ')[0]] = (start+1, end)
    return maps

def solver(
    string_input: list[str],
    code_lines: tuple[int, int],
    input_val: int,
) -> int:
    parse = string_input[2:]
    start, stop = code_lines
    codes = parse[start: stop]
    for code in codes:
        ranges = [
            int(val)
            for val in code.split(' ')
        ]
        dest_rng_start, src_rng_start, rng_len = ranges
        if input_val >= src_rng_start and input_val < (src_rng_start + rng_len):
            # now we can map the input val to output vals
            diff = input_val - src_rng_start
            return dest_rng_start + diff
    #default condition       
    return input_val

@time_fxn()
def total_computation(
    input_file_path: Path
) -> str:
    string_input, seeds, maps = shared_computation(
        input_file_path,
    )
    part_1(string_input, seeds, maps)
    part_2(string_input, seeds, maps)
    return 'yay, finished!'

@time_fxn(print_val=False)
def shared_computation(
    input_file_path: Path,
) -> tuple[list[str], list[int], dict[str, tuple[int, int]]]:
    string_input = input_as_list(input_file_path)
    seeds = [
        int(seed)
        for seed in string_input[0].split('seeds: ')[-1].split(' ')
    ]
    maps = parse_maps(string_input)
    return string_input, seeds, maps

@time_fxn()
def part_1(
    string_input: list[str],
    seeds: list[int],
    maps: dict[str, tuple[int, int]],
) -> int:
    return return_min_loc(string_input, seeds, maps)

def return_min_loc(string_input, seeds, maps) -> int:
    loc_vals = []
    for seed in seeds:
        for sequence in SEQUENCES:
            seed = solver(
                string_input=string_input,
                code_lines=maps[sequence],
                input_val=seed
            )
        loc_vals.append(seed)
    return min(loc_vals)

@time_fxn()
def part_2(
    string_input: list[str],
    seeds: list[int],
    maps: dict[str, tuple[int, int]],
) -> None:
    intervals = []
    for start_idx in range(0, len(seeds), 2):
        start_val = seeds[start_idx]
        seed_range = (start_val, start_val+seeds[start_idx+1])
        intervals.append(seed_range)

    merged = merge_intervals(intervals)
    min_locs = []
    for seed_range_ends in merged:
        seed_range = range(seed_range_ends[0], seed_range_ends[1])
        for seed in seed_range:
            min_locs.append(
                return_min_loc(
                    string_input, [seed], maps
                )
            )
            break
    for seed_range_ends in merged:
        seed_range = range(seed_range_ends[0], seed_range_ends[1])
        for seed in tqdm(seed_range):
            min_locs.append(
                return_min_loc(
                    string_input, [seed], maps
                )
            )
            min_locs = [min(min_locs)]
    return min(min_locs)

def merge_intervals(
    intervals: list[tuple[int, int]],
) -> list[tuple[int, int]]:
    merged = []
    intervals.sort(key=lambda x: x[0])
    merged.append(intervals[0])
    for current in intervals[1:]:
        last_merged = merged[-1]
        if current[0] <= last_merged[1]:
            merged[-1] = (last_merged[0], max(last_merged[1], current[1]))
        else:
            merged.append(current)
    return merged



if __name__ == "__main__":
    total_computation(
        Path('./zs_d5.txt')
    )
    log_performance(
        f'{Path(__file__).stem}',
        PERF,
    )
