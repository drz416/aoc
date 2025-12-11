# /// script
# requires-python = ">=3.14"
# dependencies = []
# ///
#
# to add dependencies -> uv add --script <file> <module>
# to remove dependencies -> uv remove --script <file> <module>
# to run with test data    -> uv run --script d#p#
# to run with puzzle data  -> uv run --script d#p# X (any argument)



# Template Imports
#----------------------------------------------------------------
import sys
import re
from pathlib import Path
from pprint import pprint
from time import time, time_ns
from collections import deque, Counter, defaultdict
from functools import partial, lru_cache
from itertools import product, combinations
#----------------------------------------------------------------


# Solution Code
#----------------------------------------------------------------

def get_directions(position: tuple[int], boundaries: list[int]) -> tuple[tuple[int]]:
    if position == (0,0):                                       # top left
        return ((0,1), (1,1), (1,0))
    if position == (0,boundaries[1]):                           # top right
        return ((1,0), (1,-1), (0,-1))
    if position == tuple(boundaries):                           # bottom right
        return ((0,-1), (-1,-1), (-1,0))
    if position == (boundaries[0], 0):                          # bottom left
        return ((-1,0), (-1,1), (0,1))
    if position[0] == 0:                                        # top
        return ((0,1), (1,1), (1,0), (1,-1), (0,-1))
    if position[1] == boundaries[1]:                            # right
        return ((1,0), (1,-1), (0,-1), (-1,-1), (-1,0))
    if position[0] == boundaries[0]:                            # bottom
        return ((0,-1), (-1,-1), (-1,0), (-1,1), (0,1))
    if position[1] == 0:                                        # left
        return ((-1,0), (-1,1), (0,1), (1,1), (1,0))
    return ((-1,0), (-1,1), (0,1), (1,1), (1,0), (1,-1), (0,-1), (-1,-1))

def count_surrounding_rolls(
        position: tuple[int],
        grid: list[str],
        directions: tuple[tuple[int]]) -> int:
    rolls = 0
    for i, j in directions:
        if grid[position[0]+i][position[1]+j] == "@":
            rolls += 1
    return rolls

accessible: set[tuple[int]] = set()


def main(lines: list[str]):

    rows = len(lines)
    columns = len(lines[0])
    boundaries = [rows-1, columns-1]


    for i, row in enumerate(lines):
        for j, pos in enumerate(row):
            if pos == ".":
                continue
            if count_surrounding_rolls(
                    (i,j),
                    lines,
                    get_directions((i,j), boundaries)) < 4:
                accessible.add((i,j))

    ans = len(accessible)

    print("")
    print(f"Ans: {ans}")

    # ans: 1416




#----------------------------------------------------------------



# Data load and caling main()
#----------------------------------------------------------------
if __name__ == "__main__":
    # Prep Data
    lines: list[str]

    if len(sys.argv) == 1:
        # Paste test example data here
        test_data = """\
..@@.@@@@.
@@@.@.@.@@
@@@@@.@.@@
@.@@@@..@.
@@.@@@@.@@
.@@@@@@@.@
.@.@.@.@@@
@.@@@.@@@@
.@@@@@@@@.
@.@.@@@.@."""
        lines = test_data.splitlines()
    else:
        data_file = Path.cwd() / "puzzle_data.txt"
        with open(data_file, "r") as f:
            lines = f.readlines()

    for i, line in enumerate(lines):
        lines[i] = line.strip()
    
    start_time = time()
    main(lines)
    print("")
    print(f"Time in main(): {time() - start_time:.06f}s")
#----------------------------------------------------------------


