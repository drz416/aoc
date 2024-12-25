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
Register A: 117440
Register B: 0
Register C: 0

Program: 0,3,5,4,3,0"""
        lines = test_data.splitlines()
    else:
        data_file = Path.cwd() / "puzzle_data.txt"
        with open(data_file, "r") as f:
            lines = f.readlines()

    for i, line in enumerate(lines):
        lines[i] = line.strip()

    # Puzzle code
    #----------------------------------------------------------------

    for line in lines:
        if line.startswith("Program"):
            prog_raw = line.split(": ")[1]
            prog = tuple(map(int, prog_raw.split(",")))
            prog_raw += ","
        else:
            pass
    
    i = 0
    while True:
        if i % 1000000 == 0:
            print(f"{i}..")
        if run_prog(i, prog, prog_raw):
            break
        i += 1

    print(f"Ans at a={i}")
        
        

    



def run_prog(a_val: int, prog: tuple[int], prog_raw: str) -> bool:
    a = [a_val]
    b = [0]
    c = [0]

    index = 0
    out = ""

    combo = {
        0: [0],
        1: [1],
        2: [2],
        3: [3],
        4: a,
        5: b,
        6: c,
    }

    while index < len(prog):
        opcode = prog[index]
        operand = prog[index+1]

        # print("")
        # print("a =", a[0])
        # print("b =", b[0])
        # print("c =", c[0])
        # print(f"{opcode=} {operand=}")        


        if opcode == 0:
            # The adv instruction (opcode 0) performs division. The numerator
            # is the value in the A register. The denominator is found by
            # raising 2 to the power of the instruction's combo operand. (So,
            # an operand of 2 would divide A by 4 (2^2); an operand of 5 would
            # divide A by 2^B.) The result of the division operation is
            # truncated to an integer and then written to the A register.
            a[0] = a[0] // (2 ** combo[operand][0])
            index += 2

        elif opcode == 1:
            # The bxl instruction (opcode 1) calculates the bitwise XOR of
            # register B and the instruction's literal operand, then stores
            # the result in register B.
            b[0] = b[0] ^ operand
            index += 2

        elif opcode == 2:
            # The bst instruction (opcode 2) calculates the value of its combo
            # operand modulo 8 (thereby keeping only its lowest 3 bits), then
            # writes that value to the B register.
            b[0] = combo[operand][0] % 8
            index += 2

        elif opcode == 3:
            # The jnz instruction (opcode 3) does nothing if the A register is
            # 0. However, if the A register is not zero, it jumps by setting
            # the instruction pointer to the value of its literal operand; if
            # this instruction jumps, the instruction pointer is not increased
            # by 2 after this instruction.
            if a[0] == 0:
                index += 2
            else:
                index = operand

        elif opcode == 4:
            # The bxc instruction (opcode 4) calculates the bitwise XOR of
            # register B and register C, then stores the result in register B.
            # (For legacy reasons, this instruction reads an operand but ignores it.)
            b[0] = b[0] ^ c[0]
            index += 2

        elif opcode == 5:
            # The out instruction (opcode 5) calculates the value of its combo
            # operand modulo 8, then outputs that value. (If a program outputs
            # multiple values, they are separated by commas.)
            out += f"{combo[operand][0] % 8},"
            index += 2

        elif opcode == 6:
            # The bdv instruction (opcode 6) works exactly like the adv
            # instruction except that the result is stored in the B register.
            # (The numerator is still read from the A register.)
            b[0] = a[0] // (2 ** combo[operand][0])
            index += 2

        elif opcode == 7:
            # The cdv instruction (opcode 7) works exactly like the adv
            # instruction except that the result is stored in the C register.
            # (The numerator is still read from the A register.)
            c[0] = a[0] // (2 ** combo[operand][0])
            index += 2
        

        if prog_raw.startswith(out) == False:
            return False
        
    return prog_raw == out

    # print("")
    # total = 0

    # print(f"Total: {total}")
    # ans: 


        





if __name__ == "__main__":
    main(sys.argv)


