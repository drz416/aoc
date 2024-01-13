import re
from pprint import pprint

import sys
from pathlib import Path

# Run with test data    -> python3 -m d#p#
# Run with puzzle data  -> python3 -m d#p# X (any argument)

def main(argv: list[str]):
    # Prep Code
    lines: list[str]

    if len(argv) == 1:
        test_data = """\
R 6 (#70c710)
D 5 (#0dc571)
L 2 (#5713f0)
D 2 (#d2c081)
R 2 (#59c680)
D 2 (#411b91)
L 5 (#8ceee2)
U 2 (#caa173)
L 1 (#1b58a2)
U 2 (#caa171)
R 2 (#7807d2)
U 3 (#a77fa3)
L 2 (#015232)
U 2 (#7a21e3)"""
        lines = test_data.splitlines()
    else:
        data_file = Path.cwd() / "puzzle_data.txt"
        with open(data_file, "r") as f:
            lines = f.readlines()

    for i, line in enumerate(lines):
        lines[i] = line.strip()

    # Puzzle code
    #----------------------------------------------------------------

    START_VERTEX = (0, 0)
    current_vertex = START_VERTEX
    verticies: list[tuple[int]] = []
    verticies.append(current_vertex)

    pattern = r'(?P<unused1>.)\s(?P<unused2>.*)\s\(#(?P<encoding>.*)\)'
    p_obj = re.compile(pattern)

    sum_lengths = 0
    # Map verticies in trench (this method uses matrix 2x2 determinantes to
    # calculate the area of an arbitrary polygon)
    for line in lines:
        encoding = p_obj.search(line)['encoding']
        direction = int(encoding[-1])
        length = int(encoding[0:-1], 16)
        sum_lengths += length
        
        # 0 means R, 1 means D, 2 means L, and 3 means U
        if direction == 0:
            current_vertex = (current_vertex[0], current_vertex[1] + length)
        elif direction == 1:
            current_vertex = (current_vertex[0] + length, current_vertex[1])
        elif direction == 2:
            current_vertex = (current_vertex[0], current_vertex[1] - length)
        elif direction == 3:
            current_vertex = (current_vertex[0] - length, current_vertex[1])
        else:
            raise ValueError("Unrecognized direction :", direction)
        verticies.append(current_vertex)
    # pprint(verticies)

    sum = 0
    for i in range(len(verticies) - 1):
        sum += determinant(verticies[i], verticies[i+1])

    print(sum, abs(sum), abs(sum)/2)
    print(sum_lengths, sum_lengths/2, sum_lengths/2+1)
    print(abs(sum)/2 + sum_lengths/2+1)


def determinant(point1: tuple[int], point2: tuple[int]) -> int:
    return point1[0] * point2[1] - point1[1] * point2[0]


main(sys.argv)


