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

    class Present():
        def __init__(self, shape_index: int) -> None:
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
            n += 5
        else:
            grid, presents = rows[n].split(": ")
            x, y = grid.split("x")
            grids.append([(y, x), tuple(presents.split())])
            n += 1

    # pprint(shapes, width=20)
    # pprint(grids)

    prst = Present(1)
    print(prst)
    prst.flip_horizontal()
    prst.rotate_90()
    print(prst)

    ans = 0

    
    print(f"\nAns: {ans}")

    # ans: ####




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


