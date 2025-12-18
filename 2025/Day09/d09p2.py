# /// script
# requires-python = ">=3.14"
# dependencies = []
# ///
#
# to add dependencies -> uv add --script <file> <module>
# to remove dependencies -> uv remove --script <file> <module>
# to run with test data    -> uv run --script d#p#
# to run with puzzle data  -> uv run --script d#p# X (any argument)



# Template Imports
#----------------------------------------------------------------
import sys
import re
from pathlib import Path
from pprint import pprint
from time import time, time_ns
from collections import deque, Counter, defaultdict
from functools import partial, lru_cache
from itertools import product, combinations
#----------------------------------------------------------------


# Solution Code
#----------------------------------------------------------------

def main(rows: list[str]):

    # Grab all red tiles, and create a unique list of horizontal and vertical positions
    red_tiles: list[tuple[int]] = []
    v_positions = {0}
    h_positions = {0}
    for row in rows:
        h, v = row.split(",")
        h, v = int(h), int(v)
        red_tiles.append((v, h))                # Note order is flipped for easier indexing
        v_positions.add(v)
        h_positions.add(h)

    v_positions = list(v_positions)
    h_positions = list(h_positions)
    v_positions.sort()
    h_positions.sort()

    # Fold the unused rows and columns by essentially sequencing only the existing rows and columns
    v_lookup = {}
    h_lookup = {}
    for i, v_pos in enumerate(v_positions):
        v_lookup[v_pos] = i
    for i, h_pos in enumerate(h_positions):
        h_lookup[h_pos] = i

    # Update all the red tile verticies to folded verticies
    folded_tiles: list[tuple[int]] = []
    for v, h in red_tiles:
        folded_tiles.append((v_lookup[v], h_lookup[h]))

    # Make an empty grid
    grid: list[list[bool]] = []
    for _ in range(len(v_positions)+1):               # Adding a bottom border of blanks
        grid.append([2] * (len(h_positions)+1))        # Adding a right border of blanks

    # Draw red and green tile border (int of 1 == red or green)
    prev_red = folded_tiles[0]
    path_tiles = folded_tiles[1:]
    path_tiles.append(folded_tiles[0])

    for next_tile in path_tiles:
        if next_tile[0] == prev_red[0]:          # v equal, Traverse horizontal
            v = prev_red[0]
            start = min(prev_red[1], next_tile[1])
            end = max(prev_red[1], next_tile[1])
            for h in range(start, end+1):
                grid[v][h] = 1
        else:                                   # h equal, Traverse vertical
            h = prev_red[1]
            start = min(prev_red[0], next_tile[0])
            end = max(prev_red[0], next_tile[0])
            for v in range(start, end+1):
                grid[v][h] = 1
        prev_red = next_tile
    
    # Since final shape does not have any enclosed empty spaces, convert all empty
    # space to 0s using breadthforce search. Start by setting top left corner to 0
    pos_que: deque[tuple[int]] = deque()
    pos_que.append((0,0))

    def get_directions(position: tuple[int]) -> list[tuple[int]]:
        v, h = position
        return [(v-1, h), (v, h+1), (v+1, h), (v, h-1)]

    while pos_que:
        tile = pos_que.popleft()
        v, h = tile
        try:
            if grid[v][h] == 2:
                grid[v][h] = 0
                for direction in get_directions((v, h)): 
                    pos_que.append(direction)
        except IndexError:
            continue

    # Now compare each red tile pairwise and look for rectangles that are fully enclosed,
    # Put another way, no 0s within
    ans = 0
    for ((v1, h1), (v2, h2)) in combinations(folded_tiles, 2):
        v_range = range(min(v1, v2), max(v1, v2)+1)
        h_range = range(min(h1, h2), max(h1, h2)+1)
        for v, h in product(v_range, h_range):
            if grid[v][h] == 0:
                break
        else:
            area = (abs(v_positions[v1]-v_positions[v2])+1) * (abs(h_positions[h1]-h_positions[h2])+1)
            if area > ans:
                ans = area

    print(f"\nAns: {ans}")

    # ans: 1540192500




#----------------------------------------------------------------



# Data load and caling main()
#----------------------------------------------------------------
if __name__ == "__main__":
    # Prep Data
    rows: list[str]

    if len(sys.argv) == 1:
        # Paste test example data here
        test_data = """\
7,1
11,1
11,7
9,7
9,5
2,5
2,3
7,3"""
        rows = test_data.splitlines()
    else:
        data_file = Path.cwd() / "puzzle_data.txt"
        with open(data_file, "r") as f:
            rows = f.readlines()

    for i, line in enumerate(rows):
        rows[i] = line.strip()
    
    start_time = time()
    main(rows)
    print("")
    print(f"Time in main(): {time() - start_time:.06f}s")
#----------------------------------------------------------------


