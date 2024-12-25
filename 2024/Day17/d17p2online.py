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
Register A: 2024
Register B: 0
Register C: 0

Program: 0,3,5,4,3,0"""
        lines = test_data.splitlines()
    else:
        data_file = Path.cwd() / "puzzle_data.txt"
        with open(data_file, "r") as f:
            lines = f.readlines()

    for i, line in enumerate(lines):
        lines[i] = line.strip()

    # Puzzle code
    #----------------------------------------------------------------

    for line in lines:
        if line.startswith("Register A"):
            a = [int(line.split(": ")[1])]
        elif line.startswith("Register B"):
            b = [int(line.split(": ")[1])]
        elif line.startswith("Register C"):
            c = [int(line.split(": ")[1])]
        elif line.startswith("Program"):
            prog = line.split(": ")[1]
            prog = list(map(int, prog.split(",")))
        else:
            pass
    

    print(find(prog, 0))
    # ans: 216148338630253


def find(program, ans):
    if program == []:
        return ans
    for t in range(8):
        a = ans << 3 | t
        b = a % 8
        b = b ^ 3
        c = a >> b
        b = b ^ 5
        b = b ^ c
        if b % 8 == program[-1]:
            sub = find(program[:-1], a)
            if sub is None:
                continue
            return sub
        






if __name__ == "__main__":
    main(sys.argv)


