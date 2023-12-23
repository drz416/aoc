import sys
from pathlib import Path

# Run with test data    -> python3 -m d#p#
# Run with puzzle data  -> python3 -m d#p# X (any argument)

def main(argv: list[str]):
    # Prep Code
    lines: list[str]

    if len(argv) == 1:
        test_data = """\
-L|F7
7S-7|
L|7||
-L-J|
L|-JF"""
        lines = test_data.splitlines()
    else:
        data_file = Path.cwd() / "puzzle_data.txt"
        with open(data_file, "r") as f:
            lines = f.readlines()

    for i, line in enumerate(lines):
        lines[i] = line.strip()

    # Puzzle code
    #----------------------------------------------------------------

    # find S
    found = False
    row = 0
    column = 0
    for i, line in enumerate(lines):
        for j, c in enumerate(line):
            if c == 'S':
                row = i
                column = j
                found = True
                break
        if found:
            break

    print(f"0 S ({row}, {column})")

    # Define directions
    # Key is pipe standing on, tuple is direction going with 2 possibilities
    # for each of 4 directions (0-3), counted clockwise from top
    directions = {'|': (2, None, 0, None),
                  '-': (None, 3, None, 1),
                  'F': (None, 2, 1, None),
                  '7': (None, None, 3, 2),
                  'J': (3, None, None, 0),
                  'L': (1, 0, None, None),}

    # take first step
    came_from = None
    if lines[row-1][column] in {'7', '|', 'F'}:
        pipe = lines[row-1][column]
        came_from = 2
        row -= 1
    elif lines[row][column+1] in {'J', '-', '7'}:
        pipe = lines[row][column+1]
        came_from = 3
        column += 1
    else:
        pipe = lines[row+1][column]
        came_from = 0
        row += 1
    step = 1
    print(step, pipe)

    # traverse pipes
    while pipe != 'S':
        step += 1
        new_direction = directions[pipe][came_from]
        if new_direction == 0:
            row -= 1
            came_from = 2
        elif new_direction == 1:
            column += 1
            came_from = 3
        elif new_direction == 2:
            row += 1
            came_from = 0
        else:
            column -= 1
            came_from = 1
        pipe = lines[row][column]
        
        print(step, pipe)
    
    print(f"Furthest: {int(step / 2)}")





main(sys.argv)

