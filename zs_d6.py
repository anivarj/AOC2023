from typing import Union
from pathlib import Path
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
        self.options = calc_options(time, winning_distance)
    
@dataclass
class Option:
    time_held_down: int
    dist_traveled: int
    winning: bool

def calc_options(
    total_time: int,
    winning_distance: int,
) -> list[Option]:
    options = []
    for ms_held_down in range(total_time+1):
        print(f'held down for {ms_held_down} of {total_time}')
        remaining_time = total_time - ms_held_down
        speed = ms_held_down
        dist_traveled = remaining_time * speed
        print(f'time_held_down={ms_held_down}, dist_traveled={dist_traveled}, winning={dist_traveled > winning_distance}')
        options.append(
            Option(
                time_held_down=ms_held_down,
                dist_traveled=dist_traveled,
                winning=dist_traveled > winning_distance
            )
        )
    return options

@time_fxn()
def main(
    input_file_path: Path
) -> str:
    games = shared_computation(
        input_file_path,
    )
    part_1(games)
    part_2()
    return 'yay, finished!'

@time_fxn(print_val=False)
def shared_computation(
    input_file_path: Path,
) -> list[Game]:
    string_input = input_as_list(input_file_path)
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
    return games

@time_fxn()
def part_1(
    games: list[Game]
) -> None:
    for g in games:
        num_ways_to_win = [
            option.winning
            for option in g.options
        ]
        g.ways = sum(num_ways_to_win)
    ans: int = games[0].ways
    for g in games[1:]:
        ans *= g.ways
    
    return ans

@time_fxn()
def part_2(
) -> None:
    ...

if __name__ == "__main__":
    main(
        Path('./zs_d6.txt')
    )
    log_performance(
        f'{Path(__file__).stem}',
        PERF,
    )
