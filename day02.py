"""Solution to day 2 of Advent of Code"""

from get_input import get_input, line_parser


def safe(report):
    if report[0] == report[1]:
        return False
    diff = (report[0] - report[1]) / abs(report[0] - report[1])
    for a, b in zip(report, report[1:]):
        if not ((0 < abs(a - b) <= 3) and diff == (a - b) // abs(a - b)):
            return False
    return True


def part1(reports):
    return sum(1 for report in reports if safe(report))


def part2(reports):
    count = 0
    for report in reports:
        if safe(report):
            count += 1
            continue
        for i in range(len(report)):
            mutated = report[:]
            mutated.pop(i)
            if safe(mutated):
                count += 1
                break
    return count


def parse(line):
    return [int(n) for n in line.split(' ')]


TEST_TEXT = """
7 6 4 2 1
1 2 7 8 9
9 7 6 2 1
1 3 2 4 5
8 6 4 4 1
1 3 6 7 9
"""


def test_part1():
    assert part1(line_parser(TEST_TEXT, parse=parse)) == 2


def test_part2():
    assert part2(line_parser(TEST_TEXT, parse=parse)) == 4


if __name__ == "__main__":
    LINES = line_parser(get_input(day=2, year=2024), parse=parse)
    print(f"Part 1: {part1(LINES)}")
    print(f"Part 2: {part2(LINES)}")
