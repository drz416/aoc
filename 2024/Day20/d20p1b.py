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
###############
#...#...#.....#
#.#.#.#.#.###.#
#S#...#.#.#...#
#######.#.#.###
#######.#.#...#
#######.#.###.#
###..E#...#...#
###.#######.###
#...###...#...#
#.#####.#.###.#
#.#...#.#.#...#
#.#.#.#.#.#.###
#...#...#...###
###############"""
        lines = test_data.splitlines()
    else:
        data_file = Path.cwd() / "puzzle_data.txt"
        with open(data_file, "r") as f:
            lines = f.readlines()

    for i, line in enumerate(lines):
        lines[i] = line.strip()

    # Puzzle code
    #----------------------------------------------------------------

    # Setup containers
    grid: list[list[str]] = []
    for i, line in enumerate(lines):
        grid.append(list(line))
        if "S" in line:
            start = (i, line.find("S"))
        if "E" in line:
            end = (i, line.find("E"))

    # Traverse track and record distance markers
    dist_markers = {start: 0}
    last_node = None
    curr = start
    distance = 0
    while curr != end:
        neighbours = get_neighbours(grid, curr, last_node)
        if len(neighbours) != 1:
            raise ValueError(f"Fork in the road at {curr} {neighbours=}")
        last_node = curr
        curr = neighbours[0]
        distance += 1
        dist_markers[curr] = distance

    total_distance = dist_markers[end]

    # Identify walls that can be cheated (are single thickness)
    cheat_walls = {}
    for x, y in product(range(1, len(grid)-1), range(1, len(grid[0])-1)):
        if grid[x][y] != "#":
            continue
        if (grid[x+1][y] in ".SE") and (grid[x-1][y] in ".SE"):
            from_start = min(dist_markers[(x+1,y)], dist_markers[(x-1,y)])
            from_end = total_distance - max(dist_markers[(x+1,y)], dist_markers[(x-1,y)])
            cheat_walls[(x, y)] = from_start + 2 + from_end
            continue
        if (grid[x][y+1] in ".SE") and (grid[x][y-1] in ".SE"):
            from_start = min(dist_markers[(x,y+1)], dist_markers[(x,y-1)])
            from_end = total_distance - max(dist_markers[(x,y+1)], dist_markers[(x,y-1)])
            cheat_walls[(x, y)] = from_start + 2 + from_end
            continue


    c = Counter([total_distance - dist for dist in cheat_walls.values()])
    
    total = 0
    for dist in cheat_walls.values():
        if total_distance - dist >= 100:
            total += 1
    
    print(total)    

    # ans: 






def get_neighbours(grid, node: tuple[int], last_node: tuple[int]) -> list[tuple[int]]:
    directions = ((-1,0), (0,1), (1,0), (0,-1))
    neighbours = []

    for (dx, dy) in directions:
        x, y = node[0]+dx, node[1]+dy
        if last_node == (x, y):
            continue
        if grid[x][y] in ".E":
            neighbours.append((x, y))
    return neighbours

def print_grid(grid) -> None:
    for row in grid:
        print("".join(row))


if __name__ == "__main__":
    main(sys.argv)


