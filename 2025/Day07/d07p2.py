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

    manifold: list[list[str]] = []
    for row in rows:
        manifold.append(list(row))
    start = (0, rows[0].find("S"))
    last_row = len(rows) - 1

    @lru_cache
    def get_timelines(position: tuple[int]) -> int:
        nonlocal manifold
        nonlocal last_row

        if position[0] == last_row:
            return 1
        if manifold[position[0]+1][position[1]] == ".":
            return get_timelines((position[0]+1, position[1]))
        if manifold[position[0]+1][position[1]] == "^":
            return get_timelines((position[0], position[1]-1)) + get_timelines((position[0], position[1]+1))


    ans = get_timelines(start)

    print(f"\nAns: {ans}")

    # ans: 73007003089792




#----------------------------------------------------------------



# Data load and caling main()
#----------------------------------------------------------------
if __name__ == "__main__":
    # Prep Data
    rows: list[str]

    if len(sys.argv) == 1:
        # Paste test example data here
        test_data = """\
.......S.......
...............
.......^.......
...............
......^.^......
...............
.....^.^.^.....
...............
....^.^...^....
...............
...^.^...^.^...
...............
..^...^.....^..
...............
.^.^.^.^.^...^.
..............."""
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


