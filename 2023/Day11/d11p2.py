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

    # Find empty rows
    empty_rows: list[int] = []
    for i, line in enumerate(lines):
        if line == '.' * len(line):
            empty_rows.append(i)
    print("Empty rows: ", empty_rows)

    # Find empty columns
    empty_columns: list[int] = []
    for j in range(len(lines[0])):
        for i in range(len(lines)):
            if lines[i][j] != '.':
                break
        else:
            empty_columns.append(j)
    print("Empty columns: ", empty_columns)

    # Find galaxies
    galaxies: set[tuple[int]] = set()
    for i, line in enumerate(lines):
        for j, c in enumerate(line):
            if c == '#':
                galaxies.add((i, j))

    # Adjust galaxy positions
    gap_width = 1_000_000
    coordinate_adjustment = gap_width - 1

    adj_galaxies: set[tuple[int]] = set()
    for i, j in galaxies:
        row_adjust = 0
        for row in empty_rows:
            if row < i:
                row_adjust += 1
        i += coordinate_adjustment * row_adjust

        column_adjust = 0
        for column in empty_columns:
            if column < j:
                column_adjust += 1
        j += coordinate_adjustment * column_adjust
        adj_galaxies.add((i, j))


    print(galaxies)
    print(adj_galaxies)

    total_distance = 0
    for galaxy in adj_galaxies:
        for other_galaxy in adj_galaxies:
            row_distance = abs(other_galaxy[0] - galaxy[0])
            column_distance = abs(other_galaxy[1] - galaxy[1])
            distance = row_distance + column_distance
            total_distance += distance
            print(galaxy, other_galaxy,distance, total_distance)

    print("Total distance: ", total_distance/2)

# answer 678626199476   




main(sys.argv)


