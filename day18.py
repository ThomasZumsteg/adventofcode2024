"""Solution to day 18 of Advent of Code"""

import itertools
from get_input import get_input, line_parser
from dataclasses import dataclass

Input = complex


@dataclass
class State:
    pass


def part1(corrupt: list[Input], size=70, limit=1024) -> int:
    mapping = {c: "#" for c in corrupt[:limit]}
    stage = [0+0j]
    end = complex(size, size)
    seen = set()
    for steps in itertools.count(0):
        next_stage = []
        for node in stage:
            if node in seen or mapping.get(node) == '#' or \
                    not (size >= node.real >= 0 and size >= node.imag >= 0):
                continue
            seen.add(node)
            if node == end:
                return steps
            for step in [1, -1, 1j, -1j]:
                next_stage.append(node + step)
        if next_stage == []:
            return None
        stage = next_stage


def part2(corrupt: list[Input], size=70) -> str:
    start, end = 0, len(corrupt)
    while start < end:
        mid = (start + end) // 2
        if part1(corrupt, size=size, limit=mid) is not None:
            start = mid + 1
        else:
            end = mid
    point = corrupt[start - 1]
    return f"{int(point.real)},{int(point.imag)}"


def parse(text: str) -> Input:
    a, b = text.split(',')
    return complex(int(a), int(b))


TEST_TEXT = """
5,4
4,2
4,5
3,0
2,1
6,3
2,4
1,5
0,6
3,3
2,6
5,1
1,2
5,5
2,5
6,5
1,4
0,4
6,4
1,1
6,1
1,0
0,5
1,6
2,0
"""


def test_part1():
    assert part1(line_parser(TEST_TEXT, parse=parse), size=6, limit=12) == 22


def test_part2():
    assert part2(line_parser(TEST_TEXT, parse=parse), size=6) == "6,1"


if __name__ == "__main__":
    LINES = line_parser(get_input(day=18, year=2024), parse=parse)
    print(f"Part 1: {part1(LINES)}")
    print(f"Part 2: {part2(LINES)}")
