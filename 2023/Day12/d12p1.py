import re

import sys
from pathlib import Path

# Run with test data    -> python3 -m d#p#
# Run with puzzle data  -> python3 -m d#p# X (any argument)

def main(argv: list[str]):
    # Prep Code
    lines: list[str]

    if len(argv) == 1:
        test_data = """\
???.### 1,1,3
.??..??...?##. 1,1,3
?#?#?#?#?#?#?#? 1,3,1,6
????.#...#... 4,1,1
????.######..#####. 1,6,5
?###???????? 3,2,1"""

        lines = test_data.splitlines()
    else:
        data_file = Path.cwd() / "puzzle_data.txt"
        with open(data_file, "r") as f:
            lines = f.readlines()

    for i, line in enumerate(lines):
        lines[i] = line.strip()

    # Puzzle code
    #----------------------------------------------------------------

    # Split data
    all_groups: list[list[int]] = []

    for i, line in enumerate(lines):
        lines[i] = line.split()[0]
        groups = line.split()[1].split(',')
        groups = [int(num) for num in groups]
        all_groups.append(groups)

    # Print all 
    # for i, line in enumerate(lines):
    #     print(line, groupings[i], groupings_totals[i])    

    # Initialize re
    pattern = r"(#+)+"
    p_obj = re.compile(pattern)

    # Go through all permutations and check for possiblities
    possibilities = 0
    for i, line in enumerate(lines):
        unknowns = line.count('?')
        permutations = create_permutations(unknowns)

        for permutation in permutations:
            line_copy = line
            for c in permutation:
                line_copy = line_copy.replace('?', c, 1)
            new_groups = count_groupings(p_obj, line_copy)
            if new_groups == all_groups[i]:
                possibilities += 1
        print(line, possibilities)


def create_permutations(unknowns: int) -> list[str]:
    permutations: list[str] = []
    for num in range(2 ** unknowns):
        binary = bin(num).lstrip('0b').zfill(unknowns)
        permutations.append(binary.replace('0', '.').replace('1', '#'))
    return permutations.copy()


def count_groupings(p_obj: re.Pattern, line: str) -> list[int]:
    groups: list[str] = p_obj.findall(line)
    numbers = []
    for group in groups:
        numbers.append(group.count('#'))
    return numbers.copy()    


main(sys.argv)


