import sys
from pathlib import Path

# Run module via python3 -m d#p#, any argument passed uses puzzle data
# no argument passed uses test data 

def main(argv: list[str]):
    # Prep Code
    lines: list[str]

    if len(argv) == 1:
        test_data = """\
Time:      7  15   30
Distance:  9  40  200"""
        lines = test_data.splitlines()
    else:
        data_file = Path.cwd() / "puzzle_data.txt"
        with open(data_file, "r") as f:
            lines = f.readlines()

    for i, line in enumerate(lines):
        lines[i] = line.strip()

    # Puzzle code
    


main(sys.argv)