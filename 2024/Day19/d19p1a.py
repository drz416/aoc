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
    towels: list[str] = []
    patterns: list[str] = []
    all_combinations = []
    
    for i, line in enumerate(lines):
        if i == 0:
            towels = line.split(", ")
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
        
        find_combos(possible_towels, (), pattern, towel_combinations)

        all_combinations.append(towel_combinations)

    

    total = 0
    for comb in all_combinations:
        print(comb)
        if len(comb) != 0:
            total += 1
    

    print(f"Total: {total}")
    # ans: cannot find answer, too slow

def find_combos(
        available_towels: list[str],
        arrangement_so_far: tuple[str],
        remaining_pattern: str,
        combinations: list[list[str]],
        ) -> None:
    print(f"  \033[KEnter: {' '.join(arrangement_so_far)} <- {remaining_pattern}\033[0G", end="")
    if len(combinations) != 0:
        return
    if remaining_pattern == "":
        if len(arrangement_so_far) != 0:
            combinations.append(arrangement_so_far)
        return
    
    for towel in available_towels:
        if remaining_pattern.startswith(towel):
            new_arrangement = arrangement_so_far + (towel,)
            new_remaining = remaining_pattern[len(towel):]
            find_combos(available_towels, new_arrangement, new_remaining, combinations)





    



if __name__ == "__main__":
    main(sys.argv)


