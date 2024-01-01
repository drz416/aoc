from collections import deque
import subprocess
import time

import sys
from pathlib import Path

# Run with test data    -> python3 -m d#p#
# Run with puzzle data  -> python3 -m d#p# X (any argument)

def main(argv: list[str]):
    # Prep Code
    lines: list[str]

    if len(argv) == 1:
        test_data = r""".|...\....
|.-.\.....
.....|-...
........|.
..........
.........\
..../.\\..
.-.-/..|..
.|....-|.\
..//.|...."""
        lines = test_data.splitlines()
    else:
        data_file = Path.cwd() / "puzzle_data.txt"
        with open(data_file, "r") as f:
            lines = f.readlines()

    for i, line in enumerate(lines):
        lines[i] = line.strip()

    # Puzzle code
    #----------------------------------------------------------------

    grid = lines
    beams: deque[Beam] = deque()

    # Construct all possible entry points
    entries = {}
    for i in range(len(grid)):              
        entries[((i, -1), 'e')] = 0              # Left edge entries
        entries[((i, len(grid[0])), 'w')] = 0    # Right edge entries
    for j in range(len(grid[0])):
        entries[((-1, j), 's')] = 0              # Top edge entries
        entries[((len(grid), j), 'n')] = 0       # Bottom edge entries

    # Test each one
    for entry in entries:

        energized_positions = {}
        position_directions_log = {}
        beams.clear()
        beams.append(Beam(grid, beams, entry[0], entry[1]))

        i = 0
        while True:
            try:
                beam = beams.popleft()
            except IndexError:
                # print("No more beams")
                break
            out_of_bounds = beam.move()
            if out_of_bounds:
                continue
            energized_positions[beam.get_position] = 1
            position_direction = beam.get_position + (beam.facing,)
            if position_direction in position_directions_log:
                continue
            position_directions_log[position_direction] = 1

            beam.process_position()

            # Draw energized positions
            # subprocess.run('clear')
            # draw_array = []
            # for line in lines:
            #     draw_array.append(list(line))
            # for position in position_directions_log.keys():
            #     draw_array[position[0]][position[1]] = '#'
            # for row in draw_array:
            #     print(''.join(row))
            # time.sleep(0.1)

            beams.append(beam)
            i += 1
        entries[entry] = len(energized_positions)
        # print(f"{i=} Entry={entry} Energized={len(energized_positions)}")
    
    print(f"Finished. Max energizations of {max(entries.values())}")


class Beam():
    def __init__(
            self,
            grid: list[str],
            beams: deque["Beam"],
            position: tuple[int],
            facing: str
            ) -> None:
        """\
position: row, column
facing: 'n', 'e', 's', 'w'"""
        self.grid = grid
        self.beams = beams
        self.position = list(position)
        self.facing = facing
        self.backslash_mirror = {
            'n': 'w',
            'e': 's',
            's': 'e',
            'w': 'n'
        }
        self.forwardslash_mirror = {
            'n': 'e',
            'e': 'n',
            's': 'w',
            'w': 's' 
        }

    @property
    def get_position(self) -> tuple[int]:
        return tuple(self.position)
    
    def move(self) -> bool:
        """Returns True if it moves off of the grid"""
        if self.facing == 'n':
            self.position[0] -= 1
            if self._out_of_boundary:
                return True
        elif self.facing == 'e':
            self.position[1] += 1
            if self._out_of_boundary:
                return True
        elif self.facing == 's':
            self.position[0] += 1
            if self._out_of_boundary:
                return True
        else:
            self.position[1] -= 1
            if self._out_of_boundary:
                return True
        return False

    @property
    def _out_of_boundary(self) -> bool:
        if self.position[0] < 0 or self.position[0] >= len(self.grid):
            return True
        if self.position[1] < 0 or self.position[1] >= len(self.grid[0]):
            return True
        return False
    
    def process_position(self) -> bool:
        if self.grid[self.position[0]][self.position[1]] == '.':
            return
        elif self.grid[self.position[0]][self.position[1]] == '-':
            if self.facing in {'e', 'w'}:
                return
            else:
                self.facing = 'e'
                self.beams.append(self.__class__(
                    self.grid,
                    self.beams,
                    self.get_position,
                    'w'
                ))
                return
        elif self.grid[self.position[0]][self.position[1]] == '|':
            if self.facing in {'n', 's'}:
                return
            else:
                self.facing = 'n'
                self.beams.append(self.__class__(
                    self.grid,
                    self.beams,
                    self.get_position,
                    's'
                ))
                return
        elif self.grid[self.position[0]][self.position[1]] == '\\':
            self.facing = self.backslash_mirror[self.facing]
        elif self.grid[self.position[0]][self.position[1]] == '/':
            self.facing = self.forwardslash_mirror[self.facing]
        else:
            raise TypeError(f"Unrecognized symbol: {self.grid[self.position[0]][self.position[1]]}")


main(sys.argv)


