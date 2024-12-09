"""Solution to day 8 of Advent of Code"""

from get_input import get_input
import itertools
from collections import defaultdict
from dataclasses import dataclass


@dataclass
class Input:
    points: dict[complex, str]
    nodes: dict[str, set[complex]]


def part1(mapping: list[Input]) -> int:
    anitnodes = set()
    for node, points in mapping.nodes.items():
        for left, right in itertools.permutations(points, 2):
            anitnode = 2 * left - right
            if anitnode in mapping.points:
                anitnodes.add(anitnode)
    return len(anitnodes)


def part2(mapping: list[Input]) -> int:
    anitnodes = set()
    for node, points in mapping.nodes.items():
        for left, right in itertools.permutations(points, 2):
            diff = left - right
            anitnode = left
            while anitnode in mapping.points:
                anitnodes.add(anitnode)
                anitnode += diff
    return len(anitnodes)


def parse(text: str) -> Input:
    points = {}
    nodes = defaultdict(set)
    for r, row in enumerate(text.strip().splitlines()):
        for c, char in enumerate(row):
            point = complex(r, c)
            if char != '.':
                nodes[char].add(point)
            points[point] = '.'
    return Input(points, nodes)


TEST_TEXT = """
............
........0...
.....0......
.......0....
....0.......
......A.....
............
............
........A...
.........A..
............
............
"""


TEST_TEXT_2 = """
T.........
...T......
.T........
..........
..........
..........
..........
..........
..........
..........
"""


def test_part1():
    assert part1(parse(TEST_TEXT)) == 14


def test_simple_part2():
    assert part2(parse(TEST_TEXT_2)) == 9


def test_part2():
    assert part2(parse(TEST_TEXT)) == 34


if __name__ == "__main__":
    LINES = parse(get_input(day=8, year=2024))
    print(f"Part 1: {part1(LINES)}")
    print(f"Part 2: {part2(LINES)}")
