"""Solution to day 23 of Advent of Code"""

from get_input import get_input, line_parser
from collections import defaultdict
import itertools


Input = tuple[str, str]


def part1(connections: list[Input]) -> int:
    networks = defaultdict(set)
    for src, dst in connections:
        networks[src].add(dst)
        networks[dst].add(src)
    seen = set()
    for a, values in networks.items():
        for b, c in itertools.combinations(values, 2):
            if c in networks.get(b, set()):
                key = tuple(sorted([a, b, c]))
                seen.add(key)
    return sum(1 for network in seen if any(n[0] == 't' for n in network))


def part2(connections: list[Input]) -> str:
    networks = defaultdict(set)
    for src, dst in connections:
        networks[src].add(dst)
        networks[dst].add(src)
    seen = set()
    for a, values in networks.items():
        done = False
        for lenth in reversed(range(len(values))):
            for other in itertools.combinations(values, lenth):
                if all(c in networks.get(b, set()) for b, c in itertools.combinations(other, 2)):
                    seen.add(','.join(sorted([a, *other])))
                    done = True
                    break
            if done:
                break
    return max(seen, key=lambda x: len(x))


def parse(text) -> list[int]:
    return tuple(text.strip().split('-'))


TEST_TEXT = """
kh-tc
qp-kh
de-cg
ka-co
yn-aq
qp-ub
cg-tb
vc-aq
tb-ka
wh-tc
yn-cg
kh-ub
ta-co
de-co
tc-td
tb-wq
wh-td
ta-ka
td-qp
aq-cg
wq-ub
ub-vc
de-ta
wq-aq
wq-vc
wh-yn
ka-de
kh-ta
co-tc
wh-qp
tb-vc
td-yn
"""


def test_part1():
    assert part1(line_parser(TEST_TEXT, parse=parse)) == 7


def test_part2():
    assert part2(line_parser(TEST_TEXT, parse=parse)) == 'co,de,ka,ta'


if __name__ == "__main__":
    LINES = line_parser(get_input(day=23, year=2024), parse=parse)
    print(f"Part 1: {part1(LINES)}")
    print(f"Part 2: {part2(LINES)}")
