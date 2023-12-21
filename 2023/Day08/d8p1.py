import re

import sys
from pathlib import Path

# Run module via python3 -m d#p#, any argument passed uses puzzle data
# no argument passed uses test data 

def main(argv: list[str]):
    # Prep Code
    lines: list[str]

    if len(argv) == 1:
        test_data = """\
LLR

AAA = (BBB, BBB)
BBB = (AAA, ZZZ)
ZZZ = (ZZZ, ZZZ)"""
        lines = test_data.splitlines()
    else:
        data_file = Path.cwd() / "puzzle_data.txt"
        with open(data_file, "r") as f:
            lines = f.readlines()

    for i, line in enumerate(lines):
        lines[i] = line.strip()

    # Puzzle code
    directions = lines.pop(0)
    lines.pop(0)        #remove blank
    direction = gen_direction(directions)
    
    pattern = r"([A-Z][A-Z][A-Z])\s=\s\(([A-Z][A-Z][A-Z]),\s([A-Z][A-Z][A-Z])\)"
    p_obj = re.compile(pattern)

    maps = {}
    for line in lines:
        parsed = p_obj.findall(line)[0]
        maps[parsed[0]] = (parsed[1], parsed[2])

    position = 'AAA'
    steps = 0

    while True:
        position = maps[position][next(direction)]
        steps += 1
        print(position, steps)
        if position == 'ZZZ':
            break






def gen_direction(directions: str) -> int:
    i = -1
    while True:
        i += 1
        if i >= len(directions):
            i = 0
        yield 0 if directions[i] == 'L' else 1
        #yield directions[i]


main(sys.argv)