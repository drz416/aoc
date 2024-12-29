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
###############
#...#...#.....#
#.#.#.#.#.###.#
#S#...#.#.#...#
#######.#.#.###
#######.#.#...#
#######.#.###.#
###..E#...#...#
###.#######.###
#...###...#...#
#.#####.#.###.#
#.#...#.#.#...#
#.#.#.#.#.#.###
#...#...#...###
###############"""
        lines = test_data.splitlines()
    else:
        data_file = Path.cwd() / "puzzle_data.txt"
        with open(data_file, "r") as f:
            lines = f.readlines()

    for i, line in enumerate(lines):
        lines[i] = line.strip()

    # Puzzle code
    #----------------------------------------------------------------

    grid: list[list[str]] = []
    for i, line in enumerate(lines):
        grid.append(list(line))
    
    m, n = len(grid), len(grid[0])
    for row in range(m):
        for col in range(n):
            if grid[row][col] == 'S':
                S = (row, col)
            elif grid[row][col] == 'E':
                E = (row, col)

    queue = deque([(*S, 0, dict())])
    while queue:
        x, y, time, visited = queue.popleft()
        visited[(x, y)] = time

        if (x, y) == E:
            break

        for i, j in [(x+1, y), (x-1, y), (x, y-1), (x, y+1)]:
            if (i in range(m) and
                j in range(n) and
                (i, j) not in visited and
                grid[i][j] != '#'
            ):
                queue.append((i, j, time + 1, visited.copy()))

    cheats = 0
    threshold = 100
    path = sorted(visited, key=visited.get)
    for t2 in range(threshold, len(path)):
        for t1 in range(t2 - threshold):
            x1, y1 = path[t1]
            x2, y2 = path[t2]
            distance = abs(x1-x2) + abs(y1-y2)
            if distance <= 20 and t2 - t1 - distance >= threshold:
                cheats += 1
    
    print(cheats)

    # This is an internet solution: https://github.com/mgtezak/Advent_of_Code/blob/master/2024/20/p2.py
    # ans: 983905



    




if __name__ == "__main__":
    main(sys.argv)


