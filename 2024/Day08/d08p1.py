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
    height, width = len(lines), len(lines[0])

    for i, line in enumerate(lines):
        for j, c in enumerate(line):
            if c == ".":
                continue
            antennas[c].append((i,j))

    
    for antenna, locations in antennas.items():
        print(f"{antenna=}")
        for a1, a2 in combinations(locations, 2):
            pos_slope = get_slope(a1, a2)
            neg_slope = flip_slope(pos_slope)

            pos_node = (a2[0]+pos_slope[0], a2[1]+pos_slope[1])
            neg_node = (a1[0]+neg_slope[0], a1[1]+neg_slope[1])
            print(f"  {a1=} {a2=} -- {pos_slope=} {neg_slope=} --> nodes {pos_node=} {neg_node=}")

            if (0 <= pos_node[0] < width) and (0 <= pos_node[1] < height):
                nodes.add(pos_node)
            if (0 <= neg_node[0] < width) and (0 <= neg_node[1] < height):
                nodes.add(neg_node)


    print(f"Total: {len(nodes)}")
    # ans: 285

def get_slope(antenna1: tuple, antenna2: tuple) -> tuple:
    return (antenna2[0] - antenna1[0], antenna2[1] - antenna1[1])

def flip_slope(slope: tuple) -> tuple:
    return (-slope[0], -slope[1])


if __name__ == "__main__":
    main(sys.argv)


