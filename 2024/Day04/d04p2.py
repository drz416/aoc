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
MMMSXXMASM
MSAMXMSMSA
AMXSXMAAMM
MSAMASMSMX
XMASAMXAMM
XXAMMXXAMA
SMSMSASXSS
SAXAMASAAA
MAMMMXMMMM
MXMXAXMASX"""
        lines = test_data.splitlines()
    else:
        data_file = Path.cwd() / "puzzle_data.txt"
        with open(data_file, "r") as f:
            lines = f.readlines()

    for i, line in enumerate(lines):
        lines[i] = line.strip()

    # Puzzle code
    #----------------------------------------------------------------

    rows = len(lines)
    columns = len(line)

    grid: list[list[str]] = []
    for line in lines:
        grid.append(list(line))

    # Possible X-MASs
    # M S  M M  S M  S S
    #  A    A    A    A
    # M S  S S  S M  M M

    # Clockwise combinations
    # MSSM
    # MMSS
    # SMMS
    # SSMM

    # Indexing needed
    # [(-1,-1), (-1,1), (1,1), (1,-1)]

    # Define all directions, starting at 12 o clock
    directions = [(-1,-1), (-1,1), (1,1), (1,-1)]

    total = 0
    for x in range(rows-2):
        x += 1
        for y in range(columns-2):
            y += 1
            if grid[x][y] != "A":
                continue
            
            sub_total = check_xmas(grid, directions, x, y)
            total += sub_total

            suffix = ""
            if grid[x][y] == "X":
                suffix = "<--- X"
            print(f"({x}, {y}): {sub_total=} {suffix}")

    print(f"Total: {total}")

    # ans: 1809


def check_xmas(grid: list[list[str]], directions: list[tuple[int]], x, y) -> int:
    word = ""
    for (dx, dy) in directions:
        word += grid[x+dx][y+dy]
    if word in {"MSSM", "MMSS", "SMMS", "SSMM"}:
        return 1
    print(word)
    return 0



if __name__ == "__main__":
    main(sys.argv)


