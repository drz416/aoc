import sys
import re
from collections import deque, Counter, defaultdict
from pathlib import Path
from pprint import pprint
from functools import partial, lru_cache
from itertools import product, combinations

# Run with test data    -> python3 -m d#p#
# Run with puzzle data  -> python3 -m d#p# X (any argument)

def main(argv: list[str]):
    # Prep Code
    lines: list[str]

    if len(argv) == 1:
        test_data = """\
##########
#..O..O.O#
#......O.#
#.OO..O.O#
#..O@..O.#
#O#..O...#
#O..O..O.#
#.OO.O.OO#
#....O...#
##########

<vv>^<v^>v>^vv^v>v<>v^v<v<^vv<<<^><<><>>v<vvv<>^v^>^<<<><<v<<<v^vv^v>^
vvv<<^>^v^^><<>>><>^<<><^vv^^<>vvv<>><^^v>^>vv<>v<<<<v<^v>^<^^>>>^<v<v
><>vv>v^v^<>><>>>><^^>vv>v<^^^>>v^v^<^^>v^^>v^<^v>v<>>v^v^<v>v^^<^^vv<
<<v<^>>^^^^>>>v^<>vvv^><v<<<>^^^vv^<vvv>^>v<^^^^v<>^>vvvv><>>v^<<^^^^^
^><^><>>><>^^<<^^v>>><^<v>^<vv>>v>>>^v><>^v><<<<v>>v<v<v>vvv>^<><<>^><
^>><>^v<><^vvv<^^<><v<<<<<><^v<<<><<<^^<v<^^^><^>>^<v^><<<^>>^v<v^v<v^
>^>>^v>vv>^<<^v<>><<><<v<<v><>v<^vv<<<>^^v^>^^>>><<^v>>v^v><^^>>^<>vv^
<><^^>^^^<><vvvvv^v<v<<>^v<v>v<<^><<><<><<<^^<<<^<<>><<><^^^>^^<>^>v<>
^^>vv<^v^v<vv>^<><v<^v>^^^>>>^^vvv^>vvv<>>>^<^>>>>>^<<^v>^vvv<>^<><<v>
v^^>>><<^^<>>^v^<v^vv<>v^<<>^<^v^v><^<<<><<^<v><v<>vv>>v><v^<vv<>v^<<^"""
        lines = test_data.splitlines()
    else:
        data_file = Path.cwd() / "puzzle_data.txt"
        with open(data_file, "r") as f:
            lines = f.readlines()

    for i, line in enumerate(lines):
        lines[i] = line.strip()

    # Puzzle code
    #----------------------------------------------------------------

    # Setup containers
    grid: list[list[str]] = []
    moves = ""
    robot = [0,0]

    in_grid = True
    for i, line in enumerate(lines):
        if line == "":
            in_grid = False
            continue
        if in_grid:
            grid.append(list(line))
            if "@" in line:
                robot = [i, line.find("@")]
        else:
            moves += line
    
    directions = {
        "^": (-1,0),
        ">": (0,1),
        "v": (1,0),
        "<": (0,-1),
    }


    for m in moves:
        if move(grid, directions, robot, m):
            robot[0] += directions[m][0]
            robot[1] += directions[m][1]





    total = 0
    for x, y in product(range(len(grid)), range(len(grid[0]))):
        if grid[x][y] == "O":
            total += x*100 + y



    print(f"Total: {total}")
    # ans: 1552463

def move(grid: list[list[str]], directions: dict, obj: list[int], direction: str) -> bool:
    # Recursive move function that checks objects along a direction: ^ > v <
    x, y = obj[0], obj[1]
    dx, dy = directions[direction]
    nx = x+dx
    ny = y+dy

    # Check if nearby space is empty
    if grid[nx][ny] == ".":
        grid[nx][ny] = grid[x][y]
        grid[x][y] = "."
        return True
    
    # Check if nearby space has a wall
    if grid[nx][ny] == "#":
        return False
    
    # If neither than space has a box "O", attempt to move the box
    if move(grid, directions, [nx, ny], direction) == False:
        return False
    grid[nx][ny] = grid[x][y]
    grid[x][y] = "."
    return True    
    




if __name__ == "__main__":
    main(sys.argv)


