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
125 17"""
        lines = test_data.splitlines()
    else:
        data_file = Path.cwd() / "puzzle_data.txt"
        with open(data_file, "r") as f:
            lines = f.readlines()

    for i, line in enumerate(lines):
        lines[i] = line.strip()

    # Puzzle code
    #----------------------------------------------------------------

    # Known mappings z (x,y) for stone with a label of z,  after itering
    #  x steps, the number y will be created
    mappings = {
        0: [(1,1)],
        1: [(3,2),(3,0), (3,2), (3,4)],
        2: [(3,4),(3,0), (3,4), (3,8)],
        3: [(3,6),(3,0), (3,7), (3,2)],
        4: [(3,8),(3,0), (3,9), (3,6)],
        5: [(5,2),(5,0), (5,4), (5,8), (5,2),(5,8), (5,8), (5,0)],
        6: [(5,2),(5,4), (5,5), (5,7), (5,9),(5,4), (5,5), (5,6)],
        7: [(5,2),(5,8), (5,6), (5,7), (5,6),(5,0), (5,3), (5,2)],
        8: [(5,3),(5,2), (5,7), (5,7), (5,2),(5,6), (4,8)], #special case
        9: [(5,3),(5,6), (5,8), (5,6), (5,9),(5,1), (5,8), (5,4)],
    }

    # Initialize stones cache
    # {
    #   level: {value1: number of values,
    #           value2: number of values,
    #           }
    # }
    stones = defaultdict(dict)
    for value in lines[0].split():
        value = int(value)
        stones[0][value] = stones[0].setdefault(value, 0) + 1

    # Go through blinks
    blinks = 75
    for lvl in range(blinks):
        #pprint(dict(stones))
        for val, num in stones[lvl].items():
            if num == 0:
                pass
            elif (val in mappings) and (lvl + mappings[val][0][0] < blinks):
                # print(f"val in mappings {val=}")
                for offset, digit in mappings[val]:
                    stones[lvl+offset][digit] = stones[lvl+offset].setdefault(digit, 0) + num
            elif len(str(val)) % 2 == 0:
                # print(f"val is even len {val=}")
                left_side = str(val)[0:int(len(str(val)) / 2)]
                right_side = str(val)[int(len(str(val)) / 2):]
                left_side = int(left_side)
                right_side = int(right_side)
                stones[lvl+1][left_side] = stones[lvl+1].setdefault(left_side, 0) + num
                stones[lvl+1][right_side] = stones[lvl+1].setdefault(right_side, 0) + num
            else:
                # print(f"Else val * 2024 {val=}, {2024*val}")
                stones[lvl+1][val*2024] = stones[lvl+1].setdefault(lvl*2024, 0) + num
        del(stones[lvl])
    pprint(dict(stones))

    total = 0
    for num in stones[blinks].values():
        total += num
    print(f"Total: {total}")
    # ans: 238317474993392





if __name__ == "__main__":
    main(sys.argv)


