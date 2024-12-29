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

    grid_d = [len(grid), len(grid[0])]
    trying_to_save = 50 if len(argv) == 1 else 100

    # Traverse track and record distance markers
    dist_markers = {start: 0}
    prev_node = None
    curr = start
    distance = 0
    while curr != end:
        neighbours = get_neighbours(grid, curr, prev_node)
        if len(neighbours) != 1:
            raise ValueError(f"Fork in the road at {curr} {neighbours=}")
        prev_node = curr
        curr = neighbours[0]
        distance += 1
        dist_markers[curr] = distance

    total_distance = dist_markers[end]
    print(total_distance)
    # breakpoint()
    cheat_paths = {}
    distance_saved = {}
    for i, (node1, node2) in enumerate(combinations(dist_markers.keys(), 2)):
        if i % 100_000 == 0:
            print(i)
        path_distance = abs(dist_markers[node1] - dist_markers[node2])
        if path_distance <= trying_to_save:
            continue

        straight_distance = get_distance(node1, node2)
        if straight_distance > 20:
            continue
        if straight_distance == path_distance:
            continue

        cheat_dist = find_path_through_walls(grid, grid_d, node1, node2)
        if cheat_dist == None:
            continue
        if cheat_dist >= path_distance:
            continue
        
        # cheat effective
        from_start, from_end = sorted([dist_markers[node1], dist_markers[node2]])
        from_end = total_distance - from_end
        cheat_paths[(node1, node2)] = from_start + cheat_dist + from_end
        distance_saved[(node1, node2)] = total_distance - (from_start + cheat_dist + from_end)
                
    
    pprint(distance_saved)
    c = Counter(distance_saved.values())
    for saved in range(total_distance+1):
        try:
            ct = c[saved]
        except IndexError:
            continue
        if ct == 0:
            continue
        print(f"There are {ct} cheats that save {saved} picoseconds")
        
    total = 0
    for saved in distance_saved.values():
        if saved >= 50:
            total += 1

    print(total)    

    # ans: can't find bug


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

def get_distance(node1: tuple[int], node2: tuple) -> int:
    return abs(node1[0] - node2[0]) + abs(node1[1] - node2[1])

def find_path_through_walls(grid, grid_d, start_node, final_node) -> int:
    q = deque()
    q.append((start_node, 0))
    visited = set()
    directions = ((-1,0), (0,1), (1,0), (0,-1))
    
    while q:
        # breakpoint()
        node, dist = q.popleft()
        if dist == 20:
            continue
        
        visited.add(node)

        for (dx, dy) in directions:
            x, y = node[0]+dx, node[1]+dy
            if x < 0 or x >= grid_d[0]:
                continue
            if y < 0 or y >= grid_d[1]:
                continue
            if (x, y) in visited:
                continue
            if (x, y) == final_node:
                return dist + 1

            if grid[x][y] == "#":
                q.append(((x, y), dist+1))
            
    return None
    


    




if __name__ == "__main__":
    main(sys.argv)


