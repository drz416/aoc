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
7 6 4 2 1
1 2 7 8 9
9 7 6 2 1
1 3 2 4 5
8 6 4 4 1
1 3 6 7 9"""
        lines = test_data.splitlines()
    else:
        data_file = Path.cwd() / "puzzle_data.txt"
        with open(data_file, "r") as f:
            lines = f.readlines()

    for i, line in enumerate(lines):
        lines[i] = line.strip()

    # Puzzle code
    #----------------------------------------------------------------

    total_safe = 0

    for line in lines:
        report = line.split()
        report = str_to_int(report)
        
        if report[1] > report[0]:
            total_safe += check_increasing(report)
        elif report[1] < report[0]:
            total_safe += check_decreasing(report)

        print(f"{report}, {total_safe=}")

    
    print(f"Total: {total_safe}")

    # ans: 282



def check_increasing(report: list[int]) -> int:
    for i, elem in enumerate(report):
        if i == 0:
            pass
        elif (elem - curr_val) not in {1, 2, 3}:
            return 0
        curr_val = elem
    return 1


def check_decreasing(report: list[int]) -> int:
    for i, elem in enumerate(report):
        if i == 0:
            pass
        elif (elem - curr_val) not in {-1, -2, -3}:
            return 0
        curr_val = elem
    return 1

def str_to_int(report: list[str]) -> list[int]:
    new_list = []
    for elem in report:
        new_list.append(int(elem))
    return new_list
    



if __name__ == "__main__":
    main(sys.argv)


