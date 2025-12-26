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

def main(rows: list[str]):

    # FYI this class definition is not required for this problem, as this problem
    # is NP-complete it cannot be solved, however the AOC puzzle has a very
    # simple solution that uses process of elimination

    class Present():
        def __init__(self, shape_index: int) -> None:
            self.index = shape_index
            self.shape = shapes[shape_index]

        def rotate_90(self) -> None:
            self.shape = ((self.shape[2][0], self.shape[1][0], self.shape[0][0]),
                          (self.shape[2][1], self.shape[1][1], self.shape[0][1]),
                          (self.shape[2][2], self.shape[1][2], self.shape[0][2]))
        # def rotate_180(self) -> None:
        #     self.shape = ((self.shape[2][2], self.shape[2][1], self.shape[2][0]),
        #                   (self.shape[1][2], self.shape[1][1], self.shape[1][0]),
        #                   (self.shape[0][2], self.shape[0][1], self.shape[0][0]))

        # def rotate_270(self) -> None:
        #     self.rotate_180()
        #     self.rotate_90()

        def flip_horizontal(self) -> None:
            self.shape = ((self.shape[2][0], self.shape[2][1], self.shape[2][2]),
                          (self.shape[1][0], self.shape[1][1], self.shape[1][2]),
                          (self.shape[0][0], self.shape[0][1], self.shape[0][2]))

        def __str__(self):
            s = ""
            for row in self.shape:
                for c in row:
                    s += '#' if c == 1 else '.'
                s += '\n'
            return s

    shapes: dict = {}
    shape_sizes: dict = {}
    shape_index = -1
    to_int = lambda x: 1 if x == '#' else 0
    grids = []

    n = 0    
    while n < len(rows):
        if rows[n][1] == ":":
            shape = []
            shape.append(tuple(to_int(c) for c in rows[n+1]))
            shape.append(tuple(to_int(c) for c in rows[n+2]))
            shape.append(tuple(to_int(c) for c in rows[n+3]))
            shape_index += 1
            shapes[shape_index] = shape
            shape_sizes[shape_index] = sum(shape[0]) + sum(shape[1]) + sum(shape[2])
            n += 5
        else:
            grid, presents = rows[n].split(": ")
            x, y = grid.split("x")
            grids.append([(int(y), int(x)), tuple(map(int,presents.split()))])
            n += 1

    def check_no_overlap_fit(grid: tuple[int], presents: tuple[int]) -> bool:
        no_overlap_m, no_overlap_n = grid[0] // 3, grid[1] // 3
        no_overlap_fit = no_overlap_m * no_overlap_n
        if no_overlap_fit >= sum(presents):
            return True
        return False
    
    def check_no_physical_space(grid: tuple[int], presents: tuple[int]) -> bool:
        space_required = 0
        for i, present in enumerate(presents):
            space_required += present * shape_sizes[i]
        if space_required > (grid[0] * grid[1]):
            return True
        return False


    fit = 0
    no_fit = 0
    unsure = 0
    # Go through all grids
    for grid, presents in grids:
        # check if they fit with no overlap (treat each shape as 3x3)
        if check_no_overlap_fit(grid, presents):
            fit += 1
            continue
        # check if they cannot possibly fit due to number of squares
        if check_no_physical_space(grid, presents):
            no_fit += 1
            continue
        unsure += 1

    print(f"{fit=}\n{no_fit=}\n{unsure=}")


    ans = fit
    print(f"\nAns: {ans}")

    # ans: 512




#----------------------------------------------------------------



# Data load and caling main()
#----------------------------------------------------------------
if __name__ == "__main__":
    # Prep Data
    rows: list[str]

    if len(sys.argv) == 1:
        # Paste test example data here
        test_data = """\
0:
###
##.
##.

1:
###
##.
.##

2:
.##
###
##.

3:
##.
###
##.

4:
###
#..
###

5:
###
.#.
###

4x4: 0 0 0 0 2 0
12x5: 1 0 1 0 2 2
12x5: 1 0 1 0 3 2"""
        rows = test_data.splitlines()
    else:
        data_file = Path.cwd() / "puzzle_data.txt"
        with open(data_file, "r") as f:
            rows = f.readlines()

    for i, line in enumerate(rows):
        rows[i] = line.strip()
    
    start_time = time()
    main(rows)
    print("")
    print(f"Time in main(): {time() - start_time:.06f}s")
#----------------------------------------------------------------


