import sys
import re
from collections import deque, Counter, defaultdict
from pathlib import Path
from pprint import pprint
from functools import partial, lru_cache
from itertools import product, combinations

# Run with test data    -> python3 -m d#p#
# Run with puzzle data  -> python3 -m d#p# X (any argument)

def main(argv: list[str]):
    # Prep Code
    lines: list[str]

    if len(argv) == 1:
        test_data = """\
2333133121414131402"""
        lines = test_data.splitlines()
    else:
        data_file = Path.cwd() / "puzzle_data.txt"
        with open(data_file, "r") as f:
            lines = f.readlines()

    for i, line in enumerate(lines):
        lines[i] = line.strip()

    # Puzzle code
    #----------------------------------------------------------------

    disk_map = lines[0]
    disk: list[int] = []

    file = True
    id = 0
    for c in disk_map:
        if file:
            disk.extend([id] * int(c))
            id += 1
            file = False
        elif (file == False) and (c == "0"):
            # no space between files, do nothing
            file = True
        else:
            disk.extend([-1] * int(c))
            file = True

    print(disk)
    back = len(disk) - 1
    
    for front in range(len(disk)):
        # print("front", disk[front])
        if disk[front] != -1:
            continue
        while back > front:
            # print("back", disk[back])
            if disk[back] != -1:
                disk[front] = disk[back]
                disk[back] = -1
                back -= 1
                break
            back -= 1

    print(disk)

    total = 0
    for i, c in enumerate(disk):
        if c != -1:
            total += i * c


    print(f"Total: {total}")
    # ans: 6283404590840




if __name__ == "__main__":
    main(sys.argv)


