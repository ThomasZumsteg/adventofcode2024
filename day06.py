"""Solution to day 6 of Advent of Code"""

from get_input import get_input
from dataclasses import dataclass


@dataclass(frozen=True)
class State:
    position: complex
    heading: complex

    def step(self) -> 'State':
        return State(self.position + self.heading, self.heading)

    def turn_right(self) -> 'State':
        return State(self.position, self.heading * -1j)


@dataclass
class Input:
    mapping: [[str]]
    guard_start: (complex, complex)


def walk(mapping, state):
    while char := mapping.get(state.step().position):
        if char == '#':
            state = state.turn_right()
        else:
            assert char == '.'
            state = state.step()
        yield state


def part1(lines: list[Input]) -> int:
    seen = set([lines.guard_start.position])
    for step in walk(lines.mapping, lines.guard_start):
        seen.add(step.position)
    return len(seen)


def part2(lines: list[Input]) -> int:
    seen = set()
    obstructions = set()
    for step in walk(lines.mapping, lines.guard_start):
        seen.add(step)
        block = step.step().position
        if lines.mapping.get(block) == '.':
            psudo_map = lines.mapping.copy()
            psudo_map[block] = '#'
            psudo_seen = set()
            for psudo_step in walk(psudo_map, lines.guard_start):
                if psudo_step in psudo_seen:
                    assert step.step().position != lines.guard_start.position
                    obstructions.add(step.step().position)
                    break
                psudo_seen.add(psudo_step)
    return len(obstructions)


def parse(text: str) -> Input:
    mapping = {}
    headings = {'^': -1, 'v': 1, '<': -1j, '>': 1j}
    for r, row in enumerate(text.strip().splitlines()):
        for c, char in enumerate(row):
            if char in headings:
                guard_start = State(complex(r, c), headings[char])
                char = '.'
            mapping[complex(r, c)] = char
    return Input(mapping, guard_start)


TEST_TEXT = """
....#.....
.........#
..........
..#.......
.......#..
..........
.#..^.....
........#.
#.........
......#...
"""


def test_part1():
    assert part1(parse(TEST_TEXT)) == 41


def test_part2():
    assert part2(parse(TEST_TEXT)) == 6

if __name__ == "__main__":
    LINES = parse(get_input(day=6, year=2024))
    print(f"Part 1: {part1(LINES)}")
    # NOT 1730, 1791, 1692 (to high)
    print(f"Part 2: {part2(LINES)}")
