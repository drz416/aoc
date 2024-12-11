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
    failed_updates: list[tuple[str]] = []
    fixed_updates: list[tuple[str]] = []

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
        fail = False
        # Generate combinations of 2 pages numbers
        for (p1, p2) in combinations(update, 2):
            # Search if the reverse rule exists, if True then fail update
            for rule in rules:
                if (p2, p1) == rule:
                    failed_updates.append(update)
                    fail = True
                    break
            if fail == True:
                break
        if fail == False:
            good_updates.append(update)


    # Fix failed updates
    # Work from first page, and go through rules and make swaps where errors are found
    for update in failed_updates:
        update = list(update)
        p1 = 0
        # print("")
        # print(f"{update=}")

        while p1 < (len(update) - 1):
            # print(list(range(p1 + 1, len(update))))
            swapped = False
            for p2 in range(p1 + 1, len(update)):
                # print(f"{p1=} {p2=}")
                (a, b) = (update[p1], update[p2])
                # print(f"{(a, b)=}")
                for rule in rules:
                    if (b, a) == rule:
                        (update[p1], update[p2]) = (b, a)
                        swapped = True
                        # print("swap!")
                        break
                if swapped == True:
                    break
                # print("ok!")
            if swapped == False:
                p1 += 1
        fixed_updates.append(update)

    pprint(failed_updates)
    pprint(fixed_updates)
                




    # Count the mid-pages
    total = 0
    for update in fixed_updates:
        #print(update[int((len(update)-1)/2)])
        total += int(update[int((len(update)-1)/2)])

    print(f"Total: {total}")

    # ans: 4743



if __name__ == "__main__":
    main(sys.argv)


