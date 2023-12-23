import sys
from pathlib import Path

# Run with test data    -> python3 -m d#p#
# Run with puzzle data  -> python3 -m d#p# X (any argument)

def main(argv: list[str]):
    # Prep Code
    lines: list[str]

    if len(argv) == 1:
        test_data = """\
...........
.S-------7.
.|F-----7|.
.||.....||.
.||.....||.
.|L-7.F-J|.
.|..|.|..|.
.L--J.L--J.
..........."""
        lines = test_data.splitlines()
    else:
        data_file = Path.cwd() / "puzzle_data.txt"
        with open(data_file, "r") as f:
            lines = f.readlines()

    for i, line in enumerate(lines):
        lines[i] = line.strip()

    # Puzzle code
    #----------------------------------------------------------------
    # This solution uses the RAY CASTING ALGORITHM
    # https://en.wikipedia.org/wiki/Point_in_polygon
    # Crosses 1 boundary -> inside polygon
    # Crosses 2 boundaries -> outside polygon


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

    # Create a set that tracks boundary positions, insert start position
    boundary: set[tuple[int]] = set()
    boundary.add((row, column))

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
    boundary.add((row, column))
    #print(step, pipe)

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
        boundary.add((row, column))
        
        #print(step, pipe)
    
    print(f"Furthest: {int(step / 2)}")

    # Replace 'S' with correct symbol

    # Count boundary crosses
    inside_count = 0
    inside_list = []
    for i, line in enumerate(lines):
        for j, c in enumerate(line):
            crosses = 0
            if (i, j) in boundary:
                continue
            if j == len(line) - 1:
                continue
            for k, cursor in enumerate(line[j+1:]):
                if (i, j+k+1) not in boundary:
                    continue
                if cursor in {'|', '7', 'F'}: #for sample data, need to include 'S' here, not for puzzle data
                    crosses += 1
                    
            if crosses % 2 == 1:
                inside_count += 1
                inside_list.append((i, j))
    
    print('Inside: ', inside_count)



main(sys.argv)

