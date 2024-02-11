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
###.....#.....###.#.###
###.#####.#.#.###.#.###
###.....#.#.#.....#...#
###.###.#.#.#########.#
###...#.#.#.......#...#
#####.#.#.#######.#.###
#.....#.#.#.......#...#
#.#####.#.#.#########.#
#.#...#...#...###.....#
#.#.#.#######.###.###.#
#...#...#.......#.###.#
#####.#.#.###.#.#.###.#
#.....#...#...#.#.#...#
#.#########.###.#.#.###
#...###...#...#...#.###
###.###.#.###.#####.###
#...#...#.#.....#...###
#.###.###.#.###.#.#.###
#.....###...###...#...#
#####################.#"""
        lines = test_data.splitlines()
    else:
        data_file = Path.cwd() / "puzzle_data2.txt"
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
    start = (0, mp[0].index('.'))
    trail_start = (start[0] + 1, start[1])
    end = (len(mp) - 1, mp[-1].index('.'))
    Trail.mp: list[str] = mp
    Trail.end: tuple[int] = end

    trail_q: deque[Trail] = deque()
    trail_q.append(Trail(trail_start, {start}, 1))
    completed = 0
    max_steps = 0


    # Start loop
    count = 0
    while len(trail_q) > 0:
        if count % 100_000 == 0:
            print(f"Trails: {len(trail_q):7}  |  Completed: {(completed):7}  |  Max Steps: {max_steps:5}")
        count += 1

        trail = trail_q.popleft()
        directions = trail.scan_directions()
        if len(directions) == 0:
            del trail
            continue                # dead-end, delete path
        if len(directions) == 1:
            trail.move(directions[0])
            if trail.at_end():
                completed += 1
                max_steps = max(max_steps, trail.steps)
            else:
                trail_q.append(trail)
        else:
            for direction in directions:
                new_trail = deepcopy(trail)
                new_trail.move(direction)
                trail_q.append(new_trail)

    # print(completed)
    print("End")
    print(f"Trails: {len(trail_q):7}  |  Completed: {(completed):7}  |  Max Steps: {max_steps:5}")




class Trail():
    mp: list[str]
    end: tuple[int]
    directions = {
        0: (1, 0),
        1: (0, 1),
        2: (0, -1),
        3: (-1, 0)
    }

    def __init__(
            self,
            position: tuple[int],
            prev_positions: set[tuple[int]],
            steps: int,
            ) -> None:
        self.position = position
        self.prev_positions = prev_positions
        self.steps = steps
    
    def scan_directions(self) -> list[tuple[int]]:
        new_directions = []
        for dx, dy in self.directions.values():
            if (self.position[0] + dx, self.position[1] + dy) in self.prev_positions:
                # already visited location
                continue
            if self.mp[self.position[0] + dx][self.position[1] + dy] == '#':
                # can't go into walls
                continue
            new_directions.append((dx, dy))
        return new_directions
    
    def move(self, direction: tuple[int]) -> None:
        self.prev_positions.add(self.position)
        self.position = (self.position[0] + direction[0], self.position[1] + direction[1])
        self.steps += 1        

    def at_end(self) -> bool:
        return self.position == self.end



if __name__ == "__main__":
    main(sys.argv)


