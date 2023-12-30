import sys
from pathlib import Path

# Run with test data    -> python3 -m d#p#
# Run with puzzle data  -> python3 -m d#p# X (any argument)

def main(argv: list[str]):
    # Prep Code
    lines: list[str]

    if len(argv) == 1:
        test_data = """\
O....#....
O.OO#....#
.....##...
OO.#O....O
.O.....O#.
O.#..O.#.#
..O..#O..O
.......O..
#....###..
#OO..#...."""
        lines = test_data.splitlines()
    else:
        data_file = Path.cwd() / "puzzle_data.txt"
        with open(data_file, "r") as f:
            lines = f.readlines()

    for i, line in enumerate(lines):
        lines[i] = line.strip()

    # Puzzle code
    #----------------------------------------------------------------

    # Create 2-D array to hold all the rocks
    array: list[list[str]] = []
    for line in lines:
        array.append(list(line))
    
    print_array(array)
    print('')
    print("Move")
    print('')
    for i, row in enumerate(array):
        for j, c in enumerate(row):
            if c in {'.', '#'}:
                continue
            move_rock(array, i, j)
    count_score(array)

def move_rock(
        array: list[list[str]],
        rock_row: int,
        rock_column: int
        ) -> None:
    if check_neighbour(array, rock_row, rock_column) == False:
        return
    array[rock_row-1][rock_column] = 'O'
    array[rock_row][rock_column] = '.'
    move_rock(array, rock_row-1, rock_column)

def check_neighbour(
        array: list[list[str]],
        current_row: int,
        current_column: int
        ) -> bool:
    if current_row == 0:
        return False
    neighbour = array[current_row-1][current_column]
    if neighbour in {'O', '#'}:
        return False
    return True

def print_array(array: list[list[str]]):
    for row in array:
        print(''.join(row))

def count_score(array: list[list[str]]) -> int:
    num_rows = len(array)
    total_score = 0
    for i, row in enumerate(array):
        srow = ''.join(row)
        score = srow.count('O') * (num_rows - i)
        total_score += score
        print(srow, score, total_score)
    return total_score
    



main(sys.argv)


