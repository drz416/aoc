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
xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))"""
        lines = test_data.splitlines()
    else:
        data_file = Path.cwd() / "puzzle_data.txt"
        with open(data_file, "r") as f:
            lines = f.readlines()

    for i, line in enumerate(lines):
        lines[i] = line.strip()

    # Puzzle code
    #----------------------------------------------------------------

    # flatten lines
    flat_line = ""
    for line in lines:
        flat_line += line

    # parse out only do() instructions
    do = True
    do_instructions = ""
    index = 0
    
    while index < len(flat_line):
        # check for don't(), = 7 char
        if flat_line[index: index+7] == "don't()":
            do = False
            index += 7
            continue
        # check for do(), = 4 char
        if flat_line[index: index+4] == "do()":
            do = True
            index += 4
            continue
        if do:
            do_instructions += flat_line[index]
        index += 1
    
    print(do_instructions)


    pattern = re.compile(r"mul\((\d{1,3}),(\d{1,3})\)")

    total = 0
    matches = pattern.findall(do_instructions)
    print(matches)
    
    for match in matches:
        total += int(match[0]) * int(match[1])

    print(f"Total: {total}")

    # ans: 106780429


    



if __name__ == "__main__":
    main(sys.argv)


