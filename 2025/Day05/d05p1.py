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

def main(lines: list[str]):

    fresh_ranges: list[tuple[int]] = []
    ingredients: list[int] = []

    in_ingredients = False
    for line in lines:
        if in_ingredients:
            ingredients.append(int(line))
        elif line == "":
            in_ingredients = True
        else:
            start, end = line.split("-")
            fresh_ranges.append((int(start), int(end)))

    ans = 0
    for ingredient in ingredients:
        for fresh_range in fresh_ranges:
            # Compare each range with selected ingredient, if it's within range
            # mark it as fresh, and go onto next ingredient
            if fresh_range[0] <= ingredient <= fresh_range[1]:
                ans += 1
                break

    print("")
    print(f"Ans: {ans}")

    # ans: 601




#----------------------------------------------------------------



# Data load and caling main()
#----------------------------------------------------------------
if __name__ == "__main__":
    # Prep Data
    lines: list[str]

    if len(sys.argv) == 1:
        # Paste test example data here
        test_data = """\
3-5
10-14
16-20
12-18

1
5
8
11
17
32"""
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


