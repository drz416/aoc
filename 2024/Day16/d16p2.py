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
    grid: list[list[str]] = []
    start_facing = (0,1)
    start_score = 0
    directions = ((-1,0), (0,1), (1,0), (0,-1))
    
    # Find key locations
    for i, line in enumerate(lines):
        grid.append(list(line))
        if "S" in line:
            start_position = (i, line.find("S"))
        if "E" in line:
            end_position = (i, line.find("E"))

    # Initialize starting variables
    start_obj = Pather(start_position, start_facing, start_score, [start_position])
    q = deque([start_obj])
    
    best_paths = {(tuple(start_position), start_facing): (start_score, {start_obj})}
    Pather.best_paths = best_paths
    
    while q:
        curr_pather = q.pop()
        x, y = curr_pather.position
        if (x, y) == end_position:
            continue

        move_forward_as_last_action = False
        for dx, dy in directions:
            if (curr_pather.facing[0], curr_pather.facing[1]) == (-dx, -dy):
                pass
            elif grid[x+dx][y+dy] == "#":
                pass
            elif (dx, dy) == curr_pather.facing:
                move_forward_as_last_action = True
            else:
                #90deg turn
                new_score = curr_pather.score + 1000
                new_visited = curr_pather.visited.copy()
                new_pather = Pather((x,y), (dx,dy), new_score, new_visited)
                new_pather.move()
                if new_pather.is_best_path():
                    new_pather.set_self_best()
                    q.append(new_pather)
                elif new_pather.is_tied_best():
                    new_pather.add_to_best()
                    q.append(new_pather)

        if move_forward_as_last_action:
            curr_pather.move()
            if curr_pather.is_best_path():
                curr_pather.set_self_best()
                q.append(curr_pather)
            elif curr_pather.is_tied_best():
                curr_pather.add_to_best()
                q.append(curr_pather)


    min_dist = min(value[0] for key, value in best_paths.items() if key[0] == end_position)
    print(f"Best path score: {min_dist}")
    
    for key, value in best_paths.items():
        if (key[0] == end_position) and (value[0] == min_dist):
            final_paths = list(value[1])

    viewing_positions = set()
    for path in final_paths:
        print(f"Path: {path}, length {len(path.visited)}")
        viewing_positions.update(set(path.visited))

    print(f"Best viewing positions: {len(viewing_positions)}")
    # ans: 508

class Pather():
    best_paths: dict

    def __init__(
            self,
            position: tuple[int],
            facing: tuple[int],
            score: int,
            visited: list[tuple[int]]) -> None:
        self.position = position
        self.facing = facing
        self.score = score
        self.visited = visited
    
    def move(self) -> None:
        self.position = (self.position[0] + self.facing[0],
                         self.position[1] + self.facing[1])
        self.visited.append(self.position)
        self.score += 1
    
    def is_best_path(self) -> bool:
        if (self.position, self.facing) not in self.__class__.best_paths:
            return True
        return self.score < self.__class__.best_paths[(self.position, self.facing)][0]
    
    def set_self_best(self) -> None:
        self.__class__.best_paths[(self.position, self.facing)] = (self.score, {self})

    def is_tied_best(self) -> bool:
        return self.score == self.__class__.best_paths[(self.position, self.facing)][0]
    
    def add_to_best(self) -> None:
        self.__class__.best_paths[(self.position, self.facing)][1].add(self)

        





if __name__ == "__main__":
    main(sys.argv)


