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

    wirings: list[list[tuple[int]]] = []
    joltages: list[tuple[int]] = []

    # eg: [.##.] (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}
    pattern_outer = r'\[(.+)\]' + r'.+' + r'\{(.+)\}'
    pattern_inner = r'\((.+?)\)'
    pobj_out = re.compile(pattern_outer)
    pobj_in = re.compile(pattern_inner)

    for row in rows:
        # Read in joltage requirements, store in tuple
        _, jolts = pobj_out.findall(row)[0]
        joltages.append(tuple(map(int, jolts.split(","))))
        digits = len(joltages[-1])

        # Read in button wirings, and inteprent which positions of joltage
        # requirements they affect
        wrgs_all = pobj_in.findall(row)
        wrgs = []
        for w in wrgs_all:
            wrgs_acc = [0]*digits
            for dig in w.split(","):
                wrgs_acc[int(dig)] = 1
            wrgs.append(tuple(wrgs_acc))
        wirings.append(wrgs)

    from functools import cache
    from itertools import combinations, product

    def patterns(coeffs: list[tuple[int, ...]]) -> dict[tuple[int, ...], dict[tuple[int, ...], int]]:
        num_buttons = len(coeffs)
        num_variables = len(coeffs[0])
        out = {parity_pattern: {} for parity_pattern in product(range(2), repeat=num_variables)}
        for num_pressed_buttons in range(num_buttons+1):
            for buttons in combinations(range(num_buttons), num_pressed_buttons):
                pattern = tuple(map(sum, zip((0,) * num_variables, *(coeffs[i] for i in buttons))))
                parity_pattern = tuple(i%2 for i in pattern)
                if pattern not in out[parity_pattern]:
                    out[parity_pattern][pattern] = num_pressed_buttons
        return out

    def solve_single(coeffs: list[tuple[int, ...]], goal: tuple[int, ...]) -> int:
        pattern_costs = patterns(coeffs)
        @cache
        def solve_single_aux(goal: tuple[int, ...]) -> int:
            if all(i == 0 for i in goal): return 0
            answer = 1000000
            for pattern, pattern_cost in pattern_costs[tuple(i%2 for i in goal)].items():
                if all(i <= j for i, j in zip(pattern, goal)):
                    new_goal = tuple((j - i)//2 for i, j in zip(pattern, goal))
                    answer = min(answer, pattern_cost + 2 * solve_single_aux(new_goal))
            return answer
        return solve_single_aux(goal)

    def solve(lines: str):
        score = 0
        # lines = raw.splitlines()
        for I, L in enumerate(lines, 1):
            _, *coeffs, goal = L.split()
            goal = tuple(int(i) for i in goal[1:-1].split(","))
            coeffs = [[int(i) for i in r[1:-1].split(",")] for r in coeffs]
            coeffs = [tuple(int(i in r) for i in range(len(goal))) for r in coeffs]

            subscore = solve_single(coeffs, goal)
            print(f'Line {I}/{len(lines)}: answer {subscore}')
            score += subscore
        print(score)

    # solve(open('input/10.test').read())
    solve(rows)





    ans = 0



    print(f"\nAns: {ans}")

    # ans: ##




#----------------------------------------------------------------



# Data load and caling main()
#----------------------------------------------------------------
if __name__ == "__main__":
    # Prep Data
    rows: list[str]

    if len(sys.argv) == 1:
        # Paste test example data here
        test_data = """\
[.##.] (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}
[...#.] (0,2,3,4) (2,3) (0,4) (0,1,2) (1,2,3,4) {7,5,12,7,2}
[.###.#] (0,1,2,3,4) (0,3,4) (0,1,2,4,5) (1,2) {10,11,11,5,10,5}"""
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


