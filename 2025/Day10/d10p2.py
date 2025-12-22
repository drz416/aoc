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

    wirings: list[list[tuple[int]]] = []
    joltages: list[tuple[int]] = []

    # eg: [.##.] (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}
    pattern_outer = r'\[(.+)\]' + r'.+' + r'\{(.+)\}'
    pattern_inner = r'\((.+?)\)'
    pobj_out = re.compile(pattern_outer)
    pobj_in = re.compile(pattern_inner)

    for row in rows:
        # Read in joltage requirements, store in tuple
        _, jolts = pobj_out.findall(row)[0]
        jolts: str
        joltages.append(tuple(map(int, jolts.split(","))))
        digits = len(joltages[-1])

        # Read in button wirings, and inteprent which positions of joltage
        # requirements they affect
        wrgs_all = pobj_in.findall(row)
        wrgs = []
        for w in wrgs_all:
            wrgs_acc = [0]*digits
            for dig in w.split(","):
                wrgs_acc[int(dig)] = 1
            wrgs.append(tuple(wrgs_acc))
        wirings.append(wrgs)

    def check_if_greater(curr_joltage: tuple[int], target_joltage: tuple[int]) -> bool:
        for cj, tj in zip(curr_joltage, target_joltage):
            if cj > tj:
                return True
        return False

    def find_min(presses: int,
                 wiring: list[list[tuple[int]]],
                 target_joltage: tuple[int],
                 curr_joltage: tuple[int]) -> int:
        nonlocal min_presses

        presses += 1

        if presses >= min_presses:
            return

        for button in wiring:
            joltage = tuple(cj + bt for cj, bt in zip(curr_joltage, button))
            if joltage == target_joltage:
                min_presses = presses
                return
            if check_if_greater(joltage, target_joltage):
                continue
            find_min(presses, wiring, target_joltage, joltage)

        return

    # Go through each machine and determine minimum presses
    ans = 0
    for wiring, target_joltage in zip(wirings, joltages):
        min_presses = 99999
        # breakpoint()
        # At each machine, test out all combinations, recursively, and stop recursion
        # if a branch reaches a numeber of presses that's larger than a found
        # minimum, or if it reaches joltage requirements that are larger than the 
        # requirement

        find_min(0, wiring, target_joltage, tuple([0]*len(target_joltage)))
        
        ans += min_presses
        print(f"{min_presses=}, {ans=}")


    print(f"\nAns: {ans}")

    # ans: ##




#----------------------------------------------------------------



# Data load and caling main()
#----------------------------------------------------------------
if __name__ == "__main__":
    # Prep Data
    rows: list[str]

    if len(sys.argv) == 1:
        # Paste test example data here
        test_data = """\
[.##.] (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}
[...#.] (0,2,3,4) (2,3) (0,4) (0,1,2) (1,2,3,4) {7,5,12,7,2}
[.###.#] (0,1,2,3,4) (0,3,4) (0,1,2,4,5) (1,2) {10,11,11,5,10,5}"""
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


