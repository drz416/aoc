import sys
import re
from pathlib import Path
from pprint import pprint
from time import time, time_ns
from collections import deque, Counter, defaultdict
from functools import partial, lru_cache
from itertools import product, combinations

# Run with test data    -> python3 -m d#p#
# Run with puzzle data  -> python3 -m d#p# X (any argument)


locks: list[tuple[int]] = []
keys: list[tuple[int]] = []

def main(objects: list[str]):

    for obj in objects:
        if obj[0] == "#":
            locks.append(get_lock_heights(obj))
        else:
            keys.append(get_key_heights(obj))

    total = 0
    for lock, key in product(locks, keys):
        total += 1 if check_fit(lock, key) else 0

    print(f"Total: {total}")

    # ans: 3356







def get_lock_heights(lock: str) -> tuple[int]:
    heights = {}
    for x, row in enumerate(lock.split("\n")):
        for y, position in enumerate(row):
            if position == ".":
                heights.setdefault(y, x-1)
    return tuple(heights[i] for i in range(5))

def get_key_heights(key: str) -> tuple[int]:
    heights = {}
    for x, row in enumerate(key.split("\n")):
        for y, position in enumerate(row):
            if position == "#":
                heights.setdefault(y, 6-x)
    return tuple(heights[i] for i in range(5))

def check_fit(lock: tuple[str], key: tuple[str]) -> bool:
    for l_pin, key_pin in zip(lock, key):
        if key_pin >= (6-l_pin):
            return False
    return True



# Setup code
#----------------------------------------------------------------

if __name__ == "__main__":
    # Prep Code
    lines: list[str]

    if len(sys.argv) == 1:
        test_data = """\
#####
.####
.####
.####
.#.#.
.#...
.....

#####
##.##
.#.##
...##
...#.
...#.
.....

.....
#....
#....
#...#
#.#.#
#.###
#####

.....
.....
#.#..
###..
###.#
###.#
#####

.....
.....
.....
#....
#.#..
#.#.#
#####"""
        objects = test_data.split("\n\n")
    else:
        data_file = Path.cwd() / "puzzle_data.txt"
        with open(data_file, "r") as f:
            objects = f.read().split("\n\n")
    
    start_time = time()
    main(objects)
    print("")
    print(f"Time in main(): {time() - start_time:.06f}s")


