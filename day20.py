"""Solution to day 20 of Advent of Code"""

from get_input import get_input, line_parser
from dataclasses import dataclass, field
from collections.abc import Generator
from collections import defaultdict


@dataclass
class Input:
    racetrack: dict[complex, str]
    start: complex
    end: complex


@dataclass(frozen=True)
class State:
    pos: complex
    steps: tuple[complex] = field(default_factory=tuple)
    cheats: tuple[complex] = field(default_factory=tuple)

    def __eq__(self, other):
        return self.pos == other.pos

    def moves(self) -> Generator['State']:
        for direction in [1, -1, 1j, -1j]:
            step = self.pos + direction
            yield State(step, self.steps + (step,), self.cheats)

    def __hash__(self):
        return hash(self.pos) + hash(len(self.cheats))


def part1(racetrack: Input, cheat_limit: int = 2, limit: int = 100) -> int:
    queue = [State(racetrack.start, (racetrack.start,))]
    seen = set()
    track = racetrack.racetrack
    while queue:
        state = queue.pop(0)
        if state.pos == racetrack.end:
            path = state.steps
            break
        if state in seen:
            continue
        seen.add(state)
        for move in state.moves():
            if track.get(move.pos) != '.':
                continue
            queue.append(move)
    saves = defaultdict(set)
    cheats = set()
    path_dict = {step: i for i, step in enumerate(path)}
    for s, start in enumerate(path):
        print(f"{s}/{len(path)}")
        queue = [(0, start)]
        seen = set()
        while queue:
            cheat_count, step = queue.pop(0)
            if cheat_count > cheat_limit:
                continue
            if step in seen or track.get(step) is None:
                continue
            seen.add(step)
            cheat = (start, step)
            if step in path_dict and cheat not in cheats:
                saved = path_dict[step] - s - cheat_count
                saves[saved].add(cheat)
                cheats.add(cheat)
            for direction in [1, -1, 1j, -1j]:
                queue.append((cheat_count + 1, step + direction))

    total = 0
    for s, vs in sorted(saves.items(), key=lambda x: x[0]):
        if s >= limit:
            total += len(vs)
    return total


def part2(start: Input) -> int:
    return part1(start, cheat_limit=20, limit=100)


def parse(text: str) -> Input:
    racetrack = {}
    for r, row in enumerate(text.strip().split('\n')):
        for c, char in enumerate(row):
            if char == 'S':
                start = complex(r, c)
                char = '.'
            elif char == 'E':
                end = complex(r, c)
                char = '.'
            assert char in '.#'
            racetrack[complex(r, c)] = char
    return Input(racetrack, start, end)


TEST_TEXT = """
###############
#...#...#.....#
#.#.#.#.#.###.#
#S#...#.#.#...#
#######.#.#.###
#######.#.#...#
#######.#.###.#
###..E#...#...#
###.#######.###
#...###...#...#
#.#####.#.###.#
#.#...#.#.#...#
#.#.#.#.#.#.###
#...#...#...###
###############
"""


def test_part1():
    assert part1(parse(TEST_TEXT), limit=12) == 8
    assert part1(parse(TEST_TEXT), limit=10) == 10
    assert part1(parse(TEST_TEXT), limit=8) == 14


def test_part2():
    assert part1(parse(TEST_TEXT), cheat_limit=20, limit=76) == 3
    assert part1(parse(TEST_TEXT), cheat_limit=20, limit=74) == 7
    assert part1(parse(TEST_TEXT), cheat_limit=20, limit=72) == 7 + 22
    assert part1(parse(TEST_TEXT), cheat_limit=20, limit=70) == 7 + 22 + 12
    assert part1(parse(TEST_TEXT), cheat_limit=20, limit=68) == 7 + 22 + 12 + 14


if __name__ == "__main__":
    LINES = parse(get_input(day=20, year=2024))
    print(f"Part 1: {part1(LINES)}")
    print(f"Part 2: {part2(LINES)}")
