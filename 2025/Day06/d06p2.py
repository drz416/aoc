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

from math import prod

def main(rows: list[str]):

    operators: list[str] = rows.pop()

    ans = 0
    values = []
    for col in reversed(range(len(operators))):
        # Scan through each column from right to left (backwards) and
        # construct values (top to bottom)
        val = ""
        for row in rows:
            digit = row[col]
            val += "" if digit == " " else digit
        if val == "":
            values = []
            continue
        values.append(int(val))

        if operators[col] == " ":
            pass
        elif operators[col] == "+":
            ans += sum(values)
            continue
        else:
            ans += prod(values)
    
    print(f"\nAns: {ans}")

    # ans: 8674740488592




#----------------------------------------------------------------



# Data load and caling main()
#----------------------------------------------------------------
if __name__ == "__main__":
    # Prep Data
    rows: list[str]

    if len(sys.argv) == 1:
        # Paste test example data here
        test_data = """\
123 328  51 64 
 45 64  387 23 
  6 98  215 314
*   +   *   +  """
        rows = test_data.splitlines()
    else:
        data_file = Path.cwd() / "puzzle_data.txt"
        with open(data_file, "r") as f:
            rows = f.readlines()

    # for i, line in enumerate(rows):
    #     rows[i] = line.strip()
    
    start_time = time()
    main(rows)
    print("")
    print(f"Time in main(): {time() - start_time:.06f}s")
#----------------------------------------------------------------


