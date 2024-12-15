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
2333133121414131402"""
        lines = test_data.splitlines()
    else:
        data_file = Path.cwd() / "puzzle_data.txt"
        with open(data_file, "r") as f:
            lines = f.readlines()

    for i, line in enumerate(lines):
        lines[i] = line.strip()

    # Puzzle code
    #----------------------------------------------------------------

    disk_map = lines[0]
    disk: list[int] = []

    file = True
    id = 0
    for c in disk_map:
        if file:
            disk.extend([id] * int(c))
            id += 1
            file = False
        elif (file == False) and (c == "0"):
            # no space between files, do nothing
            file = True
        else:
            disk.extend([-1] * int(c))      #-1 ID means empty space
            file = True

    # Example disk is
    # 00...111...2...333.44.5555.6666.777.888899
    print(disk)

    file = [-1,0]       # file [ID, length]

    # Scan from back of disk
    for back_seek in range(len(disk)-1, -1, -1):
        # print(f"{back_seek}: {disk[back_seek]=} {file=} --> ", end="")
        if (file[0] == -1) and (disk[back_seek] != -1):
            # from empty space to file start, start recording
            # print("Empty to File start")
            file[0] = disk[back_seek]
            file[1] = 1
            continue
        if (file[0] == disk[back_seek]) and (disk[back_seek] != -1):
            # within a file, keep incrementing size
            # print("Within a file")
            file[1] += 1
            continue
        if (file[0] == -1) and (disk[back_seek] == -1):
            # within empty space, no action, keep moving forward
            # print("Within empty file")
            continue
        if (file[0] != -1) and ((disk[back_seek] == -1) or (file[0] != disk[back_seek])):
            # came to end of file, check for empty space to move
            # print("End of file -> ", end="")
            empty_block_size_needed = file[1]
            empty_block_size = 0
            for i, c in enumerate(disk):
                if i > back_seek:
                    break
                if c != -1:
                    empty_block_size = 0
                    continue
                empty_block_size += 1
                if empty_block_size == empty_block_size_needed:
                    # Space found, copy to front
                    # print("Space found, copying to front", end="")
                    free_space_start = i - empty_block_size + 1
                    free_space_end = free_space_start + empty_block_size_needed
                    disk[free_space_start: free_space_end] = [file[0]] * empty_block_size_needed

                    # Erase back
                    orig_file_start = back_seek + 1
                    orig_file_end = orig_file_start + empty_block_size_needed
                    disk[orig_file_start: orig_file_end] = [-1] * empty_block_size_needed
                    break
            file[0], file[1] = disk[back_seek], 1
            # print("")

            
    print(disk)

    total = 0
    for i, c in enumerate(disk):
        if c != -1:
            total += i * c


    print(f"Total: {total}")
    # ans: 6304576012713




if __name__ == "__main__":
    main(sys.argv)


