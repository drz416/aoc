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
............
........0...
.....0......
.......0....
....0.......
......A.....
............
............
........A...
.........A..
............
............"""
        lines = test_data.splitlines()
    else:
        data_file = Path.cwd() / "puzzle_data.txt"
        with open(data_file, "r") as f:
            lines = f.readlines()

    for i, line in enumerate(lines):
        lines[i] = line.strip()

    # Puzzle code
    #----------------------------------------------------------------

    antennas = defaultdict(list)
    nodes = set()
    bounds = [len(lines), len(lines[0])]

    for i, line in enumerate(lines):
        for j, c in enumerate(line):
            if c == ".":
                continue
            antennas[c].append((i,j))

    
    for antenna, locations in antennas.items():
        print(f"{antenna=}")
        for a1, a2 in combinations(locations, 2):
            nodes.add(a1)
            nodes.add(a2)

            pos_slope = get_slope(a1, a2)
            neg_slope = flip_slope(pos_slope)

            print(f"  {a1=} {a2=} -- {pos_slope=} {neg_slope=} --> nodes ", end="")

            curr_node = a2
            while True:
                curr_node = (curr_node[0]+pos_slope[0], curr_node[1]+pos_slope[1])
                if check_in_bounds(curr_node, bounds) == False:
                    break
                nodes.add(curr_node)
                print(f"{curr_node}, ", end="")

            curr_node = a1
            while True:
                curr_node = (curr_node[0]+neg_slope[0], curr_node[1]+neg_slope[1])
                if check_in_bounds(curr_node, bounds) == False:
                    break
                nodes.add(curr_node)
                print(f"{curr_node}, ", end="")
            print("")
            

    print(f"Total: {len(nodes)}")
    # ans: 944

def get_slope(antenna1: tuple, antenna2: tuple) -> tuple:
    return (antenna2[0] - antenna1[0], antenna2[1] - antenna1[1])

def flip_slope(slope: tuple) -> tuple:
    return (-slope[0], -slope[1])

def check_in_bounds(node: tuple, bounds: list) -> bool:
    if (0 <= node[0] < bounds[0]) and (0 <= node[1] < bounds[1]):
        return True
    return False

if __name__ == "__main__":
    main(sys.argv)


