"""Solution to day 14 of Advent of Code"""

from get_input import get_input, line_parser
import itertools
import sys
from collections import defaultdict
from dataclasses import dataclass
import re


@dataclass(frozen=True)
class Input:
    position: complex
    velocity: complex

    def step(self) -> 'Input':
        return Input(self.position + self.velocity, self.velocity)

    def normalize(self, size) -> complex:
        partial = complex(self.position.real % size.real, self.position.imag % size.imag)  # noqa: E501
        return partial


def part1(robots: list[Input], size=101+103j, steps=100) -> int:
    display = defaultdict(set)
    for r in robots:
        display[r.normalize(size)].add(r)
    for _ in range(steps):
        next_display = defaultdict(set)
        lines = []
        for c in range(int(size.imag)):
            lines.append([])
            for r in range(int(size.real)):
                robots = display[complex(r, c)]
                if len(robots) == 0:
                    lines[-1].append(' ')
                    continue
                lines[-1].append(str(int(len(robots))))
                for r in robots:
                    r = r.step()
                    next_display[r.normalize(size)].add(r)
        display = next_display
    half = complex(size.real // 2, size.imag // 2)
    quartiles = defaultdict(int)
    for p, robots in display.items():
        if p.real == half.real or p.imag == half.imag:
            continue
        quartiles[(p.real < half.real, p.imag < half.imag)] += len(robots)
    result = 1
    for v in quartiles.values():
        result *= v
    return result


def part2(robots: list[Input], size=101+103j) -> int:
    display = defaultdict(set)
    for r in robots:
        display[r.normalize(size)].add(r)
    for s in itertools.count():
        next_display = defaultdict(set)
        lines = []
        interesting = False
        for c in range(int(size.imag)):
            lines.append([])
            count = 0
            for r in range(int(size.real)):
                robots = display[complex(r, c)]
                if len(robots) == 0:
                    lines[-1].append(' ')
                    count = 0
                    continue
                lines[-1].append('#')
                count += 1
                if count > 10:
                    interesting = True
                for r in robots:
                    r = r.step()
                    next_display[r.normalize(size)].add(r)
        if interesting:
            print("\n".join(''.join(line) for line in lines), file=sys.stderr)
            return s
        display = next_display
    raise NotImplementedError


def parse(line: str) -> Input:
    regex = re.compile(r"p=(-?\d+),(-?\d+) v=(-?\d+),(-?\d+)")
    match = regex.match(line)
    values = [int(n) for n in match.groups()]
    assert len(values) == 4
    return Input(complex(values[0], values[1]), complex(values[2], values[3]))


TEST_TEXT = """p=0,4 v=3,-3
p=6,3 v=-1,-3
p=10,3 v=-1,2
p=2,0 v=2,-1
p=0,0 v=1,3
p=3,0 v=-2,-2
p=7,6 v=-1,-3
p=3,0 v=-1,-2
p=9,3 v=2,3
p=7,3 v=-1,2
p=2,4 v=2,-3
p=9,5 v=-3,-3
"""


def test_part1():
    assert part1(line_parser(TEST_TEXT, parse=parse), size=11+7j) == 12


if __name__ == "__main__":
    LINES = line_parser(get_input(day=14, year=2024), parse=parse)
    print(f"Part 1: {part1(LINES)}")
    print(f"Part 2: {part2(LINES)}")
