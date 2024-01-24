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
    r_len = len(grid)
    c_len = len(grid[0])

    # Initialize start
    if len(argv) == 1:
        steps = 6
    else:
        steps = 64
    start_location = (s_coordinate[0], s_coordinate[1], steps)      # (5, 5, 6) in example

    # Initialize data structures
    reached_locations: set[start_location] = set()       # (row, column, steps_remaining)
    movements: deque[start_location] = deque()             # (row, column, steps_remaining)
    movements.append(start_location)

    while movements:
        # print(f"Deque size: {len(movements)}")
        location = movements.popleft()

        if location in reached_locations:
            continue
        reached_locations.add(location)

        for new_location in gen_movements(grid, r_len, c_len, location):
            movements.append(new_location)

    final_locations = {location for location in reached_locations if location[2] == 0}
    # pprint(final_locations)
    print(len(final_locations))
    


    

def gen_movements(
        grid: list[list[str]],
        r_len: int,
        c_len: int,
        location: tuple[int]
        ) -> list[tuple]:
    new_movements = []
    if location[2] == 0:
        return new_movements

    new_locations = [(location[0]+i, location[1]+j) for i, j in [(-1, 0), (0, 1), (1, 0), (0, -1)]]

    for new_loc in new_locations:
        if new_loc[0] < 0 or new_loc[0] >= r_len:
            continue
        if new_loc[1] < 0 or new_loc[1] >= c_len:
            continue
        if grid[new_loc[0]][new_loc[1]] == '#':
            continue
        new_movements.append(new_loc + (location[2] - 1,))
    return new_movements
    


main(sys.argv)


