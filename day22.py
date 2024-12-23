"""Solution to day 22 of Advent of Code"""

from get_input import get_input, line_parser
from collections import defaultdict, deque
import itertools


def number_gen(seed: int):
    value = seed
    while True:
        yield value
        value ^= (value * 64)
        value %= 16777216
        value ^= (value // 32)
        value %= 16777216
        value ^= (value * 2048)
        value %= 16777216


def part1(secrets: int) -> int:
    sequences = []
    for secret in secrets:
        sequences.append(list(itertools.islice(number_gen(secret), 2001)))
    return sum(s[-1] for s in sequences)


def part2(secrets):
    most_bananas = defaultdict(int)
    for secret in secrets:
        seen = set()
        buff = deque(maxlen=4)
        total = 0
        secret_gen = number_gen(secret)
        n = next(secret_gen)
        while total < 2000:
            n, prev = next(secret_gen), n
            buff.append((n % 10) - (prev % 10))
            if len(buff) < 4:
                continue
            total += 1
            key = tuple(buff)
            if key not in seen:
                seen.add(key)
                most_bananas[key] += n % 10
    return max(most_bananas.values())


TEST_TEXT = """
1
10
100
2024
"""


TEST_TEXT_2 = """
1
2
3
2024
"""


def test_part1():
    assert part1(line_parser(TEST_TEXT, parse=int)) == 37327623


def test_part2():
    assert part2(line_parser(TEST_TEXT_2, parse=int)) == 23


if __name__ == "__main__":
    LINES = line_parser(get_input(day=22, year=2024), parse=int)
    print(f"Part 1: {part1(LINES)}")
    print(f"Part 2: {part2(LINES)}")
