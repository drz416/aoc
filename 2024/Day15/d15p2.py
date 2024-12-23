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
        elif in_grid:
            row = ""
            for c in line:
                if c == "#":
                    row += "##"
                elif c == ".":
                    row += ".."
                elif c == "O":
                    row += "[]"
                elif c == "@":
                    row += "@."
            grid.append(list(row))
            if "@" in row:
                robot = [i, row.find("@")]
        else:
            moves += line
    
    directions = {
        "^": (-1,0),
        ">": (0,1),
        "v": (1,0),
        "<": (0,-1),
    }

    print_grid(grid)

    for direction in moves:
        if move(grid, directions, tuple(robot), direction):
            robot[0] += directions[direction][0]
            robot[1] += directions[direction][1]
        # print_grid(grid)






    print_grid(grid)

    total = 0
    for x, y in product(range(len(grid)), range(len(grid[0]))):
        if grid[x][y] == "[":
            total += x*100 + y

    print(f"Total: {total}")
    # ans: 1554058

def move(grid: list[list[str]], directions: dict, obj: tuple[int], direction: str) -> bool:
    # Recursive move function that moves objects in all direcitons ^ > v <
    x, y = obj
    dx, dy = directions[direction]
    nx, ny = x+dx, y+dy
    
    # print(f"Moving '{grid[x][y]}' ({x}, {y}) -> '{grid[nx][ny]}' ({nx}, {ny})", flush=True)

    # Check if nearby space is empty
    if grid[nx][ny] == ".":
        grid[nx][ny] = grid[x][y]
        grid[x][y] = "."
        return True
    
    # Check if nearby space has a wall
    if grid[nx][ny] == "#":
        return False
    
    # If neither than space has a box [], attempt to move the box
    
    # <> motion is normal
    if direction in {"<", ">"}:
        if move(grid, directions, (nx, ny), direction) == False:
            return False
        grid[nx][ny] = grid[x][y]
        grid[x][y] = "."
        return True
    
    # for ^v motion, check if both parts of the box can move, before moving
    if grid[nx][ny] == "[":
        l_obj = (nx, ny)
        r_obj = (nx, ny+1)
    elif grid[nx][ny] == "]":
        l_obj = (nx, ny-1)
        r_obj = (nx, ny)
    else:
        raise ValueError(f"Unrecognized object {grid[nx][ny]} at ({nx}, {ny})")
    # print(f"Checking moving box -> '{grid[l_obj[0]][l_obj[1]]}' {l_obj}, '{grid[r_obj[0]][r_obj[1]]} {r_obj}", flush=True)

    # l_can_move = move(grid, directions, l_obj, direction)
    # r_can_move = move(grid, directions, r_obj, direction)

    if check_move(grid, directions, l_obj, direction) and check_move(grid, directions, r_obj, direction):
        # print(f"Can move -> '{grid[l_obj[0]][l_obj[1]]}' {l_obj}, '{grid[r_obj[0]][r_obj[1]]} {r_obj}", flush=True)
        move(grid, directions, l_obj, direction)
        move(grid, directions, r_obj, direction)
        grid[nx][ny] = grid[x][y]
        grid[x][y] = "."
        return True
    
    # print(f"CANT move -> '{grid[l_obj[0]][l_obj[1]]}' {l_obj}, '{grid[r_obj[0]][r_obj[1]]} {r_obj}", flush=True)
    return False



def check_move(grid: list[list[str]], directions: dict, obj: tuple[int], direction: str) -> bool:
    # Recursive check fuction as above, but launches two recursive functions at once, testing movement before move is initialized
    x, y = obj
    dx, dy = directions[direction]
    nx, ny = x+dx, y+dy

    # Check if nearby space is empty
    if grid[nx][ny] == ".":
        return True
    
    # Check if nearby space has a wall
    if grid[nx][ny] == "#":
        return False
    
    # Next stop is a wall, identify both parts
    if grid[nx][ny] == "[":
        l_obj = (nx, ny)
        r_obj = (nx, ny+1)
    elif grid[nx][ny] == "]":
        l_obj = (nx, ny-1)
        r_obj = (nx, ny)
    
    l_check = check_move(grid, directions, l_obj, direction)
    r_check = check_move(grid, directions, r_obj, direction)

    return l_check and r_check

    
def print_grid(grid) -> None:
    header = "  "
    header2 = "  "
    for i in range(len(grid[0])):
        header += str(i % 10)
        header2 += "|"
    print(header)
    print(header2)

    for i, row in enumerate(grid):
        s = str(i % 10) + "|"
        for c in row:
            s += c
        print(s)
    print("")




if __name__ == "__main__":
    main(sys.argv)


