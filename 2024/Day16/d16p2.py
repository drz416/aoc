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
#################
#...#...#...#..E#
#.#.#.#.#.#.#.#.#
#.#.#.#...#...#.#
#.#.#.#.###.#.#.#
#...#.#.#.....#.#
#.#.#.#.#.#####.#
#.#...#.#.#.....#
#.#.#####.#.###.#
#.#.#.......#...#
#.#.###.#####.###
#.#.#...#.....#.#
#.#.#.#####.###.#
#.#.#.........#.#
#.#.#.#########.#
#S#.............#
#################"""
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
    from collections import OrderedDict
    grid: list[list[str]] = []
    directions = {
        (-1,0): ((0,1), (0,-1), (-1,0)),
        (0,1): ((-1,0), (1,0), (0,1)),
        (1,0): ((0,1), (0,-1), (1,0)),
        (0,-1): ((-1,0), (1,0), (0,-1)),
    }
    
    # Find key locations
    for i, line in enumerate(lines):
        grid.append(list(line))
        if "S" in line:
            start_position = (i, line.find("S"))
        if "E" in line:
            end_position = (i, line.find("E"))

    # Initialize starting object
    start_facing = (0,1)
    start_history = {(start_position, start_facing): 0}
    start_obj = Pather(start_position, start_facing, OrderedDict(**start_history))
    q = deque([start_obj])
    pathers = [start_obj]
    
    while q:
        curr = q.pop()
        x, y = curr.position
        print(f"\033[0G{curr.position}", sep="", end="")

        if (x, y) == end_position:
            continue
        possible_directions = []
        for dx, dy in directions[curr.facing]:
            if grid[x+dx][y+dy] != "#":
                possible_directions.append((dx, dy))
        
        for i, (dx, dy) in enumerate(possible_directions):
            if i == len(possible_directions) - 1:
                # This is the final possible direction, don't create copies just move
                if (dx, dy) != curr.facing:
                    curr.turn_90((dx, dy))
                if curr.move():
                    q.append(curr)
            else:
                # These are all turns that require copies
                new_path = Pather(curr.position, curr.facing, curr.history)
                new_path.turn_90((dx, dy))

                # check if another pather has a better score
                for pather in pathers:
                    best = True
                    if ((new_path.position, new_path.facing) in pather.history) and (pather.history[(new_path.position, new_path.facing)] < new_path.score):
                        best = False
                        break
                if best == False:
                    # The new copy is not the best path, delete the object
                    del new_path
                    continue
                
                # New path is best, move forward and ensure not backtracking
                if new_path.move():
                    pathers.append(new_path)
                    q.append(new_path)


    
    least = 99999999999999999999
    for pather in pathers:
        if (end_position, (-1,0)) in pather.history:
            least = min(least, pather.history[(end_position, (-1,0))])
    print(f"Least: {least}")


    total = 0
    for pather in pathers:
        if (end_position, (-1,0)) in pather.history:
            if pather.history[(end_position, (-1,0))] == least:
                total += 1
                pprint(pather.history)

    print(f"Total: {total}")




    # ans: 

class Pather():

    def __init__(self, position: tuple[int], facing: tuple[int], history: dict) -> None:
        self.position = position
        self.facing = facing
        self.score = history[(position, facing)]
        self.history = history.copy()
    
    def turn_90(self, new_facing: tuple[int]) -> None:
        self.facing = new_facing
        self.score += 1000
        self.history[(self.position, self.facing)] = self.score

    def move(self) -> bool:
        # Return False if stepped onto a position already traversed
        self.position = (self.position[0] + self.facing[0],
                         self.position[1] + self.facing[1])
        if (self.position, self.facing) in self.history:
            return False
        self.score += 1
        self.history[(self.position, self.facing)] = self.score
        return True
    


    

        





if __name__ == "__main__":
    main(sys.argv)


