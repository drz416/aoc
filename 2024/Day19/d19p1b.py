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
r, wr, b, g, bwu, rb, gb, br

brwrr
bggr
gbbr
rrbgbr
ubwu
bwurrg
brgr
bbrgwb"""
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
    towels: tuple[str] = []
    patterns: list[str] = []
    all_combinations = []
    
    for i, line in enumerate(lines):
        if i == 0:
            towels = tuple(line.split(", "))
            continue
        if i != 1:
            patterns.append(line)


    for i, pattern in enumerate(patterns):
        towel_combinations = []

        # Isolate towels only to possible ones; if no possible, skip
        possible_towels = []
        for towel in towels:
            if towel in pattern:
                possible_towels.append(towel)

        if len(possible_towels) == 0:
            all_combinations.append(towel_combinations)
            continue

        possible_towels = tuple(possible_towels)
        
        print(f"{i:<3} {pattern} #{len(possible_towels)}")

        # Check that end and beginning of pattern is possible
        beg_exists = end_exists = False
        
        for towel in towels:
            if pattern.startswith(towel):
                beg_exists = True
                break
        for towel in towels:
            if pattern.endswith(towel):
                end_exists = True
                break
        
        if (beg_exists and end_exists) == False:
            all_combinations.append(towel_combinations)
            continue
        
        combos = find_combos(possible_towels, pattern)

        if combos == None:
            all_combinations.append(towel_combinations)
            continue
        else:
            all_combinations.append(combos)



    total = 0
    for comb in all_combinations:
        print(comb)
        if len(comb) != 0:
            total += 1
    

    print(f"Total: {total}")
    # ans: 304

@lru_cache(maxsize=None)
def find_combos(
        available_towels: tuple[str],
        remaining_pattern: str,
        ) -> tuple[str]:
    print(f"  \033[KEnter: {remaining_pattern}\033[0G", end="")
    # if remaining_pattern == "b":
    #     breakpoint() 
    if remaining_pattern == "":
        return ()
    
    for towel in available_towels:
        if remaining_pattern.startswith(towel):
            new_remaining = remaining_pattern[len(towel):]
            combos = find_combos(available_towels, new_remaining)
            if combos == None:
                continue
            return (towel,) + combos
    return None




    



if __name__ == "__main__":
    main(sys.argv)


