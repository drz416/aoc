import sys
from pathlib import Path

# Run with test data    -> python3 -m d#p#
# Run with puzzle data  -> python3 -m d#p# X (any argument)

def main(argv: list[str]):
    # Prep Code
    lines: list[str]

    if len(argv) == 1:
        test_data = """\
rn=1,cm-,qp=3,cm=2,qp-,pc=4,ot=9,ab=5,pc-,pc=6,ot=7"""
        lines = test_data.splitlines()
    else:
        data_file = Path.cwd() / "puzzle_data.txt"
        with open(data_file, "r") as f:
            lines = f.readlines()

    for i, line in enumerate(lines):
        lines[i] = line.strip()

    # Puzzle code
    #----------------------------------------------------------------


    sequence = lines[0].split(',')
    print(sequence)

    sum = 0
    for seq in sequence:
        sum += hash_str(seq)
    
    print("Sum:", sum)


def hash_str(string: str) -> int:
    current_value = 0
    for c in string:
        current_value += ord(c)
        current_value *= 17
        current_value = current_value % 256
    return current_value

main(sys.argv)


