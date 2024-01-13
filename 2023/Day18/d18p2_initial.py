import re
from pprint import pprint

import sys
from pathlib import Path

# Run with test data    -> python3 -m d#p#
# Run with puzzle data  -> python3 -m d#p# X (any argument)

def main(argv: list[str]):
    # Prep Code
    lines: list[str]

    if len(argv) == 1:
        test_data = """\
R 6 (#70c710)
D 5 (#0dc571)
L 2 (#5713f0)
D 2 (#d2c081)
R 2 (#59c680)
D 2 (#411b91)
L 5 (#8ceee2)
U 2 (#caa173)
L 1 (#1b58a2)
U 2 (#caa171)
R 2 (#7807d2)
U 3 (#a77fa3)
L 2 (#015232)
U 2 (#7a21e3)"""
        lines = test_data.splitlines()
    else:
        data_file = Path.cwd() / "puzzle_data.txt"
        with open(data_file, "r") as f:
            lines = f.readlines()

    for i, line in enumerate(lines):
        lines[i] = line.strip()

    # Puzzle code
    #----------------------------------------------------------------

    direction: tuple[int]
    directions = {3: (-1, 0),     # U
                  0: (0, 1),      # R
                  1: (1, 0),      # D
                  2: (0, -1)      # L
                  }

    trench = {}
    position = (0, 0)
    min_r = 0
    max_r = 0
    min_c = 0
    max_c = 0

    pattern = r'(?P<unused1>.)\s(?P<unused2>.*)\s\(#(?P<encoding>.*)\)'
    p_obj = re.compile(pattern)

    # Explore trench
    for line in lines:
        encoding = p_obj.search(line)['encoding']
        direction = directions[int(encoding[-1])]
        length = int(encoding[0:-1], 16)
        
        for _ in range(length):
            position = (position[0]+direction[0], position[1]+direction[1])
            min_r = min(min_r, position[0])
            max_r = max(max_r, position[0])
            min_c = min(min_c, position[1])
            max_c = max(max_c, position[1])
            trench.setdefault(position[0], []).append(position)
 
    # Normalize trench to (0,0)
    offset_r = -min_r
    offset_c = -min_c

    n_trench = set()
    print(min_r, max_r, min_c, max_c)
    print(len(trench))

    print(trench[0][:5], '...')

    sys.exit()

    while trench:
        position = trench.pop()
        n_trench.add((position[0]+offset_r, position[1]+offset_c))


    print(len(n_trench))

    sys.exit()

    # for row in grid:
    #     print(row)
    #     # print("".join(row))
    # print('')

    # Fill dig pool from trench
    len_c = len(grid[0])
    len_r = len(grid)

    for i, row in enumerate(grid):
        if i == len_r-1:
            continue
        for j, c in enumerate(row):
            if c == '#':
                continue
            # c == '.'
            crosses = 0
            for c_sweep in range(j+1, len_c):
                if grid[i][c_sweep] == '#' and grid[i+1][c_sweep] == '#':
                    crosses += 1
            if crosses % 2 == 0:
                continue
            grid[i][j] = '#'

    counter = 0
    for row in grid:
        # print(row)
        counter += row.count('#')
        # print("".join(row))
    
    print("Count: ", counter)
    


        
        



    


    


main(sys.argv)


