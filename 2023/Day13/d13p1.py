import sys
from pathlib import Path

# Run with test data    -> python3 -m d#p#
# Run with puzzle data  -> python3 -m d#p# X (any argument)

def main(argv: list[str]):
    # Prep Code
    lines: list[str]

    if len(argv) == 1:
        test_data = """\
#.##..##.
..#.##.#.
##......#
##......#
..#.##.#.
..##..##.
#.#.##.#.

#...##..#
#....#..#
..##..###
#####.##.
#####.##.
..##..###
#....#..#"""
        lines = test_data.splitlines()
    else:
        data_file = Path.cwd() / "puzzle_data.txt"
        with open(data_file, "r") as f:
            lines = f.readlines()

    for i, line in enumerate(lines):
        lines[i] = line.strip()

    # Puzzle code
    #----------------------------------------------------------------


    # Convert data into list of arrays
    all_arrays: list[list[tuple[str]]] = []
    accumulator: list[list[str]] = []
    
    for line in lines:
        if not line:
            all_arrays.append(accumulator)
            accumulator = []
            continue
        accumulator.append(tuple(line))
    all_arrays.append(accumulator)

    # Go through each numpy array and check for vertical or horizontal lines
    horizontal_lines: list[int] = []
    vertical_lines: list[int] = []

    for i, array in enumerate(all_arrays):
        print(f"> {i}")
        horizontal_line = check_horizontal_lines(array)
        vertical_line = check_vertical_lines(array)

        if horizontal_line == 0 and vertical_line == 0:
            print(f"Array at {i=} doesn't have horizontal or vertical lines")
            # break
        if horizontal_line != 0 and vertical_line != 0:
            print(f"Array at {i=} has both horizontal and vertical lines")
            break

        horizontal_lines.append(horizontal_line)
        vertical_lines.append(vertical_line)
        print(f"({horizontal_line}, {vertical_line})")

    print("Horizontal lines:", horizontal_lines, '',
          "Vertical lines:", vertical_lines, sep='\n')

    print(f"answer = {sum(horizontal_lines)*100 + sum(vertical_lines)}")




def check_vertical_lines(array: list[tuple[str]]) -> int:
    t_array: list[tuple[str]] = []
    accumulator: list[str] = []

    for j in range(len(array[0])):
        for i in range(len(array)):
            accumulator.append(array[i][j])
        t_array.append(tuple(accumulator))
        accumulator = []
    
    return check_horizontal_lines(t_array)


def check_horizontal_lines(array: list[tuple[str]]) -> int:
    line_position = 0                       # 0 means not found
    for row in range(len(array) - 1):
        if array[row] == array[row+1]:
            if check_horizontal_consistency(array.copy(), row+1):
                line_position = row + 1
    
    return line_position


def check_horizontal_consistency(array: list[tuple[str]], position: int) -> bool:
    for i, a in enumerate(array):
        if i == position-1 or i == position:
            print(a, position, '|')
        else:
            print(a, position)
    print('')

    if len(array) == 0:
        return True
    if position == 0:
        return True
    try:
        second = array.pop(position)
    except IndexError:
        print("Position+0 missing -> stop")
        return True
    try:
        first = array.pop(position - 1)
    except IndexError:
        print("Position-1 missing -> stop")
        return True
    if first != second:
        print("No match")
        return False
    return check_horizontal_consistency(array, position-1)
    


main(sys.argv)


