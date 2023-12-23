import sys
from pathlib import Path

# Run with test data    -> python3 -m d#p#
# Run with puzzle data  -> python3 -m d#p# X (any argument)

def main(argv: list[str]):
    # Prep Code
    lines: list[str]

    if len(argv) == 1:
        test_data = """\
0 3 6 9 12 15
1 3 6 10 15 21
10 13 16 21 30 45"""
        lines = test_data.splitlines()
    else:
        data_file = Path.cwd() / "puzzle_data.txt"
        with open(data_file, "r") as f:
            lines = f.readlines()

    for i, line in enumerate(lines):
        lines[i] = line.strip()

    # Puzzle code
    #----------------------------------------------------------------

    s = 0
    for line in lines:
        sequence: list[int] = []
        for number in line.split():
            sequence.append(int(number))
        next_digit = get_next(sequence)
        s += next_digit
        print(sequence, next_digit, s)
        



def get_next(sequence: list[int]) -> int:
    # Pass in a sequence and return its next number in sequence
    for number in sequence:
        if number != 0:
            break
    else:
        return 0
    
    sub_sequence: list[int] = []
    for i, number in enumerate(sequence[0:-1]):
        sub_sequence.append(sequence[i+1] - number)
    return sequence[-1] + get_next(sub_sequence)

main(sys.argv)

#answer: 1974232246