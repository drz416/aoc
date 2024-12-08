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
xmul(2,4)%&mul[3,7]!@^do_not_mul(5,5)+mul(32,64]then(mul(11,8)mul(8,5))
"""
        lines = test_data.splitlines()
    else:
        data_file = Path.cwd() / "puzzle_data.txt"
        with open(data_file, "r") as f:
            lines = f.readlines()

    for i, line in enumerate(lines):
        lines[i] = line.strip()

    # Puzzle code
    #----------------------------------------------------------------

    pattern = re.compile(r"mul\((\d{1,3}),(\d{1,3})\)")

    total = 0

    for line in lines:
        print(line)
        matches = pattern.findall(line)
        #print(matches)
    
        for match in matches:
            total += int(match[0]) * int(match[1])

    print(f"Total: {total}")

    # ans: 196826776


    



if __name__ == "__main__":
    main(sys.argv)


