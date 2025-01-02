import sys
import re
from pathlib import Path
from pprint import pprint
from time import time, time_ns
from collections import deque, Counter, defaultdict
from functools import partial, lru_cache
from itertools import product, combinations

# Run with test data    -> python3 -m d#p#
# Run with puzzle data  -> python3 -m d#p# X (any argument)

def main(lines: list[str]):

    # Build a dict of all computers with sets to hold their linkages
    computers: dict[str, set[str]] = {}

    for line in lines:
        c1, c2 = line.split("-")
        computers[c1] = set()
        computers[c2] = set()
    
    # Read in all the linkages
    for line in lines:
        c1, c2 = line.split("-")
        computers[c1].add(c2)
        computers[c2].add(c1)
    
    largest = [0]
    largest_network = ()
    i = 0
    it = len(computers) * (len(computers) - 1)
    for comp1, comp2 in combinations(computers, 2):
        # if (comp1 in "co,de,ka,ta") and (comp2 in "co,de,ka,ta"):
        #     breakpoint()
        print(f"{i:6} / {it}")
        i += 1

        if comp2 not in computers[comp1]:
            # no link between computers
            continue

        shared_network = computers[comp1] & computers[comp2]
        if len(shared_network) == 0:
            # computers are linked but they share no other connections
            continue

        if len(shared_network) + 2 <= largest[0]:
            # no potential for a larger network
            continue

        # At least 1 other computer is shared, go through them and build a network
        curr_network = {comp1, comp2}

        largest_network = find_largest(computers, curr_network, shared_network, largest, largest_network)

    
    ans = largest

    print(f"Ans: {ans}")
    print(largest_network)
    print(f"{','.join(sorted(largest_network))}")
    # ans: ao,es,fe,if,in,io,ky,qq,rd,rn,rv,vc,vl

def find_largest(computers: dict[str, set[str]],
                 curr_network: set,
                 potential_network: set,
                 largest: list[int],
                 largest_network: tuple
                 ) -> tuple[int, set]:

    for comp3 in potential_network:
        new_current = curr_network.copy()
        new_current.add(comp3)
        new_potential = computers[comp3] & potential_network
        
        if len(new_current) + len(new_potential) <= largest[0]:
            continue
        
        if len(new_potential) == 0:
            if len(new_current) > largest[0]:
                largest[0] = len(new_current)
                largest_network = tuple(new_current)
            continue
        
        largest_network = find_largest(computers, new_current, new_potential, largest, largest_network)

    return largest_network






# Setup code
#----------------------------------------------------------------

if __name__ == "__main__":
    # Prep Code
    lines: list[str]

    if len(sys.argv) == 1:
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
    
    start_time = time()
    main(lines)
    print("")
    print(f"Time in main(): {time() - start_time:.06f}s")


