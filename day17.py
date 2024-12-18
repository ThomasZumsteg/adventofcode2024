"""Solution to day 16 of Advent of Code"""

from get_input import get_input, line_parser
import itertools
from collections import defaultdict
from dataclasses import dataclass


@dataclass(frozen=True)
class Input:
    registers: tuple[int]
    program: list[int]


@dataclass
class State:
    registers: list[int]
    pointer: int

    def process(self, code: int, oper: None | int) -> int | None:
        match code:
            case 0:  # adv
                self.registers[0] = self.reg("A") // (2 ** self.combo(oper))
            case 1:  # bxl
                self.registers[1] = self.reg("B") ^ oper
            case 2:  # bst
                self.registers[1] = self.combo(oper) % 8
            case 3:  # jnz
                if self.registers[0] != 0:
                    self.pointer = oper - 2
            case 4:
                self.registers[1] = self.reg('B') ^ self.reg('C')
            case 5:
                output = self.combo(oper) % 8
                self.pointer += 2
                return output
            case 6:
                self.registers[1] = self.reg("A") // 2 ** self.combo(oper)
            case 7:
                self.registers[2] = self.reg("A") // 2 ** self.combo(oper)
            case _:
                raise ValueError(f"Unknown code {code}")
        self.pointer += 2
        return

    def reg(self, r: str) -> int:
        assert r in "ABC"
        return self.registers[ord(r) - ord("A")]

    def combo(self, code: int | str) -> int:
        match code:
            case 0 | 1 | 2 | 3 as n:
                return n
            case 4 | 5 | 6 as n:
                return self.registers[n - 4]
            case _:
                raise ValueError(f"Unknown code {code}")

    def freeze(self) -> (int, tuple[int]):
        return (self.pointer, tuple(self.registers))


def part1(start: Input) -> int:
    state = State(list(start.registers), 0)
    output = []
    while 0 <= state.pointer < len(start.program):
        code = start.program[state.pointer]
        oper = start.program[state.pointer + 1]
        if (out := state.process(code, oper)) is not None:
            output.append(out)
    return ','.join(map(str, output))


def part2(start: Input) -> int:
    """
    2,4, # B = A % 8
    1,2, # B = B ^ 2
    7,5, # C = A // 2 ** B
    1,3, # B = B ^ 3
    4,4, # B = B ^ C
    5,5,  # out (B)
    0,3, # A = A // 2 ** 3
    3,0   # jnz
    """
    options = {0}
    required = []

    def run(reg_a: int) -> list[int]:
        output = []
        state = State([reg_a, 0, 0], 0)
        while 0 <= state.pointer < len(start.program):
            code = start.program[state.pointer]
            oper = start.program[state.pointer + 1]
            if (out := state.process(code, oper)) is not None:
                output.append(out)
        return output

    def solve(reg_a: int, required: list[int]):
        reg_a *= 8
        for n in range(8):
            output = run(reg_a + n)
            if output == required:
                yield reg_a + n

    for value in reversed(start.program):
        required.insert(0, value)
        options = {a for option in options for a in solve(option, required)}

    return min(options)


def parse(text: str) -> Input:
    lines = iter(text.strip().splitlines())
    registers = []
    while (line := next(lines)) != "":
        registers.append(int(line.split(':')[-1].strip()))
    assert len(registers) == 3
    program = [int(n) for n in next(lines).split(':')[-1].strip().split(',')]
    return Input(tuple(registers), program)


TEST_TEXT = """
Register A: 729
Register B: 0
Register C: 0

Program: 0,1,5,4,3,0
"""

TEST_TEXT_2 = """
Register A: 2024
Register B: 0
Register C: 0

Program: 0,3,5,4,3,0
"""


def test_part1():
    state = State([0, 0, 9], 0)
    state.process(2, 6)
    assert state.reg('C') == 9

    assert part1(Input([10, 0, 0], [5, 0, 5, 1, 5, 4])) == "0,1,2"

    assert part1(Input([2024, 0, 0], [0, 1, 5, 4, 3, 0])) == \
        "4,2,5,6,7,7,7,7,3,1,0"

    state = State([0, 29, 0], 0)
    state.process(1, 7)
    assert state.reg('B') == 26

    state = State([0, 2024, 43690], 0)
    state.process(4, 0)
    assert state.reg('B') == 44354

    assert part1(parse(TEST_TEXT)) == "4,6,3,5,6,3,5,2,1,0"


def test_part2():
    assert part2(parse(TEST_TEXT_2)) == 117440


if __name__ == "__main__":
    LINES = parse(get_input(day=17, year=2024))
    # NOT 4,5,7,5,5,6,0,6,3
    print(f"Part 1: {part1(LINES)}")
    print(f"Part 2: {part2(LINES)}")
