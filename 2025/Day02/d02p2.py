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


def all_equal(number: str) -> bool:
    # return true if all digits are equal
    repeating_c = number[0]
    for c in number:
        if c != repeating_c:
            return False
    return True

def print_flagged(text: str, flag: bool) -> None:
    if flag:
        print(text)

PRINT_FLAG = True
invalid_ids = set()

def main(lines: list[str]):
    p_ranges: list(str) = lines[0].split(",")

    for p_range in p_ranges:
        # for each range
        [a, b] = p_range.split("-")

        for num_id in range(int(a), int(b)+1):
            # scan through all the digits
            id = str(num_id)
            len_id = len(id)

            if len_id < 2:
                continue

            if all_equal(id):
                # check if all the digits repeat
                invalid_ids.add(num_id)
                print_flagged(id, PRINT_FLAG)
                continue

            match len_id:
                case 4:
                    if id[0:2] == id[2:4]:
                        print_flagged(id, PRINT_FLAG)
                        invalid_ids.add(num_id)
                        continue
                case 6:
                    if id[0:2] == id[2:4] == id[4:6]:
                        print_flagged(id, PRINT_FLAG)
                        invalid_ids.add(num_id)
                        continue
                    if id[0:3] == id[3:6]:
                        print_flagged(id, PRINT_FLAG)
                        invalid_ids.add(num_id)
                        continue
                case 8:
                    if id[0:2] == id[2:4] == id[4:6] == id[6:8]:
                        print_flagged(id, PRINT_FLAG)
                        invalid_ids.add(num_id)
                        continue
                    if id[0:4] == id[4:8]:
                        print_flagged(id, PRINT_FLAG)
                        invalid_ids.add(num_id)
                        continue
                case 9:
                    if id[0:3] == id[3:6] == id[6:9]:
                        print_flagged(id, PRINT_FLAG)
                        invalid_ids.add(num_id)
                        continue
                case 10:
                    if id[0:2] == id[2:4] == id[4:6] == id[6:8] == id[8:10]:
                        print_flagged(id, PRINT_FLAG)
                        invalid_ids.add(num_id)
                        continue
                    if id[0:5] == id[5:10]:
                        print_flagged(id, PRINT_FLAG)
                        invalid_ids.add(num_id)
                        continue

    ans = sum(invalid_ids)
                




    print("")
    print(f"Ans: {ans}")

    # too high 17310295458
    # too high 17298174246
    # ans: ####




#----------------------------------------------------------------



# Data load and caling main()
#----------------------------------------------------------------
if __name__ == "__main__":
    # Prep Data
    lines: list[str]

    if len(sys.argv) == 1:
        # Paste test example data here
        test_data = """\
11-22,95-115,998-1012,1188511880-1188511890,222220-222224,\
1698522-1698528,446443-446449,38593856-38593862,565653-565659,\
824824821-824824827,2121212118-2121212124"""
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


