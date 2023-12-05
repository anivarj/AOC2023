from pathlib import Path

from helpers import (
    input_as_list,
    time_fxn,
)

class Card:

    def __init__(
        self,
        card_idx: int,
        card_num: int,
        winning_nums: list[int],
        actual_nums: list[int],
    ) -> None:
        self.card_num = card_num
        self.winning_nums = winning_nums
        self.actual_nums = actual_nums
        self.score, self.num_matches = self.score_card()

    def score_card(
        self,
    ) -> tuple[int, int]:
        score = 0
        num_matches = 0
        for winning_num in self.winning_nums:
            if winning_num in self.actual_nums:
                num_matches += 1
                if score == 0:
                    score = 1
                else:
                    score *= 2
        return score, num_matches
    
    @classmethod
    def from_line(
        cls,
        idx: int,
        line: str,
    ) -> 'Card':
        card_contents, num_contents = line.split(':')
        card_num = int(card_contents.split(" ")[-1])
        winning_contents, losing_contents = num_contents.split(' | ')
        winning_nums = [
            int(val)
            for val in winning_contents.split(' ')
            if val.isdigit()
        ]
        losing_nums = [
            int(val)
            for val in losing_contents.split(' ')
            if val.isdigit()
        ]
        return Card(
            card_num=card_num,
            card_idx=idx,
            winning_nums=winning_nums,
            actual_nums=losing_nums,
        )

@time_fxn()
def main(
    input_file_path: Path
) -> str:
    cards = shared_computation(
        input_file_path,
    )
    part_1(cards)
    part_2(cards)
    return 'yay, finished!'

@time_fxn(print_val=False)
def shared_computation(
    input_file_path: Path,
) -> dict[int, Card]:
    lines = input_as_list(input_file_path)
    cards = {
        idx: Card.from_line(idx, line)
        for idx, line in enumerate(lines)
    }
    return cards

@time_fxn()
def part_1(
    cards: dict[int, Card]
) -> int:
    points = [
        card.score
        for card in cards.values()
    ]
    return sum(points)

@time_fxn()
def part_2(
    cards: dict[int, Card]
) -> int:
    originals_and_copies = []
    for card_idx in cards:
        originals_and_copies = count_copies_recursively(
            cards=cards,
            card_idx=card_idx,
            originals_and_copies=originals_and_copies
        )
    return len(originals_and_copies)

def count_copies_recursively(
    cards: dict[int, Card],
    card_idx: int,
    originals_and_copies: list,
) -> list[int]:
    originals_and_copies.append(card_idx)
    card = cards[card_idx]
    for idx in range(card_idx+1, card_idx+1+card.num_matches):
        count_copies_recursively(
            cards=cards,
            card_idx=idx,
            originals_and_copies=originals_and_copies,
        )
    return originals_and_copies

if __name__ == "__main__":
    main(
        Path('./zs_d4.txt')
    )
