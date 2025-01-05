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

    # Setup containers
    example_wires: dict[str, bool] = {}
    gates: list[list[str]] = []
    x_len = y_len = z_len = 0

    from typing import Callable
    from operator import and_, or_, xor
    op: dict[str, Callable[[bool, bool], bool]] = {
        "AND": and_,
        "OR": or_,
        "XOR": xor
    }

    # Read in initial state
    reading_gates = False
    for line in lines:
        if line == "":
            reading_gates = True
            continue
        if not reading_gates:
            wire, init_state = line.split(": ")
            example_wires[wire] = True if init_state=="1" else False
            if wire[0] == "x":
                x_len += 1
            if wire[0] == "y":
                y_len += 1
            continue
        in1, gate, in2, _, out = line.split(" ")
        gates.append([in1, in2, gate, out])      # note order is different
        if out[0] == "z":
            z_len += 1

    if len(sys.argv) == 1:
        func = lambda x, y: x & y
    else:
        func = lambda x, y: x + y

    test_x = (2 ** x_len) // 2
    test_y = (2 ** y_len) // 2
    test_z = func(test_x, test_y)
    initial_wires = gen_input_wires(test_x, test_y, x_len)

    # For each 4 gate combination, check the 3 possible swaps for a functioning
    # assembly of gates
    # (ABCD) -> (BADC), (CADB), (DACB)

    i = 0
    swap = 0
    for a, b, c, d in combinations(range(len(gates)), 4):
        if i % 100_000 == 0:
            print(i)
        i += 1

        # 1st swap
        gates[b][3], gates[a][3], gates[d][3], gates[c][3] = gates[a][3], gates[b][3], gates[c][3], gates[d][3]
        if test_z == calc_z(initial_wires, gates, op, z_len):
            swap = 1
            break
        gates[a][3], gates[b][3], gates[c][3], gates[d][3] = gates[b][3], gates[a][3], gates[d][3], gates[c][3]

        # 2nd swap
        gates[c][3], gates[a][3], gates[d][3], gates[b][3] = gates[a][3], gates[b][3], gates[c][3], gates[d][3]
        if test_z == calc_z(initial_wires, gates, op, z_len):
            swap = 2
            break
        gates[a][3], gates[b][3], gates[c][3], gates[d][3] = gates[c][3], gates[a][3], gates[d][3], gates[b][3]

        # 3nd swap
        gates[d][3], gates[a][3], gates[c][3], gates[b][3] = gates[a][3], gates[b][3], gates[c][3], gates[d][3]
        if test_z == calc_z(initial_wires, gates, op, z_len):
            swap = 3
            break
        gates[a][3], gates[b][3], gates[c][3], gates[d][3] = gates[d][3], gates[a][3], gates[c][3], gates[b][3]


    print((a, b, c, d))
    print(f"{swap=}")

    # ans: this works for the example data, but not for the puzzle data
    # There are 222 gates, and 222 choose 8 (4 pairs) gives about 10^14
    # combinations. Can't use brute force

def gen_input_wires(x: int, y: int, bit_len: int) -> dict[str, bool]:
    wires: dict[str, bool] = {}
    x_bin = bin(x)[:1:-1]           # grab the bits, reverse order for indexing
    y_bin = bin(y)[:1:-1]
    for i in range(bit_len):
        try:
            wires[f"x{i:02}"] = True if x_bin[i] == "1" else False
        except IndexError:
            wires[f"x{i:02}"] = False
        try:
            wires[f"y{i:02}"] = True if y_bin[i] == "1" else False
        except IndexError:
            wires[f"y{i:02}"] = False
    return wires

def calc_z(
        initial_wires: dict[str, bool],
        gates: list[list],
        op: dict[str],
        z_len: int) -> int:
    
    wires = initial_wires.copy()
    q: deque[tuple[str]] = deque()
    for gate in gates:
        q.append(tuple(gate))

    while q:
        in1, in2, gate, out = q[0]
        if ((in1 in wires) and (in2 in wires)) == False:
            q.rotate()
            continue
        wires[out] = op[gate](wires[in1], wires[in2])
        q.popleft()

    z = ""
    for i in range(z_len):
        z = ("1" if wires[f"z{i:02}"] else "0") + z
    return int(z, base=2)


# Setup code
#----------------------------------------------------------------

if __name__ == "__main__":
    # Prep Code
    lines: list[str]

    if len(sys.argv) == 1:
        test_data = """\
x00: 0
x01: 1
x02: 0
x03: 1
x04: 0
x05: 1
y00: 0
y01: 0
y02: 1
y03: 1
y04: 0
y05: 1

x00 AND y00 -> z05
x01 AND y01 -> z02
x02 AND y02 -> z01
x03 AND y03 -> z03
x04 AND y04 -> z04
x05 AND y05 -> z00"""
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


