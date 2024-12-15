"""Solution to day 15 of Advent of Code"""

from get_input import get_input, line_parser
from dataclasses import dataclass


@dataclass
class Input:
    start: complex
    mapping: dict[complex, str]
    moves: list[complex]

    def remap(self) -> 'Input':
        remap = {}
        for p, char in self.mapping.items():
            match char:
                case 'O':
                    replace = '[]'
                case '#':
                    replace = '##'
                case _:
                    raise ValueError(f"Unknown char {char}")
            remap[complex(p.real, 2 * p.imag)] = replace[0]
            remap[complex(p.real, 2 * p.imag + 1)] = replace[1]
        start = complex(self.start.real, 2 * self.start.imag)
        return Input(start, remap, self.moves)


def part1(state: list[Input]) -> int:
    position = state.start
    mapping = state.mapping.copy()
    for move in state.moves:
        step = position + move
        while mapping.get(step) == 'O':
            step += move
        if mapping.get(step) is None:
            mapping[step] = 'O'
            position += move
            del mapping[position]
    total = 0
    for p, char in mapping.items():
        if char != "O":
            continue
        total += int(100 * p.real + p.imag)
    return total


def part2(state: list[Input]) -> int:
    restate = state.remap()
    mapping = restate.mapping.copy()
    position = restate.start
    for move in restate.moves:
        queue = [position + move]
        to_move = set()
        clear = True
        while queue:
            pos = queue.pop()
            if pos in to_move:
                continue
            match mapping.get(pos):
                case '#':
                    clear = False
                    break
                case '[' | ']' as c:
                    to_move.add(pos)
                    queue.append(pos + (1j if c == '[' else -1j))
                    queue.append(pos + move)
                case None:
                    continue
                case c:
                    raise ValueError(f"Unknown char {c}")
        if clear:
            position += move
            while to_move:
                pos = to_move.pop()
                if pos + move in to_move:
                    to_move.add(pos)
                    continue
                mapping[pos + move] = mapping[pos]
                del mapping[pos]

        # print()
        # print(move)
        # for r in range(7):
        #     for c in range(2*7):
        #         if complex(r, c) == position:
        #             print('@', end="")
        #         else:
        #             print(mapping.get(complex(r, c), "."), end="")
        #     print()
        # breakpoint()
    total = 0
    for p, char in mapping.items():
        if char != "[":
            continue
        total += int(100 * p.real + p.imag)
    return total


def parse(text: str) -> Input:
    lines = iter(text.strip().splitlines())
    mapping = {}
    r = 0
    while (row := next(lines).strip()) != "":
        for c, char in enumerate(row):
            if char == "@":
                char = "."
                start = complex(r, c)
            if char != ".":
                mapping[complex(r, c)] = char
        r += 1
    moves = []
    for line in lines:
        for char in line:
            match char:
                case "^":
                    move = -1
                case "v":
                    move = 1
                case "<":
                    move = -1j
                case ">":
                    move = 1j
            moves.append(move)
    return Input(start, mapping, moves)


TEST_TEXT = """########
#..O.O.#
##@.O..#
#...O..#
#.#.O..#
#...O..#
#......#
########

<^^>>>vv<v>>v<<
"""


TEST_TEXT_2 = """
##########
#..O..O.O#
#......O.#
#.OO..O.O#
#..O@..O.#
#O#..O...#
#O..O..O.#
#.OO.O.OO#
#....O...#
##########

<vv>^<v^>v>^vv^v>v<>v^v<v<^vv<<<^><<><>>v<vvv<>^v^>^<<<><<v<<<v^vv^v>^
vvv<<^>^v^^><<>>><>^<<><^vv^^<>vvv<>><^^v>^>vv<>v<<<<v<^v>^<^^>>>^<v<v
><>vv>v^v^<>><>>>><^^>vv>v<^^^>>v^v^<^^>v^^>v^<^v>v<>>v^v^<v>v^^<^^vv<
<<v<^>>^^^^>>>v^<>vvv^><v<<<>^^^vv^<vvv>^>v<^^^^v<>^>vvvv><>>v^<<^^^^^
^><^><>>><>^^<<^^v>>><^<v>^<vv>>v>>>^v><>^v><<<<v>>v<v<v>vvv>^<><<>^><
^>><>^v<><^vvv<^^<><v<<<<<><^v<<<><<<^^<v<^^^><^>>^<v^><<<^>>^v<v^v<v^
>^>>^v>vv>^<<^v<>><<><<v<<v><>v<^vv<<<>^^v^>^^>>><<^v>>v^v><^^>>^<>vv^
<><^^>^^^<><vvvvv^v<v<<>^v<v>v<<^><<><<><<<^^<<<^<<>><<><^^^>^^<>^>v<>
^^>vv<^v^v<vv>^<><v<^v>^^^>>>^^vvv^>vvv<>>>^<^>>>>>^<<^v>^vvv<>^<><<v>
v^^>>><<^^<>>^v^<v^vv<>v^<<>^<^v^v><^<<<><<^<v><v<>vv>>v><v^<vv<>v^<<^
"""


TEST_TEXT_3 = """
#######
#...#.#
#.....#
#..OO@#
#..O..#
#.....#
#######

<vv<<^^<<^^
"""


def test_part1():
    assert part1(parse(TEST_TEXT)) == 2028
    assert part1(parse(TEST_TEXT_2)) == 10092


def test_part2():
    # assert part2(parse(TEST_TEXT_3)) == 0
    assert part2(parse(TEST_TEXT_2)) == 9021


if __name__ == "__main__":
    LINES = parse(get_input(day=15, year=2024))
    print(f"Part 1: {part1(LINES)}")
    print(f"Part 2: {part2(LINES)}")
