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
1
2
3
2024"""
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

    secrets_container = [20_000_000] * 2001
    prices_container = [0] * 2001
    changes_container = [0] * 2001
    sequences: list[dict] = []
    possible_sequences = set()

    # go through each buyer
    for row, line in enumerate(lines):
        secret = int(line)
        secrets_container[0] = secret
        prices_container[0] = secret % 10
        sequences.append({})
        

        # log its secrets, prices and changes
        for i in range(1, 2001):
            secrets_container[i] = evolution3(evolution2(evolution1(secrets_container[i-1])))
            prices_container[i] = secrets_container[i] % 10
            changes_container[i] = prices_container[i] - prices_container[i-1]
        
        # go through log and record all initial 4 step prices
        for j in range(4, 2001):
            sequences[row].setdefault((changes_container[j-3],
                                       changes_container[j-2],
                                       changes_container[j-1],
                                       changes_container[j],
                                       ), prices_container[j])
            possible_sequences.add((changes_container[j-3],
                                    changes_container[j-2],
                                    changes_container[j-1],
                                    changes_container[j],
                                    ))

    ans = 0
    for chg_sequence in possible_sequences:
        sum = 0
        for entire_sequence in sequences:
            try:
                sum += entire_sequence[chg_sequence]
            except KeyError:
                continue
        ans = max(ans, sum)
        

    print(f"Ans: {ans}")
    # ans: 2272

def evolution1(number: int) -> int:
    return ((number * 64) ^ number) % 16_777_216

def evolution2(number: int) -> int:
    return ((number // 32) ^ number) % 16_777_216

def evolution3(number: int) -> int:
    return ((number * 2048) ^ number) % 16_777_216


if __name__ == "__main__":
    main(sys.argv)


