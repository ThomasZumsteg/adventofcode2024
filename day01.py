"""Solution to day 1 of Advent of Code"""

from get_input import get_input, line_parser
from collections import Counter


def part1(rows):
    left = sorted([r[0] for r in rows])
    right = sorted([r[1] for r in rows])
    return sum(abs(l - r) for l, r in zip(left, right))


def part2(rows):
    left = [r[0] for r in rows]
    counts = Counter([r[1] for r in rows])
    return sum(l * counts[l] for l in left)


def parse(line):
    left, right = line.split(' ', 1)
    return (int(left.strip()), int(right.strip()))


TEST1 = """
3   4
4   3
2   5
1   3
3   9
3   3
"""


def test_part1():
    assert part1(line_parser(TEST1, parse=parse)) == 11


def test_part2():
    assert part2(line_parser(TEST1, parse=parse)) == 31


if __name__ == "__main__":
    LINES = line_parser(get_input(day=1, year=2024), parse=parse)
    print(f"Part 1: {part1(LINES)}")
    print(f"Part 2: {part2(LINES)}")
