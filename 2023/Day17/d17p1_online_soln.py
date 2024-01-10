# FYI Part 1 and Part 2 are not my solutions

import heapq

import sys
from pathlib import Path

# Run with test data    -> python3 -m d#p#
# Run with puzzle data  -> python3 -m d#p# X (any argument)

def main(argv: list[str]):
    # Prep Code
    lines: list[str]

    if len(argv) == 1:
        test_data = """\
2413432311323
3215453535623
3255245654254
3446585845452
4546657867536
1438598798454
4457876987766
3637877979653
4654967986887
4564679986453
1224686865563
2546548887735
4322674655533"""
        lines = test_data.splitlines()
    else:
        data_file = Path.cwd() / "puzzle_data.txt"
        with open(data_file, "r") as f:
            lines = f.readlines()

    for i, line in enumerate(lines):
        lines[i] = line.strip()

    # Puzzle code
    #----------------------------------------------------------------

    grid = {
        (r, c): int(v) for r, line in enumerate(lines) for c, v in enumerate(line.strip())
    }
    height = len(lines)
    width = len(lines[0].strip())

    queue = [(0, 0, 0, 0, 0, 0)]
    seen = set()

    while queue:
        heat, r, c, dr, dc, s = heapq.heappop(queue)

        if (r, c, dr, dc, s) in seen:
            continue

        if r == height - 1 and c == width - 1:
            part1 = heat
            break

        seen.add((r, c, dr, dc, s))

        for next_dr, next_dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            next_r = r + next_dr
            next_c = c + next_dc
            if next_r < 0 or next_r >= height or next_c < 0 or next_c >= width:
                continue  # off the grid, not valid
            if next_dr == -dr and next_dc == -dc:
                continue  # can't go backwards
            if next_dr == dr and next_dc == dc:
                if s < 3:
                    heapq.heappush(
                        queue,
                        (
                            heat + grid[(next_r, next_c)],
                            next_r,
                            next_c,
                            next_dr,
                            next_dc,
                            s + 1,
                        ),
                    )
                else:
                    continue
            else:
                heapq.heappush(
                    queue,
                    (heat + grid[(next_r, next_c)], next_r, next_c, next_dr, next_dc, 1),
                )

    print(f"Part 1: {part1}")

    


main(sys.argv)


