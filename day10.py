"""Solution to day 10 of Advent of Code"""

from get_input import get_input


Input = int


def part1(mapping: list[Input]) -> int:
    trailheads = [n for n, c in mapping.items() if c == 0]
    total = 0
    for trailhead in trailheads:
        stack = [trailhead]
        ends = set()
        while stack:
            pos = stack.pop()
            if mapping[pos] == 9:
                ends.add(pos)
                continue
            for step in [1, 1j, -1, -1j]:
                next_pos = pos + step
                if next_pos not in mapping:
                    continue
                if mapping[next_pos] == mapping[pos] + 1:
                    stack.append(next_pos)
        total += len(ends)
    return total


def part2(mapping: list[Input]) -> int:
    trailheads = [n for n, c in mapping.items() if c == 0]
    total = 0
    for trailhead in trailheads:
        stack = [trailhead]
        subtotal = 0
        while stack:
            pos = stack.pop()
            if mapping[pos] == 9:
                subtotal += 1
                continue
            for step in [1, 1j, -1, -1j]:
                next_pos = pos + step
                if next_pos not in mapping:
                    continue
                if mapping[next_pos] == mapping[pos] + 1:
                    stack.append(next_pos)
        total += subtotal
    return total


def parse(line: str) -> Input:
    mapping = {}
    for r, row in enumerate(line.strip().splitlines()):
        for c, char in enumerate(row):
            assert char in "0123456789"
            mapping[complex(r, c)] = int(char)
    return mapping


TEST_TEXT = """
89010123
78121874
87430965
96549874
45678903
32019012
01329801
10456732
"""


def test_part1():
    assert part1(parse(TEST_TEXT)) == 36


def test_part2():
    assert part2(parse(TEST_TEXT)) == 81


if __name__ == "__main__":
    LINES = parse(get_input(day=10, year=2024))
    print(f"Part 1: {part1(LINES)}")
    print(f"Part 2: {part2(LINES)}")
