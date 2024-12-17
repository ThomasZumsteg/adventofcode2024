"""Solution to day 15 of Advent of Code"""

from get_input import get_input, line_parser
from dataclasses import dataclass, field
import heapq


@dataclass
class Input:
    maze: dict[complex, str]
    start: dict[complex, str]
    end: dict[complex, str]


@dataclass(frozen=True)
class Node:
    score: int
    pos: complex
    heading: complex
    path: list[complex] = field(default_factory=list)

    def __lt__(self, other):
        return self.score < other.score

    def step(self) -> 'Node':
        return Node(self.score + 1, self.pos + self.heading, self.heading, self.path + [self.pos])

    def turn(self, direction: complex) -> 'Node':
        return Node(self.score + 1000, self.pos, direction * self.heading, self.path + [self.pos])

    @property
    def state(self) -> tuple[complex, complex]:
        return (self.pos, self.heading)


def part1(state: Input) -> int:
    queue = [Node(0, state.start, 1j)]
    min_score = None
    seen = {}
    while queue:
        node = heapq.heappop(queue)
        if seen.get(node.state, node.score) < node.score:
            continue
        seen[node.state] = node.score
        if node.pos == state.end:
            return node.score
        if state.maze.get(node.pos) is not None:
            assert state.maze.get(node.pos) == '#'
            continue
        heapq.heappush(queue, node.step())
        heapq.heappush(queue, node.turn(1j))
        heapq.heappush(queue, node.turn(-1j))
    return min_score


def part2(state: Input) -> int:
    queue = [Node(0, state.start, 1j)]
    min_score = None
    seen = {}
    spots = set()
    while queue:
        node = heapq.heappop(queue)
        if min_score is not None and node.score > min_score:
            break
        if seen.get(node.state, node.score) < node.score:
            continue
        seen[node.state] = node.score
        if node.pos == state.end:
            min_score = node.score
            spots.add(state.end)
            spots.update(node.path)
        if state.maze.get(node.pos) is not None:
            assert state.maze.get(node.pos) == '#'
            continue
        heapq.heappush(queue, node.step())
        heapq.heappush(queue, node.turn(1j))
        heapq.heappush(queue, node.turn(-1j))
    return len(spots)


def parse(text: str) -> Input:
    maze = {}
    start = []
    end = []
    for r, row in enumerate(text.strip().splitlines()):
        for c, char in enumerate(row):
            pos = complex(r, c)
            match char:
                case "S":
                    start.append(pos)
                case "E":
                    end.append(pos)
                case "#":
                    maze[pos] = "#"
                case '.':
                    pass
                case _:
                    raise ValueError(f"Unknown char {char}")
    assert len(start) == 1
    assert len(end) == 1
    return Input(maze, start[0], end[0])


TEST_TEXT = """
###############
#.......#....E#
#.#.###.#.###.#
#.....#.#...#.#
#.###.#####.#.#
#.#.#.......#.#
#.#.#####.###.#
#...........#.#
###.#.#####.#.#
#...#.....#.#.#
#.#.#.###.#.#.#
#.....#...#.#.#
#.###.#.#.#.#.#
#S..#.....#...#
###############
"""


TEST_TEXT_2 = """
#################
#...#...#...#..E#
#.#.#.#.#.#.#.#.#
#.#.#.#...#...#.#
#.#.#.#.###.#.#.#
#...#.#.#.....#.#
#.#.#.#.#.#####.#
#.#...#.#.#.....#
#.#.#####.#.###.#
#.#.#.......#...#
#.#.###.#####.###
#.#.#...#.....#.#
#.#.#.#####.###.#
#.#.#.........#.#
#.#.#.#########.#
#S#.............#
#################
"""


def test_part1():
    assert part1(parse(TEST_TEXT)) == 7036
    assert part1(parse(TEST_TEXT_2)) == 11048


def test_part2():
    assert part2(parse(TEST_TEXT)) == 45
    assert part2(parse(TEST_TEXT_2)) == 64


if __name__ == "__main__":
    LINES = parse(get_input(day=16, year=2024))
    # NOT 124492, 125492
    print(f"Part 1: {part1(LINES)}")
    print(f"Part 2: {part2(LINES)}")
