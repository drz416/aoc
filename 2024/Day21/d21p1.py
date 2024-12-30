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
029A
980A
179A
456A
379A"""
        lines = test_data.splitlines()
    else:
        data_file = Path.cwd() / "puzzle_data.txt"
        with open(data_file, "r",) as f:
            lines = f.readlines()

    for i, line in enumerate(lines):
        lines[i] = line.strip()

    # Puzzle code
    #----------------------------------------------------------------

    # Setup lookup maps
    codes = lines

    numpad = {
        "A": {"0": ("<A",),
              "1": ("<^<A", "^<<A",),
              "2": ("<^A", "^<A",),
              "3": ("^A",),
              "4": ("<^<^A", "<^^<A", "^<<^A", "^<^<A", "^^<<A",),
              "5": ("<^^A", "^<^A", "^^<A",),
              "6": ("^^A",),
              "7": ("<^<^^A", "<^^<^A", "<^^^<A", "^<<^^A", "^<^<^A", "^<^^<A",
                    "^^<<^A", "^^<^<A", "^^^<<A",),
              "8": ("<^^^A", "^<^^A", "^^<^A", "^^^<A",),
              "9": ("^^^A",)},
        "0": {"0": ("A",),
              "1": ("^<A",),
              "2": ("^A",),
              "3": ("^>A", ">^A",),
              "4": ("^<^A", "^^<A",),
              "5": ("^^A",),
              "6": ("^^>A", "^>^A", ">>^A",),
              "7": ("^<^^A", "^^<^A", "^^^<A",),
              "8": ("^^^A",),
              "9": ("^^^>A", "^^>^A", "^>^^A", ">^^^A",)},
        "1": {"1": ("A",),
              "2": (">A",),
              "3": (">>A",),
              "4": ("^A",),
              "5": ("^>A", ">^A",),
              "6": ("^>>A", ">^>A", ">>^A",),
              "7": ("^^A",),
              "8": ("^^>A", "^>^A", ">>^A",),
              "9": ("^^>>A", "^>^>A", "^>>^A", ">^^>A", ">^>^A", ">>^^A",)},
        "2": {"2": ("A",),
              "3": (">A",),
              "4": ("<^A", "^<A",),
              "5": ("^A",),
              "6": ("^>A", ">^A",),
              "7": ("<^^A", "^<^A", "^^<A",),
              "8": ("^^A",),
              "9": ("^^>A", "^>^A", ">^^A",)},
        "3": {"3": ("A",),
              "4": ("<<^A", "<^<A", "^<<A",),
              "5": ("<^A", "^<A",),
              "6": ("^A",),
              "7": ("<<^^A", "<^<^A", "<^^<A", "^<<^A", "^<^<A", "^^<<A",),
              "8": ("<^^A", "^<^A", "^^<A",),
              "9": ("^^A",)},
        "4": {"4": ("A",),
              "5": (">A",),
              "6": (">>A",),
              "7": ("^A",),
              "8": ("^>A", ">^A",),
              "9": ("^>>A", ">^>A", ">>^A",)},
        "5": {"5": ("A",),
              "6": (">A",),
              "7": ("<^A", "^<A",),
              "8": ("^A",),
              "9": ("^>A", ">^A",)},
        "6": {"6": ("A",),
              "7": ("<<^A", "<^<A", "^<<A",),
              "8": ("<^A", "^<A",),
              "9": ("^A",)},
        "7": {"7": ("A",),
              "8": (">A",),
              "9": (">>A",)},
        "8": {"8": ("A",),
              "9": (">A",)},
        "9": {"9": ("A",),},
    }

    dirpad = {
        "A": {"A": ("A",),
              "^": ("<A",),
              "<": ("<v<A", "v<<A",),
              "v": ("<vA", "v<A",),
              ">": ("vA",)},
        "^": {"^": ("A",),
              "<": ("v<A",),
              "v": ("vA",),
              ">": ("v>A", ">vA",)},
        "<": {"<": ("A",),
              "v": (">A",),
              ">": (">>A",)},
        "v": {"v": ("A",),
              ">": (">A",)},
        ">": {">": ("A",),},
    }

    reversal_map = {
        "^": "v",
        ">": "<",
        "v": "^",
        "<": ">",
    }

    ans = 0
    for code in codes:
        shortest = 10 ** 10


        # Generate combinations
        # print(code)
        numpad_possibilities = []
        from_key = "A"
        for next_key in code:    
            try:
                numpad_possibilities.append((numpad[from_key][next_key]))
            except KeyError:
                numpad_possibilities.append((reverse_possibilities(numpad[next_key][from_key])))
            from_key = next_key

        for numpad_possibility in product(*numpad_possibilities):
            dirpad1_sequence = "".join(numpad_possibility)
            # print(f"..{dirpad1_sequence}")
            dirpad1_possibilities = []
            from_key = "A"
            for next_key in dirpad1_sequence:
                try:
                    dirpad1_possibilities.append((dirpad[from_key][next_key]))
                except KeyError:
                    dirpad1_possibilities.append((reverse_possibilities(dirpad[next_key][from_key])))
                from_key = next_key
            
            for dirpad1_possibility in product(*dirpad1_possibilities):
                dirpad2_sequence = "".join(dirpad1_possibility)
                # print(f"....{dirpad2_sequence}")
                # if dirpad2_sequence == "v<<A>>^A<A>AvA<^AA>A<vAAA>^A":
                #     breakpoint()
                dirpad2_possibilities = []
                from_key = "A"
                for next_key in dirpad2_sequence:
                    try:
                        dirpad2_possibilities.append((dirpad[from_key][next_key]))
                    except KeyError:
                        dirpad2_possibilities.append((reverse_possibilities(dirpad[next_key][from_key])))
                    from_key = next_key

                for dirpad2_possibility in product(*dirpad2_possibilities):
                    human_sequence = "".join(dirpad2_possibility)
                    # print(f"      {len(human_sequence)}: {human_sequence}")
                    shortest = min(shortest, len(human_sequence))
        print(f"{code} {shortest=}")
        ans += shortest * int(code[:-1])
        # breakpoint()        

    print(f"{ans=}")
    # ans: 152942

@lru_cache
def reverse_possibilities(directions: tuple[str]) -> tuple[str]:
    reversal_map = {
        "^": "v",
        ">": "<",
        "v": "^",
        "<": ">",
    }
    
    reversed_possibilities = tuple()
    for direction in directions:
        rev = ""
        for c in direction[-2::-1]:
            rev += reversal_map[c]
        reversed_possibilities += (rev+"A",)
    return reversed_possibilities




if __name__ == "__main__":
    main(sys.argv)


