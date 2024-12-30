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
1
10
100
2024"""
        lines = test_data.splitlines()
    else:
        data_file = Path.cwd() / "puzzle_data.txt"
        with open(data_file, "r") as f:
            lines = f.readlines()

    for i, line in enumerate(lines):
        lines[i] = line.strip()

    # Puzzle code
    #----------------------------------------------------------------

    # Setup containers

    ans = 0
    for line in lines:
        secret = int(line)
        for _ in range(2000):
            secret = evolution3(evolution2(evolution1(secret)))
        # print(f"{line}: {secret}")
        ans += secret


    print(f"Ans: {ans}")

    # ans: 20401393616

def evolution1(number: int) -> int:
    return ((number * 64) ^ number) % 16_777_216

def evolution2(number: int) -> int:
    return ((number // 32) ^ number) % 16_777_216

def evolution3(number: int) -> int:
    return ((number * 2048) ^ number) % 16_777_216


if __name__ == "__main__":
    main(sys.argv)


