"""Solution to day 12 of Advent of Code"""

from get_input import get_input


Input = int


def part1(plants: list[Input]) -> int:
    seen = set()
    total = 0
    for point, plant in plants.items():
        if point in seen:
            continue
        queue = [point]
        area = set()
        perimeter = 0
        while queue:
            point = queue.pop()
            if point in area:
                continue
            area.add(point)
            for step in [1, 1j, -1, -1j]:
                next_point = point + step
                if plants.get(next_point) == plant:
                    queue.append(next_point)
                else:
                    perimeter += 1
        seen.update(area)
        total += len(area) * perimeter
    return total


def part2(plants: list[Input]) -> int:
    seen = set()
    total = 0
    for point, plant in plants.items():
        if point in seen:
            continue
        area = set()
        edge_spaces = set()
        queue = [point]
        while queue:
            point = queue.pop()
            if point in area:
                continue
            area.add(point)
            for step in [1, 1j, -1, -1j]:
                next_point = point + step
                if plants.get(next_point) == plant:
                    queue.append(next_point)
                else:
                    edge_spaces.add((point, step))
        seen.update(area)
        edges = 0
        # Left turns
        # 1 -> 1j -> -1 -> -1j
        # v -> >  -> ^  -> <
        while edge_spaces:
            point, step = edge_spaces.pop()
            edges += 1
            for side in (1j, -1j):
                step_point = point + (side * step)
                while (step_point, step) in edge_spaces:
                    edge_spaces.remove((step_point, step))
                    step_point += (side * step)
        total += len(area) * edges
    return total


def parse(text: str) -> dict[str, complex]:
    result = {}
    for r, row in enumerate(text.strip().splitlines()):
        for c, char in enumerate(row):
            result[complex(r, c)] = char
    return result


TEST_TEXT = """
RRRRIICCFF
RRRRIICCCF
VVRRRCCFFF
VVRCCCJFFF
VVVVCJJCFE
VVIVCCJJEE
VVIIICJJEE
MIIIIIJJEE
MIIISIJEEE
MMMISSJEEE
"""

TEST_TEXT_2 = """
AAAA
BBCD
BBCC
EEEC
"""

TEST_TEXT_3 = """
EEEEE
EXXXX
EEEEE
EXXXX
EEEEE
"""


TEST_TEXT_4 = """
AAAAAA
AAABBA
AAABBA
ABBAAA
ABBAAA
AAAAAA
"""


def test_part1():
    assert part1(parse(TEST_TEXT)) == 1930


def test_part2():
    assert part2(parse(TEST_TEXT)) == 1206
    assert part2(parse(TEST_TEXT_2)) == 80
    assert part2(parse(TEST_TEXT_3)) == 236
    assert part2(parse(TEST_TEXT_4)) == 368


if __name__ == "__main__":
    LINES = parse(get_input(day=12, year=2024))
    print(f"Part 1: {part1(LINES)}")
    print(f"Part 2: {part2(LINES)}")
