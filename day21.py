"""Solution to day 21 of Advent of Code"""

from get_input import get_input, line_parser
from dataclasses import dataclass, field


Input = str


class Pad:
    def move(self, direction):
        if self.pos + direction not in self.pad:
            return None
        return type(self)(self.pos + direction)

    def press(self) -> str:
        return self.pad[self.pos]

    def __hash__(self):
        return hash(self.pos)

    def __repr__(self):
        return f"{self.__class__.__name__}(pos={self.pad.get(self.pos)})"

    def __eq__(self, other):
        return self.pos == other.pos


class NumberPad(Pad):
    pad: dict[complex, str] = {
        0+0j: "7", 0+1j: "8", 0+2j: "9",
        1+0j: "4", 1+1j: "5", 1+2j: "6",
        2+0j: "1", 2+1j: "2", 2+2j: "3",
                   3+1j: "0", 3+2j: "A",  # noqa
    }

    def __init__(self, pos=3+2j):
        self.pos = pos


class DirectionPad(Pad):
    pad: dict[complex, str] = {
                   0+1j: "^", 0+2j: "A",
        1+0j: "<", 1+1j: "v", 1+2j: ">",  # noqa
    }

    def __init__(self, pos=0+2j):
        self.pos = pos


@dataclass
class State:
    pads: list[Pad]
    code: str
    moves: str = ''

    def __hash__(self):
        return hash(sum(hash(p) for p in self.pads) + hash(self.code))

    def __eq__(self, other):
        return self.pads == other.pads and self.code == other.code

    def press(self, key: str) -> 'State':
        new_moves = self.moves + key
        directions = {">": 1j, "<": -1j, "^": -1, "v": 1}
        for depth in range(len(self.pads)):
            if key == 'A':
                key = self.pads[depth].press()
                continue
            assert key in directions
            if update := self.pads[depth].move(directions[key]):
                new_state = State(
                    self.pads[:depth] + [update] + self.pads[depth+1:],
                    self.code,
                    new_moves,
                )
                # if depth > 0:
                #     print(self)
                #     print(new_state)
                #     breakpoint()
                return new_state
            return None
        return State(self.pads, self.code + key, new_moves)


def part1(codes: list[Input]) -> int:
    total = 0
    for code in codes:
        pads = [DirectionPad() for _ in range(2)] + [NumberPad()]
        queue = [State(pads, '')]
        seen = set()
        while queue:
            state = queue.pop()
            if state in seen:
                continue
            seen.add(state)
            if state.code == code:
                total += len(state.moves) * int(code.strip("A"))
                break
            if not code.startswith(state.code):
                continue
            for key in ['^', 'v', '>', '<', 'A']:
                if update := state.press(key):
                    queue.append(update)
                    queue.sort(key=lambda x: -len(x.moves))
    return total


def part2(codes: Input) -> int:
    total = 0
    for code in codes:
        pads = [DirectionPad() for _ in range(25)] + [NumberPad()]
        print(code)
        queue = [State(pads, '')]
        seen = set()
        while queue:
            state = queue.pop()
            print(len(queue), end='\r')
            if state in seen:
                continue
            seen.add(state)
            if state.code == code:
                total += len(state.moves) * int(code.strip("A"))
                break
            if not code.startswith(state.code):
                continue
            for key in ['^', 'v', '>', '<', 'A']:
                if update := state.press(key):
                    queue.append(update)
    return total


TEST_TEXT = """
029A
980A
179A
456A
379A
"""


def test_part1():
    assert part1(line_parser(TEST_TEXT, parse=str)) == 126384


if __name__ == "__main__":
    LINES = line_parser(get_input(day=21, year=2024), parse=str)
    print(f"Part 1: {part1(LINES)}")
    print(f"Part 2: {part2(LINES)}")
