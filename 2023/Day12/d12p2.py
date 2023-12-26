from functools import lru_cache

import sys
from pathlib import Path

# Run with test data    -> python3 -m d#p#
# Run with puzzle data  -> python3 -m d#p# X (any argument)

def main(argv: list[str]):
    # Prep Code
    lines: list[str]

    if len(argv) == 1:
        test_data = """\
???.### 1,1,3
.??..??...?##. 1,1,3
?#?#?#?#?#?#?#? 1,3,1,6
????.#...#... 4,1,1
????.######..#####. 1,6,5
?###???????? 3,2,1"""

        lines = test_data.splitlines()
    else:
        data_file = Path.cwd() / "puzzle_data.txt"
        with open(data_file, "r") as f:
            lines = f.readlines()

    for i, line in enumerate(lines):
        lines[i] = line.strip()

    # Puzzle code
    # ----------------------------------------------------------------

    # Split data
    all_runs: list[list[int]] = []

    for i, line in enumerate(lines):
        lines[i] = '?'.join([line.split()[0]]*5).strip('.')
        runs = (line.split()[1].split(',')) * 5
        runs = tuple(int(num) for num in runs)
        all_runs.append(runs)
 
    # for i, line in enumerate(lines):
    #     lines[i] = line.split()[0]
    #     runs = line.split()[1].split(',')
    #     runs = tuple(int(num) for num in runs)
    #     all_runs.append(runs)

    # # Print all 
    # for i, line in enumerate(lines):
    #     print('-', line, all_runs[i])

    sum = 0
    for line, runs in zip(lines, all_runs):
        result = ways(line, runs, False, 0)
        sum += result
        print(line, runs, result, sum)

@lru_cache
def ways(line: str, runs: tuple[int], inside_run: bool, depth: int) -> int:
    #print('  '*depth, line, runs)
    depth += 1
    if len(line) < (sum(runs) + len(runs) - 1):
        return 0
    if len(line) == (sum(runs) + len(runs) - 1):
        return check_fit(line, runs)
    if len(runs) == 0 and (line.count('#') == 0):
        #print("+1")
        return 1
    if line == '':
        return 1 if sum(runs) == 0 else 0

    if line[0] == '.':
        if len(runs) == 0:
            pass
        elif runs[0] == 0:
            runs = runs[1:]
        elif runs[0] > 0 and inside_run == True:
            return 0
        return ways(line[1:], runs, False, depth)

    if line[0] == '#':
        if len(runs) == 0:
            return 0
        if runs[0] == 0:
            return 0
        if sum(runs) == 0:
            return 0
        runs = ((runs[0]-1),) + runs[1:]
        return ways(line[1:], runs, True, depth)

    if line[0] == '?':
        return ways('.'+line[1:], runs, inside_run, depth) + ways('#'+line[1:], runs, inside_run, depth)




def check_fit(line: str, runs: tuple[int]) -> int:
    runs_as_string = []
    fits = 1

    for run in runs:
        assert run != 0
        runs_as_string.append('#' * run)
    runs_as_string = '.'.join(runs_as_string)

    for c, r in zip(line, runs_as_string):
        if c == '?':
            continue
        if c != r:
            fits = 0
    #print("Checking final: ", line, '==', runs_as_string, '->', fits)
    return fits


main(sys.argv)



# answer: 25470469710341
