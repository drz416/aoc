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

    lights: list[int] = []
    wirings: list[list[int]] = []
    # joltages

    # eg: [.##.] (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}
    pattern_outer = r'\[(.+)\]' + r'.+' + r'\{(.+)\}'
    pattern_inner = r'\((.+?)\)'
    pobj_out = re.compile(pattern_outer)
    pobj_in = re.compile(pattern_inner)


    for row in rows:
        # Read in lights, convert string binary representation to integer
        lgts, jolts = pobj_out.findall(row)[0]
        digits = len(lgts)
        lgts = int("".join(map(lambda x: '1' if x == '#' else '0', lgts)), base=2)
        lights.append(lgts)

        # Read in button wirings, interpret as binary representation for xor function
        # then convert each binary representation to integer
        wrgs_all = pobj_in.findall(row)
        wrgs = []
        for w in wrgs_all:
            wrgs_acc = ['0']*digits
            for dig in w.split(","):
                wrgs_acc[int(dig)] = '1'
            wrgs.append(int("".join(wrgs_acc), base=2))
        wirings.append(wrgs)

    # Go through each machine and determine minimum presses
    ans = 0
    for light, wiring in zip(lights, wirings):
        min_presses = None
        
        # At each machine, test out all combinations, from lowest number of 
        # presses to highest number
        for num_presses in range(1, len(wiring)+1):
            # If a minimum is found, ignore any higher presses
            if min_presses != None:
                break
            for combs in combinations(wiring, num_presses):
                if min_presses != None:
                    break
                light_state = 0
                for button in combs:
                    light_state = light_state ^ button              # XOR to flip the lights
                    if light_state == light:
                        min_presses = num_presses
                        break

        ans += min_presses


    print(f"\nAns: {ans}")

    # ans: 419




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


