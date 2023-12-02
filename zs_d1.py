from pathlib import Path

from helpers import (
    input_as_list,
    time_fxn,
    CHAR_MAP,
)

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
    vals = []
    for line in lines:
        first_digit = first_int(line)
        last_digit = first_int(
            ''.join(reversed(line))
        )
        vals.append(
            int(first_digit + last_digit)
        )
    return sum(vals)

@time_fxn
def part_2(
    lines: list[str]
) -> int:
    vals = []
    for line in lines:
        first_digit = first_int_including_words(
            line,
            reverse_str=False
        )
        last_digit = first_int_including_words(
            ''.join(reversed(line)),
            reverse_str=True,
        )
        vals.append(
            int(first_digit + last_digit)
        )
    return sum(vals)

def first_int_including_words(
    line: str,
    reverse_str: bool,
    ) -> str:
    chars = ''
    for char in line:
        if char.isdigit():
            return char
        else:
            chars += char
            perms = permutations(chars, reverse_str)
            for perm in perms:
                if perm in CHAR_MAP and CHAR_MAP[perm].isdigit():
                    return CHAR_MAP[perm]
    raise ValueError('no integers found wtf')
    
def permutations(
    chars: str,
    reverse_str: bool,
) -> set[str]:
    perms = set()
    for start in range(len(chars)):
        for end in range(start + 1, len(chars) + 1):
            perm = chars[start:end]
            if reverse_str:
                perms.add(''.join(reversed(perm)))
            else:
                perms.add(perm)
    return perms

def first_int(line: str) -> str:
    for char in line:
        if char.isdigit():
            return char
    raise ValueError('no integers found wtf')

if __name__ == "__main__":
    main(
        Path('./zs_d1.txt')
    )
