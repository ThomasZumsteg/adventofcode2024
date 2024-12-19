"""Solution to day 19 of Advent of Code"""

from get_input import get_input
from functools import cache
from dataclasses import dataclass


@dataclass(frozen=True)
class Input:
    towels: tuple[str]
    patterns: tuple[str]

    def search(self, pattern: str) -> bool:
        if pattern == "":
            return True
        for towel in self.towels:
            if pattern.startswith(towel) and \
                    self.search(pattern[len(towel):]):
                return True
        return False

    @cache
    def ways(self, pattern: str) -> int:
        if pattern == "":
            return 1
        ways = 0
        for towel in self.towels:
            if not pattern.startswith(towel):
                continue
            ways += self.ways(pattern[len(towel):])
        return ways


def part1(towels: list[Input]) -> int:
    total = 0
    for pattern in towels.patterns:
        if towels.search(pattern):
            total += 1
    return total


def part2(towels: list[Input]) -> int:
    total = 0
    for p, pattern in enumerate(towels.patterns):
        total += towels.ways(pattern)
    return total


def parse(text: str) -> Input:
    lines = iter(text.strip().split('\n'))
    towels = next(lines).split(', ')
    assert next(lines) == ""
    patterns = list(lines)
    return Input(tuple(towels), tuple(patterns))


TEST_TEXT = """
r, wr, b, g, bwu, rb, gb, br

brwrr
bggr
gbbr
rrbgbr
ubwu
bwurrg
brgr
bbrgwb
"""


def test_part1():
    assert part1(parse(TEST_TEXT)) == 6


def test_part2():
    assert part2(parse(TEST_TEXT)) == 16


if __name__ == "__main__":
    LINES = parse(get_input(day=19, year=2024))
    print(f"Part 1: {part1(LINES)}")
    print(f"Part 2: {part2(LINES)}")
