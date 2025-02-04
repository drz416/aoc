import sys
import re
from collections import deque, Counter, defaultdict
from pathlib import Path
from pprint import pprint
from functools import partial, lru_cache


# Run with test data    -> python3 -m d#p#
# Run with puzzle data  -> python3 -m d#p# X (any argument)

def main(argv: list[str]):
    # Prep Code
    lines: list[str]

    if len(argv) == 1:
        test_data = """\
3   4
4   3
2   5
1   3
3   9
3   3"""
        lines = test_data.splitlines()
    else:
        data_file = Path.cwd() / "puzzle_data.txt"
        with open(data_file, "r") as f:
            lines = f.readlines()

    for i, line in enumerate(lines):
        lines[i] = line.strip()

    # Puzzle code
    #----------------------------------------------------------------

    left_list: list[int] = []
    right_list: list[int] = []

    for line in lines:
        s = line.split("   ")
        left_list.append(int(s[0]))
        right_list.append(int(s[1]))

    cntr = Counter()
    cntr.update(right_list)

    total = 0

    for left_element in left_list:
        total += left_element * cntr[left_element]

    print(f"Total: {total}")

    # ans: 25358365


if __name__ == "__main__":
    main(sys.argv)


