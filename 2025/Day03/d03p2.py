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

def largest_digit(sub_bank: str) -> tuple[str]:
    """Find the largest digit in a subset of the bank, and return the batteries
    before it, the largest battery, and the batteries after it """
    b_max = "0"
    i_max = -1
    for i, battery in enumerate(sub_bank):
        if battery > b_max:
            b_max = battery
            i_max = i
        if battery == 9:
            break
    return (
        sub_bank[0:i_max],
        b_max,
        sub_bank[i_max+1:]
    )



def main(lines: list[str]):

    banks = lines
    ans = 0

    for bank in banks:
        selected_batteries = []
        remaining_bank = bank
        while True:
            split_index = len(remaining_bank) - (12 - len(selected_batteries)) + 1
            possible_batteries = remaining_bank[0:split_index]
            unselectable_batteries = remaining_bank[split_index:]
            _, b_max, remainder = largest_digit(possible_batteries)
            selected_batteries.append(b_max)
            remaining_bank = remainder + unselectable_batteries
            
            if len(selected_batteries) == 12:
                break
        
        max_battery = "".join(selected_batteries)
        print(max_battery)
        ans += int(max_battery)


    print("")
    print(f"Ans: {ans}")

    # ans: 170520923035051
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


