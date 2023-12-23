import sys
from pathlib import Path

# Run with test data    -> python3 -m d#p#
# Run with puzzle data  -> python3 -m d#p# X (any argument)

def main(argv: list[str]):
    # Prep Code
    lines: list[str]

    if len(argv) == 1:
        test_data = """\
...#......
.......#..
#.........
..........
......#...
.#........
.........#
..........
.......#..
#...#....."""
        lines = test_data.splitlines()
    else:
        data_file = Path.cwd() / "puzzle_data.txt"
        with open(data_file, "r") as f:
            lines = f.readlines()

    for i, line in enumerate(lines):
        lines[i] = line.strip()

    # Puzzle code
    #----------------------------------------------------------------

    # Expand the galaxy, rows first
    expanded_rows: list[str] = []
    for line in lines:
        expanded_rows.append(line)
        if line == '.' * len(line):
            expanded_rows.append(line)

    # Check empty columns
    empty_columns: list[int] = []
    for j in range(len(lines[0])):
        for i in range(len(lines)):
            if lines[i][j] != '.':
                break
        else:
            empty_columns.append(j)
        
    # Expand the galaxy, columns next
    expanded_galaxy: list[str] = []
    for row in expanded_rows:
        string = ''
        for j, c in enumerate(row):
            string += c
            if j in empty_columns:
                string += '.'
        expanded_galaxy.append(string)

    galaxies: set[tuple[int]] = set()
    for i, line in enumerate(expanded_galaxy):
        for j, c in enumerate(line):
            if c == '#':
                galaxies.add((i, j))

    print(galaxies)

    total_distance = 0
    for galaxy in galaxies:
        for other_galaxy in galaxies:
            row_distance = abs(other_galaxy[0] - galaxy[0])
            column_distance = abs(other_galaxy[1] - galaxy[1])
            distance = row_distance + column_distance
            total_distance += distance
            print(galaxy, other_galaxy,distance, total_distance)

    print("Total distance: ", total_distance/2)

#    for line in expanded_galaxy:
#        print(line)


    




main(sys.argv)


