import random
from typing import Union
from pathlib import Path
from functools import partial
from dataclasses import dataclass

from helpers import (
    input_as_list,
    time_fxn,
    PERF,
    log_performance,
)

class Game:

    ways: Union[int, None] = None

    def __init__(
        self,
        time: int,
        winning_distance: int,
    ) -> None:
        self.time = time
        self.winning_distance = winning_distance
        self.num_options = calc_options(time, winning_distance)
    
def calc_options(
    total_time: int,
    winning_distance: int,
) -> int:
    winning_time = find_winning_time(total_time, winning_distance)
    start_to_win_ms = recursively_search_for_start(
        start_time=0,
        end_time=winning_time,
        total_time=total_time,
        winning_distance=winning_distance
    )
    stop_to_win_ms = recursively_search_for_end(
        start_time=winning_time,
        end_time=total_time,
        total_time=total_time,
        winning_distance=winning_distance
    )
    return stop_to_win_ms - start_to_win_ms

def find_winning_time(
    total_time: int,
    winning_distance: int,
) -> int:
    """Randomly test 'held down' ms values until you find a winning one
    """
    while True:
        ms_held_down = random.randint(0, total_time)
        if is_winning(
            ms_held_down,
            total_time,
            winning_distance,
        ):
            return ms_held_down

def is_winning(
    ms_held_down: int,
    total_time: int,
    winning_distance: int,
) -> bool:
    """Return True if the boat wins after holding button down for `ms_held_down`
    """
    remaining_time = total_time - ms_held_down
    speed = ms_held_down
    dist_traveled = remaining_time * speed
    return dist_traveled > winning_distance

def recursively_search_for_start(
    start_time: int,
    end_time: int,
    total_time: int,
    winning_distance: int,
) -> int:
    winning = partial(is_winning, total_time=total_time, winning_distance=winning_distance)
    ms_tested = end_time - ((end_time - start_time) // 2)
    
    if winning(ms_tested) and not winning(ms_tested - 1):   # False, True; return value
        return ms_tested
    
    elif winning(ms_tested) and winning(ms_tested - 1): # True, True; search start_time to ms_tested
        return recursively_search_for_start(
            start_time=start_time,
            end_time=ms_tested - 1,
            total_time=total_time,
            winning_distance=winning_distance
        )
    
    else:
        return recursively_search_for_start(  # False, False; search ms_tested to end_time
            start_time=ms_tested + 1,
            end_time=end_time,
            total_time=total_time,
            winning_distance=winning_distance
        )

def recursively_search_for_end(
    start_time: int,
    end_time: int,
    total_time: int,
    winning_distance: int,
) -> int:
    winning = partial(is_winning, total_time=total_time, winning_distance=winning_distance)
    ms_tested = end_time - ((end_time - start_time) // 2)

    if winning(ms_tested) and not winning(ms_tested + 1):   # True, False; return value
        return ms_tested + 1
    
    elif winning(ms_tested) and winning(ms_tested + 1): # True, True; search ms_tested to end_time 
        return recursively_search_for_end(
            start_time=ms_tested + 1,
            end_time=end_time,
            total_time=total_time,
            winning_distance=winning_distance
        )
    
    else:
        return recursively_search_for_end(  # False, False; search start_time to ms_tested
            start_time=start_time,
            end_time=ms_tested - 1,
            total_time=total_time,
            winning_distance=winning_distance
        )

@time_fxn()
def main(
    input_file_path: Path
) -> str:
    string_input = shared_computation(
        input_file_path,
    )
    part_1(string_input)
    part_2(string_input)
    return 'yay, finished!'

@time_fxn(print_val=False)
def shared_computation(
    input_file_path: Path,
) -> list[str]:
    return input_as_list(input_file_path)

@time_fxn()
def part_1(
    string_input: list[str]
) -> int:

    times = [
        int(num)
        for num in string_input[0].split(' ')[1:]
        if num.isdigit()
    ]
    winning_distances = [
        int(num)
        for num in string_input[1].split(' ')[1:]
        if num.isdigit()
    ]
    games = [
        Game(time=time, winning_distance=winning_distance)
        for time, winning_distance in zip(times, winning_distances)
    ]

    num_ways_to_win = [
        game.num_options
        for game in games
    ]
    ans = num_ways_to_win[0]
    for num_ways in num_ways_to_win[1:]:
        ans *= num_ways
    
    return ans

@time_fxn()
def part_2(
    string_input: list[str]
) -> int:
    time = int(
        ''.join(
            num for num in string_input[0].split(' ')[1:]
            if num.isdigit()
        )
    )
    distance = int(
        ''.join(
            num for num in string_input[1].split(' ')[1:]
            if num.isdigit()
        )
    )
    game = Game(
        time=time,
        winning_distance=distance
    )
    return game.num_options

if __name__ == "__main__":
    main(
        Path('./zs_d6.txt')
    )
    log_performance(
        f'{Path(__file__).stem}',
        PERF,
    )
