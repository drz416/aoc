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

    banks = lines
    ans = 0

    for bank in banks:
        # Find maximum in the first n-1 batteries. It's the last digit once sorted
        first_highest_digit = sorted(bank[:-1])[-1]
        # Isolate the remaining digits
        remainder = bank.split(first_highest_digit, maxsplit=1)[1]
        # Find highest from remainder
        second_heighest_digit = sorted(remainder)[-1]

        highest_digit = int(first_highest_digit+second_heighest_digit)
        ans += highest_digit
        print(highest_digit, ans)


    print("")
    print(f"Ans: {ans}")

    # ans: 17229
#----------------------------------------------------------------




# Data load and caling main()
#----------------------------------------------------------------
if __name__ == "__main__":
    # Prep Data
    lines: list[str]

    if len(sys.argv) == 1:
        # Paste test example data here
        test_data = """\
987654321111111
811111111111119
234234234234278
818181911112111"""
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


