import sys
import re
from collections import deque, Counter, defaultdict
from pathlib import Path
from pprint import pprint
from functools import partial, lru_cache

# Run with test data    -> python3 -m d#p#
# Run with puzzle data  -> python3 -m d#p# X (any argument)

def main(argv: list[str]):
    # Prep Code
    lines: list[str]

    if len(argv) == 1:
        test_data = """\
....#.....
.........#
..........
..#.......
.......#..
..........
.#..^.....
........#.
#.........
......#..."""
        lines = test_data.splitlines()
    else:
        data_file = Path.cwd() / "puzzle_data.txt"
        with open(data_file, "r") as f:
            lines = f.readlines()

    for i, line in enumerate(lines):
        lines[i] = line.strip()

    # Puzzle code
    #----------------------------------------------------------------

    grid = lines
    height = len(lines)
    width = len(lines[0])
    bounds = [height, width]
    facing = (-1, 0)
    turns = {
        (-1, 0): (0, 1),
        (0, 1): (1, 0),
        (1, 0): (0, -1),
        (0, -1): (-1, 0),
    }
    visits = {}


    from itertools import product

    for x, y in product(range(height), range(width)):
        if grid[x][y] == "^":
            start = (x, y)
            break

    print(f"{start=}")
    position = list(start)
    visits[start] = 1
    in_bounds = True

    while in_bounds:
        #print(f"{position=} ", end="")
        if check_for_obstacle(grid, position, bounds, facing):
            #print(f"Obstacle! Turning to {turns[facing]}")
            facing = turns[facing]
            continue
        move_1_step(position, facing)
        visits[tuple(position)] = 1

        in_bounds = still_in_bounds(position, bounds)
        #print(f"{in_bounds=}")


    print(f"Total: {len(visits)-1}")
    # ans: 5269

def check_for_obstacle(grid: list[str], position: list[int], bounds: list[int], facing: tuple[int]) -> bool:
    position_to_check = (position[0] + facing[0], position[1] + facing[1])
    if still_in_bounds(position_to_check, bounds) == False:
        return False
    if grid[position_to_check[0]][position_to_check[1]] == "#":
        return True
    return False

def move_1_step(position: list[int], facing: tuple[int]) -> None:
    (position[0], position[1]) = (position[0] + facing[0], position[1] + facing[1])
    return

def still_in_bounds(position: list[int], bounds: list[int]) -> bool:
    if (position[0] < 0) or (position[0] >= bounds[0]):
        return False
    if (position[1] < 0) or (position[1] >= bounds[1]):
        return False
    return True



if __name__ == "__main__":
    main(sys.argv)


