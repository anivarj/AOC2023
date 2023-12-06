from pathlib import Path

from helpers import (
    input_as_list,
    time_fxn,
    PERF,
    log_performance,
)

def parse_maps(
    string_input: list[str],
) -> dict[str, dict[int, int]]:
    maps = {}
    start = 0
    parse = string_input[2:]
    for line_idx, line in enumerate(parse):
        print(f'line {line_idx+1} / {len(parse)}')
        if len(line) > 0 and not line[0].isdigit():
            start = line_idx
        if len(line) == 0 or line_idx == len(parse) - 1:
            end = line_idx
            maps[parse[start].split(' ')[0]] = dict_factory(
                list_of_string = parse,
                start = start,
                end = end,
                add_one = line_idx == len(parse) - 1
            )
    return maps

def dict_factory(
    list_of_string: list[str],
    start: int,
    end: int,
    add_one: bool,
) -> dict[int, int]:
    res = {}
    end = end + 1 if add_one else end
    codes = list_of_string[start+1: end]
    for code in codes:
        ranges = code.split(' ')
        dest_range_start = int(ranges[0])
        source_range_start = int(ranges[1])
        range_len = int(ranges[2])
        dest_range = range(dest_range_start, dest_range_start + range_len)
        source_range = range(source_range_start, source_range_start + range_len)
        res.update(
            {
                source: dest
                for source, dest in zip(source_range, dest_range)
            }
        )
    return res

@time_fxn()
def total_computation(
    input_file_path: Path
) -> str:
    seeds, maps = shared_computation(
        input_file_path,
    )
    part_1(seeds, maps)
    part_2()
    return 'yay, finished!'

@time_fxn(print_val=False)
def shared_computation(
    input_file_path: Path,
) -> tuple[list[str], dict[str, dict[int, int]]]:
    string_input = input_as_list(input_file_path)
    seeds = string_input[0].split('seeds: ')[-1].split(' ')
    maps = parse_maps(string_input)
    print('maps')
    for k, v in maps.items():
        print(k, len(v))
    return seeds, maps

@time_fxn()
def part_1(
    seeds: list[int],
    maps: dict[str, dict[int, int]],
) -> None:
    loc_nums = []
    for seed in seeds:
        soil = try_to_map(maps, 'seed-to-soil', int(seed))
        fert = try_to_map(maps, 'soil-to-fertilizer', soil)
        water = try_to_map(maps, 'fertilizer-to-water', fert)
        light = try_to_map(maps, 'water-to-light', water)
        temp = try_to_map(maps, 'light-to-temperature', light)
        humid = try_to_map(maps, 'temperature-to-humidity', temp)
        location = try_to_map(maps, 'humidity-to-location', humid)
        loc_nums.append(location)
    print(loc_nums)
    return min(loc_nums)

def try_to_map(
    maps: dict[str, dict[int, int]],
    string_key: str,
    int_key: int,
) -> int:
    try:
        res = maps[string_key][int_key]
    except KeyError:
        res = int_key
    return res

@time_fxn()
def part_2(
) -> None:
    ...

if __name__ == "__main__":
    total_computation(
        Path('./zs_d5_test.txt')
    )
    log_performance(
        f'{Path(__file__).stem}',
        PERF,
    )
