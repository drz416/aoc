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

    # Run cycles
    cycles = 1_000_000_000
    scores = {}

    i = 0
    scores[i] = count_score(array)

    while i < cycles:
        n_tilt(array)
        w_tilt(array)
        s_tilt(array)
        e_tilt(array)
        i += 1
        scores[i] = count_score(array)
        if tuple(scores.values()).count(scores[i]) == 10:
            break
    
    pprint(scores)
    print(f"Value {scores[i]} repeated 10 times at {i=}")
    #ans 96061, visually find period length, and determine what number ends at i = xxx9

## NORTH
def n_tilt(array: list[list[str]]) -> None:
    for i, row in enumerate(array):
        for j, c in enumerate(row):
            if c in {'.', '#'}:
                continue
            n_move_rock(array, i, j)

def n_move_rock(
        array: list[list[str]],
        rock_row: int,
        rock_column: int
        ) -> None:
    if n_check_neighbour(array, rock_row, rock_column) == False:
        return
    array[rock_row-1][rock_column] = 'O'
    array[rock_row][rock_column] = '.'
    n_move_rock(array, rock_row-1, rock_column)

def n_check_neighbour(
        array: list[list[str]],
        current_row: int,
        current_column: int
        ) -> bool:
    if current_row == 0:
        return False
    if array[current_row-1][current_column] in {'O', '#'}:
        return False
    return True

## WEST
def w_tilt(array: list[list[str]]) -> None:
    for i, row in enumerate(array):
        for j, c in enumerate(row):
            if c in {'.', '#'}:
                continue
            w_move_rock(array, i, j)

def w_move_rock(
        array: list[list[str]],
        rock_row: int,
        rock_column: int
        ) -> None:
    if w_check_neighbour(array, rock_row, rock_column) == False:
        return
    array[rock_row][rock_column-1] = 'O'
    array[rock_row][rock_column] = '.'
    w_move_rock(array, rock_row, rock_column-1)

def w_check_neighbour(
        array: list[list[str]],
        current_row: int,
        current_column: int
        ) -> bool:
    if current_column == 0:
        return False
    if array[current_row][current_column-1] in {'O', '#'}:
        return False
    return True

## SOUTH
def s_tilt(array: list[list[str]]) -> None:
    for i_rev in range(len(array)-1, -1, -1):
        for j, c in enumerate(array[i_rev]):
            if c in {'.', '#'}:
                continue
            s_move_rock(array, i_rev, j)

def s_move_rock(
        array: list[list[str]],
        rock_row: int,
        rock_column: int
        ) -> None:
    if s_check_neighbour(array, rock_row, rock_column) == False:
        return
    array[rock_row+1][rock_column] = 'O'
    array[rock_row][rock_column] = '.'
    s_move_rock(array, rock_row+1, rock_column)

def s_check_neighbour(
        array: list[list[str]],
        current_row: int,
        current_column: int
        ) -> bool:
    if current_row == (len(array)-1):
        return False
    if array[current_row+1][current_column] in {'O', '#'}:
        return False
    return True

## EAST
def e_tilt(array: list[list[str]]) -> None:
    for i, row in enumerate(array):
        for j_rev in range(len(row)-1, -1, -1):
            if row[j_rev] in {'.', '#'}:
                continue
            e_move_rock(array, i, j_rev)

def e_move_rock(
        array: list[list[str]],
        rock_row: int,
        rock_column: int
        ) -> None:
    if e_check_neighbour(array, rock_row, rock_column) == False:
        return
    array[rock_row][rock_column+1] = 'O'
    array[rock_row][rock_column] = '.'
    e_move_rock(array, rock_row, rock_column+1)

def e_check_neighbour(
        array: list[list[str]],
        current_row: int,
        current_column: int
        ) -> bool:
    if current_column == (len(array[0])-1):
        return False
    if array[current_row][current_column+1] in {'O', '#'}:
        return False
    return True

## Common Functions
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
        #print(srow, score, total_score)
    return total_score
    



main(sys.argv)


