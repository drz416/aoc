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

    # Define all directions, starting at 12 o clock
    directions = {
        0: [(0,0), (-1,0), (-2,0), (-3,0)],
        1: [(0,0), (-1,1), (-2,2), (-3,3)],
        2: [(0,0), (0,1), (0,2), (0,3)],
        3: [(0,0), (1,1), (2,2), (3,3)],
        4: [(0,0), (1,0), (2,0), (3,0)],
        5: [(0,0), (1,-1), (2,-2), (3,-3)],
        6: [(0,0), (0,-1), (0,-2), (0,-3)],
        7: [(0,0), (-1,-1), (-2,-2), (-3,-3)], 
    }

    total = 0
    for x in range(rows):
        for y in range(columns):
            sub_total = check_directions(grid, directions, x, y, rows, columns)
            total += sub_total

            suffix = ""
            if grid[x][y] == "X":
                suffix = "<--- X"
            print(f"({x}, {y}): {sub_total=} {suffix}")

    #print(check_directions(grid, directions, 9, 1, rows, columns))

    print(f"Total: {total}")

    # ans: 2390



def check_directions(grid: list[list[str]], directions: dict, x, y, rows, columns) -> int:
    if grid[x][y] != "X":
        return 0
    count = 0
    for direction in directions.values():
        word = ""
        for (dx, dy) in direction:
            if (0 <= x+dx < rows) and (0 <= y+dy < columns):
                word += grid[x+dx][y+dy]
        if word == "XMAS":
            count += 1
        print((x, y), direction, word, count)
    return count



if __name__ == "__main__":
    main(sys.argv)


