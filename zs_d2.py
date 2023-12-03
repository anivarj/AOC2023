from pathlib import Path
from enum import Enum

from helpers import (
    input_as_list,
    time_fxn,
)

MIN_RED = 12
MIN_GREEN = 13
MIN_BLUE = 14

class Game:
    def __init__(
        self,
        line: str,
    ) -> None:
        self.line = line
        self.parse_input(line)
    
    def parse_input(
        self,
        line: str,
    ) -> None:
        self.id = int(line.split('Game ')[-1].split(':')[0])
        pulls = line.split(': ')[-1].split('; ')
        self.pulls = [
            Pull(pull)
            for pull in pulls
        ]

class Pull:
    def __init__(
        self,
        bag_pull: str,
    ) -> None:
        self.parse_input(bag_pull)

    def parse_input(
        self,
        bag_pull: str,
    ) -> None:
        cubes = bag_pull.split(', ')
        self.red = self.find_num_cubes(cubes, 'red')
        self.green = self.find_num_cubes(cubes, 'green')
        self.blue = self.find_num_cubes(cubes, 'blue')

    def find_num_cubes(
        self,
        cubes: list[str],
        cube_type: str,
    ) -> int:
        for cube in cubes:
            if cube_type in cube:
                return int(cube.split(' ')[0])
        return 0

@time_fxn
def main(
    input_file_path: Path
) -> str:
    lines = input_as_list(input_file_path)
    part_1(lines)
    part_2(lines)
    return 'yay, finished!'

@time_fxn
def part_1(
    lines: list[str]
) -> int:
    games = [
        Game(line)
        for line in lines
    ]
    good_games = []
    for game in games:
        good_pulls = []
        for pull in game.pulls:
            good_pulls.append(
                all(
                    [
                        pull.red <= MIN_RED,
                        pull.green <= MIN_GREEN,
                        pull.blue <= MIN_BLUE
                    ]
                )
            )
        if all(good_pulls):
            good_games.append(game.id)
    return sum(good_games)

@time_fxn
def part_2(
    lines: list[str]
) -> int:
    games = [
        Game(line)
        for line in lines
    ]
    game_powers = []
    for game in games:
        min_red = max(
            [
                pull.red
                for pull in game.pulls
            ]
        )
        min_green = max(
            [
                pull.green
                for pull in game.pulls
            ]
        )
        min_blue = max(
            [
                pull.blue
                for pull in game.pulls
            ]
        )
        game_powers.append(min_red * min_green * min_blue)
    return sum(game_powers)


if __name__ == "__main__":
    main(
        Path('./zs_d2.txt')
    )
