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
AAAA
BBCD
BBCC
EEEC"""
        lines = test_data.splitlines()
    else:
        data_file = Path.cwd() / "puzzle_data.txt"
        with open(data_file, "r") as f:
            lines = f.readlines()

    for i, line in enumerate(lines):
        lines[i] = line.strip()

    # Puzzle code
    #----------------------------------------------------------------

    # Build base grid
    base_grid: list[list[int]] = []
    for line in lines:
        base_grid.append(list(line))
    base_grid_h = len(base_grid)
    base_grid_w = len(base_grid[0])

    # Build bordered grid around brase grid
    grid: list[list[int]] = [['?']*(base_grid_w+2) for _ in range(base_grid_h+2)]
    for i, row in enumerate(base_grid):
        grid[i+1][1:len(row)+1] = row

    # Trackers
    regions: list[Region] = []
    plots: dict[Plot] = {}
    
    # Scan through all plots
    for x, y in product(range(1 ,base_grid_h+1), range(1, base_grid_w+1)):
        # if (x, y) == (3, 7):
        #     breakpoint()
        # Create plot, add to tracker, and set fences
        plt = Plot((x,y), grid[x][y])
        plots[(x,y)] = plt
        plt.remove_left_fence(grid, plots)
        plt.remove_top_fence(grid, plots)

        reg = Region()
        reg.add_plot(plt)
        merged_left = reg.merge_left(grid, plots)
        if merged_left:
            reg = plots[(x,y-1)].region
        
        merged_up = reg.merge_up(grid, plots)
        if merged_left and merged_up:
            regions.remove(reg)
        if merged_left or merged_up:
            continue
        regions.append(reg)


    # for plt in plots.values():
    #     print(plt.crop, plt.borders)

    total = 0
    for i, reg in enumerate(regions):
        area = reg.get_area
        long_fences = reg.count_long_fences(plots)
        
        total += area * long_fences

        print(f"Region {i}: {reg.crop} {area=} {long_fences=}")
        # for plot in reg.plots:
        #     print(" ", plot.crop, plot.position)
    

    print(f"Total: {total}")
    # ans: 859494



class Plot():
    def __init__(self, position: tuple[int], crop: str) -> None:
        self.position = position
        self.crop = crop
        self.region = None
        self.borders = {
            "up": "fence",
            "right": "fence",
            "down": "fence",
            "left": "fence",
        }

    def remove_left_fence(self, grid, plots: dict["Plot"]) -> None:
        left_x = self.position[0]
        left_y = self.position[1]-1
        if grid[left_x][left_y] == '?':
            return
        if plots[(left_x,left_y)].crop == self.crop:
            self.borders["left"] = None
            plots[(left_x,left_y)].borders["right"] = None

    def remove_top_fence(self, grid, plots: dict["Plot"]) -> None:
        top_x = self.position[0]-1
        top_y = self.position[1]
        if grid[top_x][top_y] == '?':
            return
        if plots[(top_x,top_y)].crop == self.crop:
            self.borders["up"] = None
            plots[(top_x,top_y)].borders["down"] = None
    
    @property
    def fences(self) -> int:
        count = 0
        for border in self.borders.values():
            if border == "fence":
                count += 1
        return count
    
    def corners(self, plots: "Plot") -> int:
        # count concave corners
        count_con = 0
        possibilities = (
            ("up", "right"),
            ("right", "down"),
            ("down", "left"),
            ("left", "up"),
        )
        for side1, side2 in possibilities:
            if (self.borders[side1] == "fence") and (self.borders[side2] == "fence"):
                count_con += 1
        
        # count convex corners
        count_cvx = 0
        

        # directions to check: (top right, bottom right, bottom left, top left)
        matching_crop1 = ((-1,0), (1,0), (1,0), (-1,0))
        matching_crop2 = ((0,1), (0,1), (0,-1), (0,-1))
        diff_crop = ((-1,1), (1,1), (1,-1), (-1,-1))

        for (m1x, m1y), (m2x, m2y), (dx, dy) in zip(matching_crop1, matching_crop2, diff_crop):
            # print(f"    {m1x=} {m1y=}, {m2x=} {m2y=} {dx=} {dy=}")
            plt_m1 = (self.position[0]+m1x, self.position[1]+m1y)
            if plt_m1 not in plots:
                continue
            if plots[plt_m1].crop != self.crop:
                continue

            plt_m2 = (self.position[0]+m2x, self.position[1]+m2y)
            if plt_m2 not in plots:
                continue
            if plots[plt_m2].crop != self.crop:
                continue

            plt_d = (self.position[0]+dx, self.position[1]+dy)
            if plt_d not in plots:
                continue
            if plots[plt_d].crop == self.crop:
                continue
            count_cvx += 1

        return count_con + count_cvx
            

class Region():
    def __init__(self):
        self.plots = []
        self.crop = None
    
    def add_plot(self, plot: Plot) -> None:
        if self.crop == None:
            self.crop = plot.crop
        elif self.crop != plot.crop:
            raise TypeError(f"Region crop {self.crop} doesn't match plot crop {plot.crop}")
        self.plots.append(plot)
        plot.region = self

    def merge_left(self, grid, plots) -> bool:
        left_x = self.plots[-1].position[0]
        left_y = self.plots[-1].position[1]-1
        if grid[left_x][left_y] == '?':
            return False
        left_crop = plots[(left_x, left_y)].crop
        if self.crop != left_crop:
            return False
        target_region = plots[(left_x, left_y)].region
        self.merge_into(target_region)
        return True
    
    def merge_up(self, grid, plots) -> bool:
        up_x = self.plots[-1].position[0]-1
        up_y = self.plots[-1].position[1]
        if grid[up_x][up_y] == '?':
            return False
        up_crop = plots[(up_x, up_y)].crop
        if self.crop != up_crop:
            return False
        target_region = plots[(up_x, up_y)].region
        if self == target_region:
            return False
        self.merge_into(target_region)
        return True

    def merge_into(self, target_region: "Region") -> None:
        if self.get_area == 0:
            raise ValueError(f"Region {self} is empty, cannot merge into other")
        for pl in self.plots:
            pl.region = target_region
            target_region.plots.append(pl)

    @property
    def get_area(self) -> int:
        return len(self.plots)
    
    def count_long_fences(self, plots) -> int:
        count = 0
        for plt in self.plots:
            edges = plt.corners(plots)         #special property where these 2 match
            count += edges
        return count






if __name__ == "__main__":
    main(sys.argv)


