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

    wires: dict[str, bool] = {}
    gates: deque[tuple[str]] = deque()

    from typing import Callable
    from operator import and_, or_, xor
    op: dict[str, Callable[[bool, bool], bool]] = {
        "AND": and_,
        "OR": or_,
        "XOR": xor
    }

    reading_gates = False
    for line in lines:
        if line == "":
            reading_gates = True
            continue
        if not reading_gates:
            wire, init_state = line.split(": ")
            wires[wire] = True if init_state=="1" else False
            continue
        in1, gate, in2, _, out = line.split(" ")
        gates.append((in1, in2, gate, out))

    while gates:
        in1, in2, gate, out = gates[0]
        if ((in1 in wires) and (in2 in wires)) == False:
            gates.rotate()
            continue
        wires[out] = op[gate](wires[in1], wires[in2])
        gates.popleft()

    ans = ""
    i = 0

    while True:
        output_position = f"z{i:02}"
        try:
            ans = ("1" if wires[output_position] else "0") + ans
        except KeyError:
            break
        i += 1




    print(f"Ans: {ans} -> {int(ans, base=2)}")

    # ans: 38869984335432







# Setup code
#----------------------------------------------------------------

if __name__ == "__main__":
    # Prep Code
    lines: list[str]

    if len(sys.argv) == 1:
        test_data = """\
x00: 1
x01: 0
x02: 1
x03: 1
x04: 0
y00: 1
y01: 1
y02: 1
y03: 1
y04: 1

ntg XOR fgs -> mjb
y02 OR x01 -> tnw
kwq OR kpj -> z05
x00 OR x03 -> fst
tgd XOR rvg -> z01
vdt OR tnw -> bfw
bfw AND frj -> z10
ffh OR nrd -> bqk
y00 AND y03 -> djm
y03 OR y00 -> psh
bqk OR frj -> z08
tnw OR fst -> frj
gnj AND tgd -> z11
bfw XOR mjb -> z00
x03 OR x00 -> vdt
gnj AND wpb -> z02
x04 AND y00 -> kjc
djm OR pbm -> qhw
nrd AND vdt -> hwm
kjc AND fst -> rvg
y04 OR y02 -> fgs
y01 AND x02 -> pbm
ntg OR kjc -> kwq
psh XOR fgs -> tgd
qhw XOR tgd -> z09
pbm OR djm -> kpj
x03 XOR y03 -> ffh
x00 XOR y04 -> ntg
bfw OR bqk -> z06
nrd XOR fgs -> wpb
frj XOR qhw -> z04
bqk OR frj -> z07
y03 OR x01 -> nrd
hwm AND bqk -> z03
tgd XOR rvg -> z12
tnw OR pbm -> gnj"""
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


