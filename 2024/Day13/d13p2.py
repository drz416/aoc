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
Button A: X+94, Y+34
Button B: X+22, Y+67
Prize: X=8400, Y=5400

Button A: X+26, Y+66
Button B: X+67, Y+21
Prize: X=12748, Y=12176

Button A: X+17, Y+86
Button B: X+84, Y+37
Prize: X=7870, Y=6450

Button A: X+69, Y+23
Button B: X+27, Y+71
Prize: X=18641, Y=10279"""
        lines = test_data.splitlines()
    else:
        data_file = Path.cwd() / "puzzle_data.txt"
        with open(data_file, "r") as f:
            lines = f.readlines()

    for i, line in enumerate(lines):
        lines[i] = line.strip()

    # Puzzle code
    #----------------------------------------------------------------

    # Read-in machine definitions
    machines = {}
    button_a: tuple[int]
    button_b: tuple[int]
    prize: tuple[int]
    offset = 10000000000000

    i = 0
    for line in lines:
        if line[0:8] == "Button A":
            xy = line[10:].split(", ")
            button_a = (int(xy[0][2:]), int(xy[1][2:]))
            continue
        if line[0:8] == "Button B":
            xy = line[10:].split(", ")
            button_b = (int(xy[0][2:]), int(xy[1][2:]))
            continue
        if line[0:5] == "Prize":
            xy = line[7:].split(", ")
            prize = (int(xy[0][2:])+offset, int(xy[1][2:])+offset)
            continue
        if line == "":
            machine = {
                "a": button_a,
                "b": button_b,
                "p": prize,
            }
            machines[i] = machine
            i += 1
    machine = {
        "a": button_a,
        "b": button_b,
        "p": prize,
    }
    machines[i] = machine

    solutions: list[int] = []

    for machine in machines.values():
        det = determinant(machine)
        pprint(f"{machine} {det=}")
        if det == 0:
            continue

        presses_a = (machine["b"][1] * machine["p"][0]
                   - machine["b"][0] * machine["p"][1])
        presses_b = (machine["a"][0] * machine["p"][1]
                   - machine["a"][1] * machine["p"][0])
        
        if type(divide_w_int(presses_a, det)) == int and type(divide_w_int(presses_b, det)) == int:
            solutions.append((divide_w_int(presses_a, det), divide_w_int(presses_b, det)))
            print(f"  Soltuion at {divide_w_int(presses_a, det), divide_w_int(presses_b, det)}")
    
    print(solutions)

    tokens = 0
    for x, y in solutions:
        if x >= 0 and y >= 0:
            tokens += x * 3 + y

    print(tokens)
    # ans: 82570698600470




def determinant(machine: dict) -> int:
    print(machine)
    return machine["a"][0]*machine["b"][1] - machine["a"][1]*machine["b"][0]


def divide_w_int(numerator: int, denominator: int) -> float | int:
    int_ans = numerator // denominator
    if int_ans * denominator == numerator:
        return int_ans
    else:
        return numerator / denominator
        






if __name__ == "__main__":
    main(sys.argv)


