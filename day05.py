"""Solution to day 5 of Advent of Code"""

from get_input import get_input
from collections import defaultdict
from dataclasses import dataclass


@dataclass
class Input:
    page_mapping: dict[int, set[int]]
    updates: list[list[int]]

    def before(self, value: int) -> set[int]:
        return self.page_mapping.get(value, set())


def part1(instructions: Input) -> int:
    total = 0
    for update in instructions.updates:
        all_values = set(update)
        seen = set()
        for value in update:
            if not seen.issuperset(instructions.before(value) & all_values):
                break
            seen.add(value)
        else:
            total += update[len(update) // 2]
    return total


def part2(instructions: Input) -> int:
    total = 0
    for update in instructions.updates:
        all_values = set(update)
        modified = update[:]
        for i in range(len(update)):
            seen = set(modified[:i])
            # Not needed, but faster
            if seen.issuperset(instructions.before(modified[i]) & all_values):
                continue
            for j in range(i+1, len(update)):
                before = instructions.before(update[j])
                if seen.issuperset(before & all_values):
                    modified.insert(i, modified.pop(j))
                    break
        if modified != update:
            total += modified[len(modified) // 2]
    return total


def parse(text: str) -> Input:
    lines = iter(text.strip().splitlines())
    page_mapping = defaultdict(set)
    while (line := next(lines, "").strip()) != "":
        pre, post = line.split("|")
        page_mapping[int(post)].add(int(pre))
    pages = []
    for line in lines:
        pages.append(list(map(int, line.split(","))))
    return Input(page_mapping, pages)


TEST_TEXT = """
47|53
97|13
97|61
97|47
75|29
61|13
75|53
29|13
97|29
53|29
61|53
97|53
61|29
47|13
75|47
97|75
47|61
75|61
47|29
75|13
53|13

75,47,61,53,29
97,61,53,29,13
75,29,13
75,97,47,61,53
61,13,29
97,13,75,29,47
"""


def test_part1():
    assert part1(parse(TEST_TEXT)) == 143


def test_part2():
    assert part2(parse(TEST_TEXT)) == 123


if __name__ == "__main__":
    LINES = parse(get_input(day=5, year=2024))
    print(f"Part 1: {part1(LINES)}")
    print(f"Part 2: {part2(LINES)}")
