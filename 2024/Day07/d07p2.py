import sys
import re
from collections import deque, Counter, defaultdict
from pathlib import Path
from pprint import pprint
from functools import partial, lru_cache
from itertools import product

# Run with test data    -> python3 -m d#p#
# Run with puzzle data  -> python3 -m d#p# X (any argument)

def main(argv: list[str]):
    # Prep Code
    lines: list[str]

    if len(argv) == 1:
        test_data = """\
190: 10 19
3267: 81 40 27
83: 17 5
156: 15 6
7290: 6 8 6 15
161011: 16 10 13
192: 17 8 14
21037: 9 7 18 13
292: 11 6 16 20"""
        lines = test_data.splitlines()
    else:
        data_file = Path.cwd() / "puzzle_data.txt"
        with open(data_file, "r") as f:
            lines = f.readlines()

    for i, line in enumerate(lines):
        lines[i] = line.strip()

    # Puzzle code
    #----------------------------------------------------------------

    import operator

    all_values: tuple[str] = ()
    all_terms: list[tuple[str]] = []
    operators = {
        "*": operator.mul,
        "+": operator.add,
        "|": concactenation_operator,
    }

    for line in lines:
        lhs, rhs = line.split(": ")[0], line.split(": ")[1]
        all_values += (int(lhs), )
        rhs = tuple(int(x) for x in rhs.split(" "))
        all_terms.append(rhs)

    # Process each equation
    valid_equations = 0
    total_values = 0

    for value, terms in zip(all_values, all_terms):
        operator_positions = len(terms) - 1
        print(f"{value:<15}={str(terms):50} ", end="")

        # For each equation, check all the operator combinations
        for op_combination in product("*+|", repeat=operator_positions):
            # print(f"  {op_combination=}")
            ans = terms[0]
            for i, op in enumerate(op_combination):
                ans = operators[op](ans, terms[i+1])

            # print(f"    {value=}, {ans=} ", end="")

            if value == ans:
                valid_equations += 1
                total_values += value
                print(f"VALID! for {op_combination} ", end="")
                break
        

        print(f"{valid_equations=} {total_values=}")


    print(f"Total: {valid_equations}")
    # ans: 333027885676693

def concactenation_operator(a: int, b: int) -> int:
    return int(str(a) + str(b))


if __name__ == "__main__":
    main(sys.argv)


