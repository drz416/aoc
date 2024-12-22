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
p=0,4 v=3,-3
p=6,3 v=-1,-3
p=10,3 v=-1,2
p=2,0 v=2,-1
p=0,0 v=1,3
p=3,0 v=-2,-2
p=7,6 v=-1,-3
p=3,0 v=-1,-2
p=9,3 v=2,3
p=7,3 v=-1,2
p=2,4 v=2,-3
p=9,5 v=-3,-3"""
        lines = test_data.splitlines()
    else:
        data_file = Path.cwd() / "puzzle_data.txt"
        with open(data_file, "r") as f:
            lines = f.readlines()

    for i, line in enumerate(lines):
        lines[i] = line.strip()

    # Puzzle code
    #----------------------------------------------------------------

    # Set initial variables

    if len(argv) == 1:
        Robot.x_len = 11
        Robot.y_len = 7
        grid_dimensions = [11, 7]
    else:
        Robot.x_len = 101
        Robot.y_len = 103
        grid_dimensions = [101, 103]

    Robot.x_mid = int((Robot.x_len - 1) / 2)
    Robot.y_mid = int((Robot.y_len - 1) / 2)

    robots: list[Robot] = []
    
    
    # Load robots
    pattern = r"p=(\d+),(\d+)\sv=(-?\d+),(-?\d+)"
    pobj = re.compile(pattern)

    for line in lines:
        mt = pobj.findall(line)[0]
        mt = tuple(map(int, mt))
        robots.append(Robot((mt[0], mt[1]), (mt[2], mt[3])))

    from time import sleep

    i = 0
    start_moves = total_moves = 65
    moves = 103
    while True:
        for robot in robots:
            if start_moves == total_moves:
                robot.move(start_moves)    
            else:
                robot.move(moves)
        draw(grid_dimensions, robots)
        i += 1
        print(f"{i=} {total_moves=} --------------------------------------------------------")
        total_moves += moves
        sleep(0.2)



    total = 1

    print(f"Total: {total}")
    # ans: 7584


def draw(grid_dimensions: list[int], robots: list["Robot"]) -> None:
    grid = [[" "]*grid_dimensions[0] for _ in range(grid_dimensions[1])]
    for robot in robots:
        grid[robot.position[1]][robot.position[0]] = "#"
    for row in grid:
        print("".join(row))


# pattern1: 9  110 211 312
# pattern2: 65 168 271


class Robot:
    x_len: int
    y_len: int
    x_mid: int
    y_mid: int

    def __init__(self, position: tuple[int], velocity: tuple[int]) -> None:
        self.position = position
        self.velocity = velocity

    def move(self, seconds: int) -> None:
        self.position = ((self.position[0] + self.velocity[0] * seconds) % self.__class__.x_len,
                         (self.position[1] + self.velocity[1] * seconds) % self.__class__.y_len)

    @property
    def quadrant(self) -> int:
        #   0 | 1
        #   2 | 3       4 is middle column/row
        x, y = self.position
        if x < self.__class__.x_mid and y < self.__class__.y_mid:
            return 0
        if x > self.__class__.x_mid and y < self.__class__.y_mid:
            return 1
        if x < self.__class__.x_mid and y > self.__class__.y_mid:
            return 2
        if x > self.__class__.x_mid and y > self.__class__.y_mid:
            return 3
        return 4


if __name__ == "__main__":
    main(sys.argv)


