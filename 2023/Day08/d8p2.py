import re
import math

import sys
from pathlib import Path

# Run module via python3 -m d#p#, any argument passed uses puzzle data
# no argument passed uses test data 

def main(argv: list[str]):
    # Prep Code
    lines: list[str]

    if len(argv) == 1:
        test_data = """\
LR

11A = (11B, XXX)
11B = (XXX, 11Z)
11Z = (11B, XXX)
22A = (22B, XXX)
22B = (22C, 22C)
22C = (22Z, 22Z)
22Z = (22B, 22B)
XXX = (XXX, XXX)"""
        lines = test_data.splitlines()
    else:
        data_file = Path.cwd() / "puzzle_data.txt"
        with open(data_file, "r") as f:
            lines = f.readlines()

    for i, line in enumerate(lines):
        lines[i] = line.strip()

    # Puzzle code
    #----------------------------------------------------------------
    directions = lines.pop(0)
    lines.pop(0)        #remove blank
    
    pattern = r"(..[A-Z])\s=\s\((..[A-Z]),\s(..[A-Z])\)"
    p_obj = re.compile(pattern)

    # Read in maps into a dict
    maps = {}
    for line in lines:
        parsed = p_obj.findall(line)[0]
        maps[parsed[0]] = (parsed[1], parsed[2])

    # Read in starting positions
    positions: list[str] = []
    steps: list[int] = []
    direction_gens: list[direction_gen] = []

    for key in maps.keys():
        if key[2] == 'A':
            positions.append(key)
            steps.append(0)
            direction_gens.append(direction_gen(directions))
    
    print(steps, positions)

    for i, direction in enumerate(direction_gens):
        j = 0
        while True:
            LR = next(direction)
            positions[i] = maps[positions[i]][LR]
            j += 1
            #print(j, LR, positions[i])
            if positions[i][2] == 'Z':
                steps[i] = j
                break

    print(steps, positions)
    print(math.lcm(*steps))

    #answer: 7309459565207




def direction_gen(directions: str) -> int:
    i = -1
    while True:
        i += 1
        if i >= len(directions):
            i = 0
        yield 0 if directions[i] == 'L' else 1


main(sys.argv)