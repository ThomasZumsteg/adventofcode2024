"""Solution to day 12 of Advent of Code"""

from get_input import get_input, line_parser
from functools import cache


Input = int


@cache
def expand(stone, times) -> int:
    if times == 0:
        return 1
    if stone == 0:
        return expand(1, times-1)
    elif len(str(stone)) % 2 == 0:
        half = len(str(stone)) // 2
        return expand(int(str(stone)[:half]), times-1) + \
            expand(int(str(stone)[half:]), times-1)
    else:
        return expand(stone * 2024, times-1)


def part1(stones: list[Input], times=25) -> int:
    return sum(expand(stone, times) for stone in stones)


def part2(stones: list[Input]) -> int:
    return part1(stones, 75)


TEST_TEXT = """125 17"""


def test_part1():
    assert part1(line_parser(TEST_TEXT, seperator=' ', parse=int)) == 55312


if __name__ == "__main__":
    LINES = line_parser(get_input(day=11, year=2024), seperator=' ', parse=int)
    print(f"Part 1: {part1(LINES)}")
    print(f"Part 2: {part2(LINES)}")
