import sys
import re
from collections import deque, Counter
from pathlib import Path
from pprint import pprint

# Run with test data    -> python3 -m d#p#
# Run with puzzle data  -> python3 -m d#p# X (any argument)

def main(argv: list[str]):
    # Prep Code
    lines: list[str]

    if len(argv) == 1:
        test_data = """\
1,0,1~1,2,1
0,0,2~2,0,2
0,2,3~2,2,3
0,0,4~0,2,4
2,0,5~2,2,5
0,1,6~2,1,6
1,1,8~1,1,9"""
        lines = test_data.splitlines()
    else:
        data_file = Path.cwd() / "puzzle_data.txt"
        with open(data_file, "r") as f:
            lines = f.readlines()

    for i, line in enumerate(lines):
        lines[i] = line.strip()

    # Puzzle code
    #----------------------------------------------------------------

    from copy import deepcopy
    # Constants
    pattern = r'(\d+),(\d+),(\d+)~(\d+),(\d+),(\d+)'
    brick_pattern = re.compile(pattern)

    # Read-in all bricks
    bricks: dict[Brick] = {}
    for brick_definition in lines:
        b_obj = Brick(brick_definition, brick_pattern)
        bricks[b_obj.name] = b_obj

    # Create grid
    grid: dict[Position] = {}
    for x in range(0, Brick.max_x + 1):
        for y in range(0, Brick.max_y + 1):
            for z in range(1, Brick.max_z + 1):
                p_obj = Position((x, y, z))
                grid[p_obj.coordinates] = p_obj

    # Place bricks
    for brick in bricks.values():
        brick.place(grid)


    # Fall all bricks from the ground up
    # for brick in bricks.values():
    #     print(brick)
    # print("Fall")

    for z in range(1, Brick.max_z + 1):
        for x in range(0, Brick.max_x + 1):
            for y in range(0, Brick.max_y + 1):
                if grid[(x, y, z)].occupied_by != None:
                    bricks[grid[(x, y, z)].occupied_by].fall(grid, bricks)
      
    # Take a snapshot of initial state
    for brick in bricks.values():
        clear_resting_on(bricks)

    grid_save = deepcopy(grid)
    bricks_save = deepcopy(bricks)


    # Run disintegration of each brick
    count = 0
    for brick in bricks_save.values():
        for position in brick.positions:            # Remove from all positions
            grid[position].occupied_by = None
        bricks.pop(brick.name)                      # Remove brick from dictionary

        # Fall all bricks
        for z in range(1, Brick.max_z + 1):
            for x in range(0, Brick.max_x + 1):
                for y in range(0, Brick.max_y + 1):
                    if grid[(x, y, z)].occupied_by != None:
                        if bricks[grid[(x, y, z)].occupied_by].fall(grid, bricks) == True:
                            count += 1
        print(brick, "Count:", count)

        # Refresh state
        grid = deepcopy(grid_save)
        bricks = deepcopy(bricks_save)



    # for brick in bricks.values():
    #     print(brick)
    # for position in grid.values():
    #     print(position)

    # Count disintegrations





class Brick():
    counter = 0
    max_x = 0
    max_y = 0
    max_z = 0
    
    def __init__(self, definition: str, brick_pattern: re.Pattern) -> None:
        self.name = f"Brick-{self.__class__.counter:04}"
        self.__class__.counter += 1
        xs, ys, zs, xf, yf, zf = brick_pattern.findall(definition)[0]
        xs, ys, zs, xf, yf, zf = int(xs), int(ys), int(zs), int(xf), int(yf), int(zf)
        self.__class__.max_x = max(self.__class__.max_x, xf)
        self.__class__.max_y = max(self.__class__.max_y, yf)
        self.__class__.max_z = max(self.__class__.max_z, zf)
        self.definition = (xs, ys, zs, xf, yf, zf)
        self.positions = []
        self.resting_on = set()
        self.orientation = None
        self.can_be_disintegrated = True

    def place(self, grid: dict) -> None:
        xs, ys, zs, xf, yf, zf = self.definition
        self.positions.append((xs, ys, zs))
        self.orientation = 'v'
        while True:
            if xs != xf:
                xs += 1
                self.positions.append((xs, ys, zs))
                self.orientation = 'h'
            elif ys != yf:
                ys += 1
                self.positions.append((xs, ys, zs))
                self.orientation = 'h'
            elif zs != zf:
                zs += 1
                self.positions.append((xs, ys, zs))
                self.orientation = 'v'
            else:
                break
        for positition in self.positions:
            grid[positition].occupied_by = self.name

    def fall(self, grid: dict, bricks: dict, fell: bool = False) -> None:
        if self.resting_on:                         # don't move if resting on a brick
            return fell
        if self.positions[0][2] == 1:               # don't move if resting on the ground                   
            self.resting_on.add('Ground')
            return fell

        if self.orientation == 'v':                 # if vertical, only check below base
            base = self.positions[0]
            below_base = (base[0], base[1], base[2] - 1)
            if grid[below_base].occupied_by != None:    # if resting on a brick, don't move
                self.resting_on.add(grid[below_base].occupied_by)
                return fell
            top = self.positions.pop()              # not resting on anything, move brick by 1 down
            self.positions.insert(0, below_base)
            grid[top].occupied_by = None
            grid[below_base].occupied_by = self.name
        elif self.orientation == 'h':               # if horizontal, check each position
            for position in self.positions:
                below_position = (position[0], position[1], position[2] - 1)
                if grid[below_position].occupied_by != None:
                    self.resting_on.add(grid[below_position].occupied_by)
            if self.resting_on:                     # if resting on any bricks, don't move
                return fell
            new_positions = []                      # not resting on anything, move brick by 1 down
            for position in self.positions:
                below_position = (position[0], position[1], position[2] - 1)
                new_positions.append(below_position)
                grid[position].occupied_by = None
                grid[below_position].occupied_by = self.name
            self.positions = new_positions

        return self.fall(grid, bricks, fell = True)              # Re-run the fall until reaching ground on another brick

    def __str__(self) -> str:
        return f"{self.name}: {self.positions}, Resting on: {self.resting_on}, Discintegrate: {self.can_be_disintegrated}"


class Position():
    def __init__(self, coordinates: tuple[int]) -> None:
        self.coordinates = coordinates
        self.x, self.y, self.z = coordinates[0], coordinates[1], coordinates[2]
        self.occupied_by = None
        pass

    def __str__(self) -> str:
        return f"{self.coordinates}: {self.occupied_by}"

def clear_resting_on(bricks: dict[Brick]) -> None:
    for brick in bricks.values():
        brick.resting_on = set()

if __name__ == "__main__":
    main(sys.argv)


