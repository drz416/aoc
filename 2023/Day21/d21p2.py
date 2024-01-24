from functools import partial, lru_cache

import sys
import re
from collections import deque, Counter
from pathlib import Path
from pprint import pprint

# Run with test data    -> python3 -m d#p#
# Run with puzzle data  -> python3 -m d#p# X (any argument)

argv = sys.argv


# Prep Code
lines: list[str]

if len(argv) == 1:
    test_data = """\
...........
.....###.#.
.###.##..#.
..#.#...#..
....#.#....
.##..S####.
.##..#...#.
.......##..
.##.#.####.
.##..##.##.
..........."""
    lines = test_data.splitlines()
else:
    data_file = Path.cwd() / "puzzle_data.txt"
    with open(data_file, "r") as f:
        lines = f.readlines()

for i, line in enumerate(lines):
    lines[i] = line.strip()

# Puzzle code
#----------------------------------------------------------------

# Create x, y grid, and note S position
s_coordinate = [0, 0]
grid = []
for i, line in enumerate(lines):
    grid.append(list(line))
    if line.find('S') >= 0:
        s_coordinate = [i, line.find('S')]
grid_size = [len(grid), len(grid[0])]

# Create data structures
visited = set()
sys.setrecursionlimit(2000)

# Initialize start
if len(argv) == 1:
    steps = 500
else:
    steps = 26501365
start_location = (s_coordinate[0], s_coordinate[1], steps)      # example is: (5, 5, 6)

@lru_cache(maxsize=None)
def count_movements(location: tuple[int]) -> int:
    visited.add(location)
    if location[2] == 0:
        return 1
    
    possible_movements = 0
    neighbours = [(location[0]+i, location[1]+j) for i, j in ((-1, 0), (0, 1), (1, 0), (0, -1))]    
    for neighbour in neighbours:
        if grid[neighbour[0] % grid_size[0]][neighbour[1] % grid_size[1]] == '#':
            continue
        neighbour += (location[2] - 1,)
        # print("visited test", neighbour, visited, neighbour in visited)
        # if (neighbour[0] % grid_size[0], neighbour[1] % grid_size[1], neighbour[2]) in visited:
        if neighbour in visited:
            continue
        # print(location, neighbour)
        possible_movements += count_movements(neighbour)
        # print(location, neighbour, possible_movements)
    return possible_movements


print(count_movements(start_location))
# pprint(visited)





