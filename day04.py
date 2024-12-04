"""Solution to day 4 of Advent of Code"""

from get_input import get_input, line_parser


INPUT = dict[complex, str]


def part1(lines: list[INPUT]) -> int:
    word = "XMAS"
    count = 0
    for pos, char in lines.items():
        for step in [1-1j, 1, 1+1j, 1j, -1j, -1-1j, -1, -1+1j]:
            if all(lines.get(pos + step * i) == word[i] for i in range(len(word))):
                count += 1
    return count


def part2(lines: list[INPUT]) -> int:
    count = 0
    for pos, char in lines.items():
        if char != "A":
            continue
        positions = [1+1j, 1-1j, -1-1j, -1+1j]
        for r in range(4):
            rotation = [lines.get(pos + p) for p in positions[r:] + positions[:r]]
            if rotation == ["M", "M", "S", "S"]:
                count += 1
                break
    return count


def parse(text: str) -> INPUT:
    result = {}
    for r, line in enumerate(text.strip().split('\n')):
        for c, char in enumerate(line):
            result[complex(r, c)] = char
    return result


TEST_TEXT = """
MMMSXXMASM
MSAMXMSMSA
AMXSXMAAMM
MSAMASMSMX
XMASAMXAMM
XXAMMXXAMA
SMSMSASXSS
SAXAMASAAA
MAMMMXMMMM
MXMXAXMASX
"""


def test_part1():
    assert part1(parse(TEST_TEXT)) == 18


def test_part2():
    assert part2(parse(TEST_TEXT)) == 9


if __name__ == "__main__":
    LINES = parse(get_input(day=4, year=2024))
    print(f"Part 1: {part1(LINES)}")
    print(f"Part 2: {part2(LINES)}")
