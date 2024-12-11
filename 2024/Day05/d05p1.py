import sys
import re
from collections import deque, Counter, defaultdict
from pathlib import Path
from pprint import pprint
from functools import partial, lru_cache

# Run with test data    -> python3 -m d#p#
# Run with puzzle data  -> python3 -m d#p# X (any argument)

def main(argv: list[str]):
    # Prep Code
    lines: list[str]

    if len(argv) == 1:
        test_data = """\
47|53
97|13
97|61
97|47
75|29
61|13
75|53
29|13
97|29
53|29
61|53
97|53
61|29
47|13
75|47
97|75
47|61
75|61
47|29
75|13
53|13

75,47,61,53,29
97,61,53,29,13
75,29,13
75,97,47,61,53
61,13,29
97,13,75,29,47"""
        lines = test_data.splitlines()
    else:
        data_file = Path.cwd() / "puzzle_data.txt"
        with open(data_file, "r") as f:
            lines = f.readlines()

    for i, line in enumerate(lines):
        lines[i] = line.strip()

    # Puzzle code
    #----------------------------------------------------------------

    # Split out rules from updates
    rules: list[tuple[str]] = []
    updates: list[tuple[str]] = []
    good_updates: list[tuple[str]] = []

    section = "rules"
    for line in lines:
        if line == "":
            section = "updates"
        elif section == "rules":
            rules.append((tuple(line.split("|"))))
        elif section == "updates":
            updates.append((tuple(line.split(","))))


    # In an update, pair all the pages into 2 page combinations, keeping order,
    # and check if the reverse rule exists
    from itertools import combinations

    for update in updates:
        # Generate combinations of 2 pages numbers
        g = combinations(update, 2)
        fail = False
        for (p1, p2) in g:
            # Search if the reverse rule exists, if True then fail update
            for rule in rules:
                if (p2, p1) == rule:
                    fail = True
                    break
            if fail == True:
                break
        if fail == False:
            good_updates.append(update)


    # Count the mid-pages
    total = 0
    for update in good_updates:
        print(update[int((len(update)-1)/2)])
        total += int(update[int((len(update)-1)/2)])

    print(f"Total: {total}")

    # ans: 5651




if __name__ == "__main__":
    main(sys.argv)


