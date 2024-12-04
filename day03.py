"""Solution to day 3 of Advent of Code"""

from get_input import get_input
import re


def part1(line: str) -> int:
    assert isinstance(line, str)
    return sum(
        int(a) * int(b) for (a, b) in
        re.findall(r'mul\((\d+),(\d+)\)', line)
    )


def part2(lines: str) -> int:
    state = "do"
    total = 0
    for m in re.finditer(r"(mul\((\d+),(\d+)\)|don't\(\)|do\(\))", lines):
        match m.group(1)[:m.group(1).find("(")]:
            case "mul" if state == "do":
                total += int(m.group(2)) * int(m.group(3))
            case "don't" | "do" as oper:
                state = oper
            case _:
                assert state == "don't" and m.group(1).startswith("mul("), \
                    f"state={state}, m.group(1)={m.group(1)}"
    return total


def test_part1():
    test_text = """
    xmul(2,4)%&mul[3,7]!@^do_not_mul(5,5)+mul(32,64]then(mul(11,8)mul(8,5))
    """
    assert part1(test_text) == 161


def test_part2():
    test_text = """
    xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))
    """
    assert part2(test_text) == 48


if __name__ == "__main__":
    LINES = get_input(day=3, year=2024)
    print(f"Part 1: {part1(LINES)}")
    print(f"Part 2: {part2(LINES)}")
