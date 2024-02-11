import sys
import re
from collections import deque, Counter
from pathlib import Path
from pprint import pprint

# Run with test data    -> python3 -m d#p#
# Run with puzzle data  -> python3 -m d#p# X (any argument)

def main(argv: list[str]):
    # Prep Code
    lines: list[str]

    if len(argv) == 1:
        test_data = """\
#.#####################
#.......#########...###
#######.#########.#.###
###.....#.>.>.###.#.###
###v#####.#v#.###.#.###
###.>...#.#.#.....#...#
###v###.#.#.#########.#
###...#.#.#.......#...#
#####.#.#.#######.#.###
#.....#.#.#.......#...#
#.#####.#.#.#########v#
#.#...#...#...###...>.#
#.#.#v#######v###.###v#
#...#.>.#...>.>.#.###.#
#####v#.#.###v#.#.###.#
#.....#...#...#.#.#...#
#.#########.###.#.#.###
#...###...#...#...#.###
###.###.#.###v#####v###
#...#...#.#.>.>.#.>.###
#.###.###.#.###.#.#v###
#.....###...###...#...#
#####################.#"""
        lines = test_data.splitlines()
    else:
        data_file = Path.cwd() / "puzzle_data.txt"
        with open(data_file, "r") as f:
            lines = f.readlines()

    for i, line in enumerate(lines):
        lines[i] = line.strip()

    # Puzzle code
    #----------------------------------------------------------------

    from collections import deque
    from copy import deepcopy

    # initialize
    mp = lines
    Trail.mp: list[str] = mp
    start = (0, mp[0].index('.'))
    trail_start = (start[0] + 1, start[1])
    end = (len(mp) - 1, mp[-1].index('.'))

    trail_q: deque[Trail] = deque()
    trail_q.append(Trail(trail_start, start, 1, end))
    completed: list[Trail] = []


    # Start loop
    while len(trail_q) > 0:
        trail = trail_q.popleft()
        directions = trail.scan_directions()
        if len(directions) == 0:
            raise ValueError("No directions returned")
        if len(directions) == 1:
            trail.move(directions[0])
            if trail.at_end():
                completed.append(trail)
            else:
                trail_q.append(trail)
        else:
            for direction in directions:
                new_trail = deepcopy(trail)
                new_trail.move(direction)
                trail_q.append(new_trail)

    print(completed)
    for trail in completed:
        print(trail.steps)
    print("max:", max(trail.steps for trail in completed))




class Trail():
    mp: list[str]
    directions = {
        (-1, 0),
        (0, 1),
        (1, 0),
        (0, -1)
    }

    def __init__(
            self,
            position: tuple[int],
            prev_position: tuple[int],
            steps: int,
            end: tuple[int]
            ) -> None:
        self.position = position
        self.prev_position = prev_position
        self.steps = steps
        self.end = end
    
    def scan_directions(self) -> list[tuple[int]]:
        new_directions = []
        for dx, dy in self.directions:
            if self.prev_position == (self.position[0] + dx, self.position[1] + dy):
                # coming from that direction
                continue
            c = self.mp[self.position[0] + dx][self.position[1] + dy]
            if c == '#':
                # can't go into walls
                continue
            if (dx, dy) == (-1, 0) and c == 'v':
                continue
            if (dx, dy) == (0, 1) and c == '<':
                continue
            if (dx, dy) == (1, 0) and c == '^':
                continue
            if (dx, dy) == (0, -1) and c == '>':
                continue
            new_directions.append((dx, dy))
        return new_directions
    
    def move(self, direction: tuple[int]) -> None:
        self.prev_position = self.position
        self.position = (self.position[0] + direction[0], self.position[1] + direction[1])
        self.steps += 1        

    def at_end(self) -> bool:
        return self.position == self.end



if __name__ == "__main__":
    main(sys.argv)


