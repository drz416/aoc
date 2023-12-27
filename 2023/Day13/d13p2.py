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

    # initial_horizontal_lines = [0, 4]       # for test data

    # initial_vertical_lines = [5, 0]         # for test data

    initial_horizontal_lines = [            # for puzzle data
        9, 2, 1, 0, 0, 0, 0, 0, 4, 7, 0, 0, 0, 0, 3, 0, 0, 0, 8, 0, 0, 0, 9, 8,
        0, 2, 2, 10, 0, 1, 0, 2, 5, 0, 15, 6, 0, 13, 0, 14, 8, 0, 0, 0, 3, 16,
        0, 0, 0, 0, 3, 14, 5, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 2, 0, 0, 4, 0, 6,
        14, 3, 1, 0, 12, 2, 0, 0, 7, 3, 10, 0, 0, 6, 2, 3, 15, 0, 0, 11, 0, 0,
        0, 0, 11, 0, 0, 0, 14, 10, 8
        ]
    
    initial_vertical_lines = [              # for puzzle data
        0, 0, 0, 3, 14, 2, 9, 3, 0, 0, 1, 14, 7, 16, 0, 13, 9, 1, 0, 2, 1, 5,
        0, 0, 11, 0, 0, 0, 16, 0, 6, 0, 0, 1, 0, 0, 2, 0, 1, 0, 0, 5, 2, 6, 0,
        0, 6, 10, 12, 2, 0, 0, 0, 13, 0, 5, 13, 14, 3, 4, 0, 5, 1, 0, 10, 11,
        0, 2, 0, 0, 0, 0, 11, 0, 0, 6, 8, 0, 0, 0, 7, 11, 0, 0, 0, 0, 1, 2, 0,
        8, 2, 7, 1, 0, 12, 11, 8, 0, 0, 0
        ]

    # Convert data into list of arrays
    all_arrays: list[list[list[str]]] = []
    accumulator: list[list[str]] = []
    
    for line in lines:
        if not line:
            all_arrays.append(accumulator)
            accumulator = []
            continue
        accumulator.append(list(line))
    all_arrays.append(accumulator)

    # Go through each numpy array and check for vertical or horizontal lines
    horizontal_lines: list[int] = []
    vertical_lines: list[int] = []

    for i, array in enumerate(all_arrays):
        print('')
        print(f"Array: [{i}]")
        horizontal_line = check_horizontal_lines(array.copy(), initial_horizontal_lines[i])
        print("Switch to vertial")
        vertical_line = check_vertical_lines(array.copy(), initial_vertical_lines[i])

        if horizontal_line == 0 and vertical_line == 0:
            print(f"Array at {i=} doesn't have horizontal or vertical lines")
            # break
        if horizontal_line != 0 and vertical_line != 0:
            print(f"Array at {i=} has both horizontal and vertical lines")
            break

        horizontal_lines.append(horizontal_line)
        vertical_lines.append(vertical_line)
        print(f"({horizontal_line}, {vertical_line})")

    print('', "Horizontal lines:", horizontal_lines,
          "Vertical lines:", vertical_lines, sep='\n')

    print(f"answer = {sum(horizontal_lines)*100 + sum(vertical_lines)}")




def check_vertical_lines(array: list[list[str]], v_cant_be: int) -> int:
    t_array: list[list[str]] = []
    accumulator: list[str] = []

    for j in range(len(array[0])):
        for i in range(len(array)):
            accumulator.append(array[i][j])
        t_array.append(list(accumulator))
        accumulator = []
    
    return check_horizontal_lines(t_array, v_cant_be)


def check_horizontal_lines(array: list[list[str]], h_cant_be: int) -> int:
    line_position = 0                       # 0 means not found
    for row in range(len(array) - 1):
        array_copy = array.copy()
        made_swap = False
        if row+1 == h_cant_be:
            print("Skipping", row+1)
            continue
        if array_copy[row] != array_copy[row+1]:
            array_copy[row], array_copy[row+1], made_swap = search_fix_smudge(array_copy[row], array_copy[row+1])
            if made_swap:
                print("Made swap on line check")
        if array_copy[row] == array_copy[row+1]:
            print(f"Matched at {row}, {row+1}")
            if check_horizontal_consistency(array_copy, row+1, made_swap):
                line_position = row + 1

    return line_position


def check_horizontal_consistency(array: list[tuple[str]], position: int, made_swap: bool) -> bool:
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
        print("Position+0 missing -> ok")
        return True
    try:
        first = array.pop(position - 1)
    except IndexError:
        print("Position-1 missing -> ok")
        return True
    if made_swap == False:
        first, second, made_swap = search_fix_smudge(first, second)
        if made_swap:
            print("Made swap in consistency")
    if first != second:
        print("No match")
        return False
    return check_horizontal_consistency(array, position-1, made_swap)
    
def search_fix_smudge(first_row: list[str], second_row: list[str]) -> tuple:
    differences = 0
    for first, second in zip(first_row, second_row):
        if first != second:
            differences += 1
        if differences > 1:
            break
    if differences == 1:
        return (first_row, first_row, True)
    return (first_row, second_row, False)

main(sys.argv)


