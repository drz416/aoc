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

    # Delmit each row by consecurtive spaces, built-into str.split()
    rows: list[list[str]] = []
    for line in lines:
        rows.append(line.split())
    
    operators: list[str] = rows.pop()

    # Go through each problem and perform math
    num_values = len(rows)
    
    ans = 0
    for i_prob, operator in enumerate(operators):
        if operator == "+":
            prob_ans = 0
            for i_val in range(num_values):
                prob_ans += int(rows[i_val][i_prob])
        else:                                   # opeartor == "*"
            prob_ans = 1
            for i_val in range(num_values):
                prob_ans *= int(rows[i_val][i_prob])
        ans += prob_ans
    
    print(f"\nAns: {ans}")

    # ans: 4878670269096




#----------------------------------------------------------------



# Data load and caling main()
#----------------------------------------------------------------
if __name__ == "__main__":
    # Prep Data
    lines: list[str]

    if len(sys.argv) == 1:
        # Paste test example data here
        test_data = """\
123 328  51 64 
 45 64  387 23 
  6 98  215 314
*   +   *   +  """
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


