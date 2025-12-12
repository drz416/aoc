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

    # Read in the ranges, convert them to int and sort them
    raw_ranges: list[tuple[int]] = []
    for line in lines:
        if line == "":
            break
        start, end = line.split("-")
        raw_ranges.append((int(start), int(end)))
    raw_ranges.sort()

    # Inspect and combine the ranges on a stack, pull out when not overlapping
    que_ranges: deque[tuple[int]] = deque(raw_ranges)
    que_merged: deque[tuple[int]] = deque()
    while True:
        if len(que_ranges) == 1:
            que_merged.append(que_ranges.popleft())
            break
        a_min, a_max = que_ranges.popleft()
        b_min, b_max = que_ranges.popleft()
        
        if b_min > a_max:
            que_merged.append((a_min, a_max))
            que_ranges.appendleft((b_min, b_max))
        else:
            que_ranges.appendleft((a_min, max(a_max, b_max)))

    ans = 0
    while que_merged:
        a_min, a_max = que_merged.popleft()
        ans += a_max - a_min + 1

    print(f"\nAns: {ans}")

    # ans: 367899984917516

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
"""
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


