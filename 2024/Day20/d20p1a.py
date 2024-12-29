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
    cheat_walls = {}

    for i, line in enumerate(lines):
        grid.append(list(line))
        if "S" in line:
            start = (i, line.find("S"))
        if "E" in line:
            end = (i, line.find("E"))

    # Identify walls that can be cheated (are single thickness)
    for x, y in product(range(1, len(grid)-1), range(1, len(grid[0])-1)):
        if grid[x][y] != "#":
            continue
        if (grid[x+1][y] in ".SE") and (grid[x-1][y] in ".SE"):
            cheat_walls[(x, y)] = 0
            continue
        if (grid[x][y+1] in ".SE") and (grid[x][y-1] in ".SE"):
            cheat_walls[(x, y)] = 0
            continue

    # setup dijkstra container references

    unvisited = set()
    shortest_paths = {}

    # read in grid
    for m, row in enumerate(grid):
        for n, c in enumerate(row):
            if c in ".SE":
                unvisited.add((m, n))
                shortest_paths[(m, n)] = {
                    "dist": 1_000_000,
                    "prev": None,
                }

    base_case = dijkstra_solve(grid, start, end, unvisited, shortest_paths, cheat_wall=None)[end]["dist"]
    print(f"Shortest with no cheating: {base_case}")

    for i, cheat_wall in enumerate(cheat_walls):
        print(f"\033[0G\033[K{i}", end="", flush=True)
        cheat_walls[cheat_wall] = dijkstra_solve(grid, start, end, unvisited, shortest_paths, cheat_wall)[end]["dist"]
    
    pprint(cheat_walls)

    # ans: 


def dijkstra_solve(
        grid: list[list[str]],
        start: tuple[int],
        end: tuple[int],
        unvisited: set,
        shortest_paths: dict,
        cheat_wall: tuple[str] = None,
        ) -> dict:
    # initialize
    from time import time_ns, time
    init_start = time()
    from copy import deepcopy
    
    visited = set()
    unvisited = unvisited.copy()
    shortest_paths = deepcopy(shortest_paths)
    shortest_paths[(start)]["dist"] = 0

    if cheat_wall != None:
        grid[cheat_wall[0]][cheat_wall[1]] = "."
        unvisited.add(cheat_wall)
        shortest_paths[cheat_wall] = {
            "dist": 1_000_000,
            "prev": None,
        } 
    # print(f"Initialize: {time() - init_start}")
    
    dijkstra_start = time()
    
    # visit all unvisited nodes
    while unvisited:
        # start with the node closest to start
        minimum = 1_000_000
        curr = None
        for node in unvisited:
            if shortest_paths[node]["dist"] < minimum:
                curr = node
                minimum = shortest_paths[node]["dist"]

        if curr == None:
            break

        # get distance of neighbours
        for neighbour in get_neighbours(grid, curr):
            if neighbour in visited:
                continue
            neighbour_dist = 1 + shortest_paths[curr]["dist"]
            if neighbour_dist < shortest_paths[neighbour]["dist"]:
                shortest_paths[neighbour]["dist"] = neighbour_dist
                shortest_paths[neighbour]["prev"] = curr

        # make node visisted
        unvisited.remove(curr)
        visited.add(curr)
        if curr == end:
            break

    if cheat_wall != None:
        grid[cheat_wall[0]][cheat_wall[1]] = "#"

    # print(f"Dijkstra: {time() - dijkstra_start}")
    return shortest_paths



def get_neighbours(grid, node: tuple[int]) -> list[tuple[int]]:
    directions = ((-1,0), (0,1), (1,0), (0,-1))
    neighbours = []

    for (dx, dy) in directions:
        x, y = node[0]+dx, node[1]+dy
        if grid[x][y] in ".E":
            neighbours.append((x, y))
    return neighbours

def print_grid(grid) -> None:
    for row in grid:
        print("".join(row))


if __name__ == "__main__":
    main(sys.argv)


