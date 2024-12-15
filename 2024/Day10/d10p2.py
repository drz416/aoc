import sys
import re
from collections import deque, Counter, defaultdict
from pathlib import Path
from pprint import pprint
from functools import partial, lru_cache
from itertools import product, combinations

# Run with test data    -> python3 -m d#p#
# Run with puzzle data  -> python3 -m d#p# X (any argument)

def main(argv: list[str]):
    # Prep Code
    lines: list[str]

    if len(argv) == 1:
        test_data = """\
89010123
78121874
87430965
96549874
45678903
32019012
01329801
10456732"""
        lines = test_data.splitlines()
    else:
        data_file = Path.cwd() / "puzzle_data.txt"
        with open(data_file, "r") as f:
            lines = f.readlines()

    for i, line in enumerate(lines):
        lines[i] = line.strip()

    # Puzzle code
    #----------------------------------------------------------------

    # Build base grid
    base_grid: list[list[int]] = []
    for line in lines:
        base_grid.append([int(c) for c in line])
    base_grid_h = len(base_grid)
    base_grid_w = len(base_grid[0])

    # Find trailheads
    trails: dict[list] = {}
    for r, row in enumerate(base_grid):
        for c, element in enumerate(row):
            if element == 0:
                trails[(r+1, c+1)] = []         #+1+1 are new positions after border is added

    # Build bordered grid around brase grid
    grid: list[list[int]] = [[0]*(base_grid_w+2) for _ in range(base_grid_h+2)]

    for i, row in enumerate(base_grid):
        grid[i+1][1:len(row)+1] = row

    # Search for trail ends from each trailhead
    for trailhead in trails:
        search_trail(grid, trails, trailhead, trailhead)
        
    pprint(grid)
    pprint(trails)

    total = 0
    for trail_ends in trails.values():
        total += len(trail_ends)


    print(f"Total: {total}")
    # ans: 1192

def search_trail(grid: list[list[int]], trails: dict[list], trailhead: tuple[int], curr_position: tuple[int]) -> None:
    if grid[curr_position[0]][curr_position[1]] == 9:
        trails[trailhead].append(curr_position) 
        return
    directions = find_directions(grid, curr_position)
    for new_direction in directions:
        search_trail(grid, trails, trailhead, new_direction)

def find_directions(grid, position: tuple[int]) -> list[tuple[int]]:
    val = grid[position[0]][position[1]]
    possible_directions = [(-1,0), (0,1), (1,0), (0,-1)]
    good_directions = []
    for (x,y) in possible_directions:
        if grid[position[0]+x][position[1]+y] == val + 1:
            good_directions.append((position[0]+x,position[1]+y))
    return good_directions




if __name__ == "__main__":
    main(sys.argv)


