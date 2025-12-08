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

def normalize(start_position: int, end_position: int) -> bool(int):
    """This function takes a final position of the dial and normalizes it to
    a position between 0 and 99, it also counts passes through zero"""
    if end_position == 0 or end_position == 100:
        return (1, 0)
    if 0 < end_position < 100:
        return (0, end_position)
    
    if end_position < 0:
        passes = abs(end_position // 100)
        if start_position == 0:
            passes -= 1
        end_position = end_position % 100
        if end_position == 0:
            passes += 1
    else: # end_position > 100
        passes = end_position // 100
        end_position = end_position % 100

    return (passes, end_position)
    

def main(lines: list[str]):

    counter = 0
    dial = 50

    for line in lines:
        direction = 1 if line[0] == "R" else (-1)
        passes, dial = normalize(dial, dial + direction * int(line[1:]))
        # print(f"{line=}, {passes=}, {dial=}")
    
        counter += passes

    ans = counter


    print("")
    print(f"Ans: {ans}")

    # ans: 5961




#----------------------------------------------------------------



# Data load code, and invoking main()
#----------------------------------------------------------------
if __name__ == "__main__":
    # Prep Data
    lines: list[str]

    if len(sys.argv) == 1:
        # Paste test example data here
        test_data = """\
L68
L30
R48
L5
R60
L55
L1
L99
R14
L82"""
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


