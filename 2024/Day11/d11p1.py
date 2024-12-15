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

    # Create stones linked list
    new_stone: Stone = None
    prev_stone: Stone = None
    head: Stone = None

    for i, number in enumerate(lines[0].split()):
        new_stone = Stone(int(number))
        if i == 0:
            head = new_stone
        else:
            prev_stone.next = new_stone
        prev_stone = new_stone

    for _ in range(25):
        blink(head)
        # print(count_stones(head))



    total = count_stones(head)

    print(f"Total: {total}")
    # ans: 200446

class Stone():
    def __init__(self, number: int) -> None:
        self.number = number
        self.next = None

def count_stones(head: Stone) -> int:
    curr_stone = head
    total = 0
    while True:
        # print(f"{curr_stone.number:<10}: {curr_stone}")
        # print(f"    next -> {curr_stone.next}")
        total += 1
        if curr_stone.next == None:
            break
        curr_stone = curr_stone.next
    return total
    
def blink(head: Stone) -> None:
    prev_stone: Stone = None
    mid_stone: Stone = None
    curr_stone: Stone = head
    while True:
        if curr_stone.number == 0:
            curr_stone.number = 1
        elif (len(str(curr_stone.number)) % 2 == 0) and (curr_stone == head):
            left_side = str(curr_stone.number)[0:int(len(str(curr_stone.number))/2)]
            right_side = str(curr_stone.number)[int(len(str(curr_stone.number))/2):]
            mid_stone = Stone(int(right_side))
            mid_stone.next = curr_stone.next
            curr_stone.number = int(left_side)
            curr_stone.next = mid_stone
            curr_stone = mid_stone
        elif (len(str(curr_stone.number)) % 2 == 0):
            left_side = str(curr_stone.number)[0:int(len(str(curr_stone.number))/2)]
            right_side = str(curr_stone.number)[int(len(str(curr_stone.number))/2):]
            mid_stone = Stone(int(left_side))
            prev_stone.next = mid_stone
            mid_stone.next = curr_stone
            curr_stone.number = int(right_side)
        else:
            curr_stone.number *= 2024
        if curr_stone.next == None:
            break
        prev_stone = curr_stone
        curr_stone = curr_stone.next



if __name__ == "__main__":
    main(sys.argv)


