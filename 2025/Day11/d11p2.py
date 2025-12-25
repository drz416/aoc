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

    devices: dict[str, list[str]] = {}
    for row in rows:
        name, outputs = row.split(": ")
        devices[name] = outputs.split()
    
    cache: dict[tuple, int] = {}            # had issues with lru_cache, created my own
    
    def paths_to_out(next_device: tuple[str, int, int]) -> int:
        nonlocal devices
        nonlocal cache

        if next_device in cache:
            return cache[next_device]
        if next_device[0] == "out":
            return 1 if next_device[1:3] == (1,1) else 0
        if next_device[0] == "dac":
            next_device = (next_device[0], 1, next_device[2])
        if next_device[0] == "fft":
            next_device = (next_device[0], next_device[1], 1)
        
        paths = 0
        for output in devices[next_device[0]]:
            paths_sub = paths_to_out((output, next_device[1], next_device[2]))
            cache[(output, next_device[1], next_device[2])] = paths_sub
            paths += paths_sub
        return paths

    ans = paths_to_out(("svr", 0, 0))

    
    print(f"\nAns: {ans}")

    # ans: 401398751986160




#----------------------------------------------------------------



# Data load and caling main()
#----------------------------------------------------------------
if __name__ == "__main__":
    # Prep Data
    rows: list[str]

    if len(sys.argv) == 1:
        # Paste test example data here
        test_data = """\
svr: aaa bbb
aaa: fft
fft: ccc
bbb: tty
tty: ccc
ccc: ddd eee
ddd: hub
hub: fff
eee: dac
dac: fff
fff: ggg hhh
ggg: out
hhh: out"""
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


