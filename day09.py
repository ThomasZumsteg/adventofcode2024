"""Solution to day 9 of Advent of Code"""

from get_input import get_input


Input = int


def part1(layout: list[Input]) -> int:
    expanded = []
    for i, c in enumerate(layout):
        file_no = i // 2
        expanded.extend([file_no if i % 2 == 0 else None] * c)
    i = 0
    while i < len(expanded):
        while expanded[i] is None and i + 1 < len(expanded):
            expanded[i] = expanded.pop()
        i += 1
    return sum(i * (c if c is not None else 0) for i, c in enumerate(expanded))


def part2(layout: list[Input]) -> int:
    expanded = []
    for i, c in enumerate(layout):
        file_no = i // 2
        expanded.extend([file_no if i % 2 == 0 else None] * c)
    i = len(expanded)
    moved = set()
    while i > 0:
        if expanded[i-1] is None or expanded[i-1] in moved:
            i -= 1
            continue
        moved.add(expanded[i-1])
        j = i
        while j > 0 and expanded[j-1] == expanded[i-1]:
            j -= 1
        free = 0
        for k in range(0, j):
            if expanded[k] is None:
                free += 1
            else:
                free = 0
            if free >= i - j:
                for m, n in zip(range(j, i), range(k - free + 1, k + 1)):
                    expanded[n] = expanded[m]
                    expanded[m] = None
                break
    return sum(i * (c if c is not None else 0) for i, c in enumerate(expanded))


def parse(text: str) -> Input:
    return [int(c) for c in list(text.strip())]


TEST_TEXT = """2333133121414131402"""


def test_part1():
    assert part1(parse(TEST_TEXT)) == 1928


def test_part2():
    assert part2(parse(TEST_TEXT)) == 2858


if __name__ == "__main__":
    LINES = parse(get_input(day=9, year=2024))
    print(f"Part 1: {part1(LINES)}")
    print(f"Part 2: {part2(LINES)}")
