"""Solution to day 7 of Advent of Code"""

from get_input import get_input, line_parser
import operator


Input = tuple[int, list[int]]


def valid(target: int, values: list[int], operators: list) -> bool:
    queue = [(values[0], values[1:])]
    while queue:
        current, vals = queue.pop()
        if current == target and vals == []:
            return True
        if current > target or vals == []:
            continue
        for op in operators:
            queue.append((op(current, vals[0]), vals[1:]))
    return False


def part1(lines: list[Input]) -> int:
    return sum(target for target, values in lines
               if valid(target, values, [operator.add, operator.mul]))


def part2(lines: list[Input]) -> int:
    operators = [operator.add, operator.mul, lambda a, b: int(str(a) + str(b))]
    return sum(target for target, values in lines
               if valid(target, values, operators))


def parse(line: str) -> Input:
    left, right = line.strip().split(": ", 1)
    return (int(left), list(map(int, right.split(' '))))


TEST_TEXT = """
190: 10 19
3267: 81 40 27
83: 17 5
156: 15 6
7290: 6 8 6 15
161011: 16 10 13
192: 17 8 14
21037: 9 7 18 13
292: 11 6 16 20
"""


def test_part1():
    assert part1(line_parser(TEST_TEXT.strip(), parse=parse)) == 3749


def test_part2():
    assert part2(line_parser(TEST_TEXT, parse=parse)) == 11387


if __name__ == "__main__":
    LINES = line_parser(get_input(day=7, year=2024), parse=parse)
    print(f"Part 1: {part1(LINES)}")
    print(f"Part 2: {part2(LINES)}")
