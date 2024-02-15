import sys
import re
from collections import deque, Counter
from pathlib import Path
from pprint import pprint

# Run with test data    -> python3 -m d#p#
# Run with puzzle data  -> python3 -m d#p# X (any argument)

def main(argv: list[str]):
    # Prep Code
    lines: list[str]

    if len(argv) == 1:
        test_data = """\
19, 13, 30 @ -2,  1, -2
18, 19, 22 @ -1, -1, -2
20, 25, 34 @ -2, -2, -4
12, 31, 28 @ -1, -2, -1
20, 19, 15 @  1, -5, -3"""
        lines = test_data.splitlines()
    else:
        data_file = Path.cwd() / "puzzle_data.txt"
        with open(data_file, "r") as f:
            lines = f.readlines()

    for i, line in enumerate(lines):
        lines[i] = line.strip()

    # Puzzle code
    #----------------------------------------------------------------

    # Build list of stone paths
    stones: list[StonePath] = []
    for line in lines:
        line = line.replace(' ', '')
        first_split = line.split('@')
        position, velocity = first_split[0].split(','), first_split[1].split(',')
        stones.append(StonePath(position, velocity))
    # for stone in stones:
    #     print(stone)

    # Initialize conditions
    if len(argv) == 1:
        MIN_X, MAX_X = 7, 27
    else:
        MIN_X, MAX_X = 200000000000000, 400000000000000
    MIN_Y, MAX_Y = MIN_X, MAX_X
    StonePath.min_x = MIN_X
    StonePath.max_x = MAX_X
    StonePath.min_y = MIN_Y
    StonePath.max_y = MAX_Y

    # Test stone paths
    inside_crosses = 0
    for i, stone_path1 in enumerate(stones):
        for j in range(i+1, len(stones)):
            stone_path2 = stones[j]
            if stone_path1.parallel(stone_path2):
                # print(f"({str(stone_path1)})-({str(stone_path2)}), Parallel: True")
                continue
            # print(f"({str(stone_path1)})-({str(stone_path2)}), Parallel: False, Crosses Inside: {stone_path1.cross_inside(stone_path2)}, Crosses: {stone_path1.cross_point(stone_path2)}")
            if stone_path1.cross_inside(stone_path2):
                inside_crosses += 1
    
    print(inside_crosses)
    




class StonePath():
    min_x: int
    max_x: int
    min_y: int
    max_y: int

    def __init__(self, position: list[str], velocity: list[str]) -> None:
        self.x, self.y, self.z = (
            int(position[0]),
            int(position[1]),
            int(position[2]))
        self.dx, self.dy, self.dz = (
            int(velocity[0]),
            int(velocity[1]),
            int(velocity[2]))

    def parallel(self, other_path: "StonePath") -> bool:
        self_slope = self.dy / self.dx
        other_slope = other_path.dy / other_path.dx
        return self_slope == other_slope
    
    def cross_point(self, other_path: "StonePath") -> tuple[float]:
        """Returns tuple[float] -> (x, y)"""
        # Math explained at end of file
        bx1, by1, bz1 = self.x, self.y, self.z
        mx1, my1, mz1 = self.dx, self.dy, self.dz
        bx2, by2, bz2 = other_path.x, other_path.y, other_path.z
        mx2, my2, mz2 = other_path.dx, other_path.dy, other_path.dz

        t1 = (my2*(bx1 - bx2) / mx2 + by2 - by1) / (my1 - my2*mx1 / mx2)
        t2 = (mx1*t1 + bx1 - bx2) / mx2

        x = mx1 * t1 + bx1
        y = my1 * t1 + by1
        return x, y, t1, t2
    
    def cross_inside(self, other_path: "StonePath") -> bool:
        x, y, t1, t2 = self.cross_point(other_path)
        if t1 < 0 or t2 < 0:
            return False
        if x >= self.min_x and x <= self.max_x:
            if y >= self.min_y and y <= self.max_y:
                return True
        return False

    
    def __str__(self) -> str:
        return f"{self.x}, {self.y}, {self.z} @ {self.dx}, {self.dy}, {self.dz}"

if __name__ == "__main__":
    main(sys.argv)



## Math behind lines crossing
#
# trajectory1: (Dx1(t), Dy1(t), Dz1(t))
# trajectory2: (Dx2(t), Dy2(t), Dz2(t))
#
# Collision when:
# trajectory1 = trajectory2
# (Dx1(t), Dy1(t), Dz1(t)) = (Dx2(t), Dy2(t), Dz2(t))
#
# x Collision:
# Dx1(t) = (Dx2(t)) 
# mx1*t + bx1 = mx2*t + bx2
# mx1*t - mx2*t = bx2 - bx1
# t = (bx2 - bx1) / (mx1 - mx2)
# 
# y Collision:
# Dy1(t) = (Dy2(t))
# t = (by2 - by1) / (my1 - my2)


