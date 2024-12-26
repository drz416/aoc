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
5,4
4,2
4,5
3,0
2,1
6,3
2,4
1,5
0,6
3,3
2,6
5,1
1,2
5,5
2,5
6,5
1,4
0,4
6,4
1,1
6,1
1,0
0,5
1,6
2,0"""
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
    if len(argv) == 1:
        drop = 12
        dim = 6 + 1
        end_node = (6, 6)
    else:
        drop = 1024
        dim = 70 + 1
        end_node = (70, 70)

    byts = tuple((int(line.split(",")[1]), int(line.split(",")[0])) for line in lines)
    
    
    dd = 1500
    while True:
        # reset grid
        grid: list[list[str]] = []
        for _ in range(dim):
            grid.append(["."] * dim)

        # drop bytes
        for i, (m, n) in zip(range(drop+dd), byts):
            grid[m][n] = "#"
        print(f"Drops {drop+dd}: ", end="")
            
        shortest_paths = dijkstra_solve(grid)
        dist_to_end_node = shortest_paths[end_node]["dist"]
        print(f"{end_node=} distance={dist_to_end_node}")

        if dist_to_end_node == 1_000_000:
            break

        dd += 1

    print(f"Last drop = {byts[drop+dd-1]} => {byts[drop+dd-1][1], byts[drop+dd-1][0]}")
    
    # ans: 60,37


    

def print_grid(grid) -> None:
    for row in grid:
        print("".join(row))

def dijkstra_solve(grid) -> dict:
    # setup containers
    dimensions = [0, len(grid)]
    visited = set()
    unvisited = set()
    shortest_paths = {}

    # read in grid
    for m, row in enumerate(grid):
        for n, c in enumerate(row):
            if c == ".":
                unvisited.add((m, n))
                shortest_paths[(m, n)] = {
                    "dist": 1_000_000,
                    "prev": None,
                }
    
    # initialize
    shortest_paths[(0,0)]["dist"] = 0
    
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
        for neighbour in get_neighbours(grid, dimensions, curr):
            if neighbour in visited:
                continue
            neighbour_dist = 1 + shortest_paths[curr]["dist"]
            if neighbour_dist < shortest_paths[neighbour]["dist"]:
                shortest_paths[neighbour]["dist"] = neighbour_dist
                shortest_paths[neighbour]["prev"] = curr

        # make node visisted
        unvisited.remove(curr)
        visited.add(curr)

    return shortest_paths





def get_neighbours(grid, dimensions, node) -> list[tuple[int]]:
    directions = ((-1,0), (0,1), (1,0), (0,-1))
    neighbours = []

    for (dm, dn) in directions:
        m, n = node[0]+dm, node[1]+dn
        if (m < 0) or (m > dimensions[1] - 1):
            continue
        if (n < 0) or (n > dimensions[1] - 1):
            continue
        if grid[m][n] == ".":
            neighbours.append((m, n))
    return neighbours



if __name__ == "__main__":
    main(sys.argv)


