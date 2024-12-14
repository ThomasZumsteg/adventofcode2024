"""Solution to day 13 of Advent of Code"""

from get_input import get_input, line_parser
import re
from dataclasses import dataclass


@dataclass
class Input:
    button_a: complex
    button_b: complex
    target: complex

    def scale(self, scale: complex) -> 'Input':
        return Input(
            self.button_a,
            self.button_b,
            self.target + scale
        )


def part1(games: list[Input], scale=0+0j) -> int:
    tokens = 0
    for game in games:
        ratio = game.button_a.imag / game.button_a.real
        presses_b = round(
            (game.target.imag - ratio * game.target.real) /
            (game.button_b.imag - ratio * game.button_b.real)
        )
        presses_a = round(
            (game.target.real - game.button_b.real * presses_b) /
            game.button_a.real
        )
        if presses_a * game.button_a + presses_b * game.button_b == game.target:  # noqa: E501
            tokens += int(3 * round(presses_a) + round(presses_b))
    return tokens


def part2(games: list[Input]) -> int:
    return part1([game.scale(10000000000000*(1+1j)) for game in games])


def parse(text: str) -> Input:
    regex = re.compile(
        r"Button A: X\+(\d+), Y\+(\d+)\n"
        r"Button B: X\+(\d+), Y\+(\d+)\n"
        r"Prize: X=(\d+), Y=(\d+)"
    )
    match = regex.match(text)
    values = [int(n) for n in match.groups()]
    assert len(values) == 6
    return Input(
        complex(*values[:2]),
        complex(*values[2:4]),
        complex(*values[4:])
    )


TEST_TEXT = """
Button A: X+94, Y+34
Button B: X+22, Y+67
Prize: X=8400, Y=5400

Button A: X+26, Y+66
Button B: X+67, Y+21
Prize: X=12748, Y=12176

Button A: X+17, Y+86
Button B: X+84, Y+37
Prize: X=7870, Y=6450

Button A: X+69, Y+23
Button B: X+27, Y+71
Prize: X=18641, Y=10279
"""


def test_part1():
    assert part1(line_parser(TEST_TEXT, seperator='\n\n', parse=parse)) == 480


if __name__ == "__main__":
    LINES = line_parser(get_input(day=13, year=2024), seperator='\n\n', parse=parse)  # noqa: E501
    print(f"Part 1: {part1(LINES)}")
    print(f"Part 2: {part2(LINES)}")
