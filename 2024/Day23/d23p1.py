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
kh-tc
qp-kh
de-cg
ka-co
yn-aq
qp-ub
cg-tb
vc-aq
tb-ka
wh-tc
yn-cg
kh-ub
ta-co
de-co
tc-td
tb-wq
wh-td
ta-ka
td-qp
aq-cg
wq-ub
ub-vc
de-ta
wq-aq
wq-vc
wh-yn
ka-de
kh-ta
co-tc
wh-qp
tb-vc
td-yn"""
        lines = test_data.splitlines()
    else:
        data_file = Path.cwd() / "puzzle_data.txt"
        with open(data_file, "r") as f:
            lines = f.readlines()

    for i, line in enumerate(lines):
        lines[i] = line.strip()

    # Puzzle code
    #----------------------------------------------------------------
    from time import time
    start_time = time()
    # Build a dict of all computers with sets to hold their linkages
    computers: dict[set[str]] = {}

    for line in lines:
        c1, c2 = line.split("-")
        computers[c1] = set()
        computers[c2] = set()
    
    # Read in all the linkages
    for line in lines:
        c1, c2 = line.split("-")
        computers[c1].add(c2)
        computers[c2].add(c1)
    
    # Start with each computer and check its neighbours looking for a group of 3
    groups_of_three: set[tuple[str]] = set()
    
    for comp1, comp1_neighbours in computers.items():
        for comp2 in comp1_neighbours:
            comp2_neighbours = computers[comp2]

            if len(comp1_neighbours & comp2_neighbours) == 0:
                continue

            for comp3 in (comp1_neighbours & comp2_neighbours):
                groups_of_three.add(tuple(sorted([comp1, comp2, comp3])))

    # Count groups of 3 with a "t"
    
    ans = 0
    for group in groups_of_three:
        any_start_with_t = any(comp.startswith("t") for comp in group)
        if any_start_with_t:
            ans += 1
            print(group)

    print(f"Ans: {ans}")
    print(time() - start_time)

    # ans: 1304




if __name__ == "__main__":
    main(sys.argv)


