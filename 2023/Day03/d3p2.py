from pathlib import Path

def main():
    # Prep Code
    use_test_data = False
    data = """\
467..114.8
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598.."""
    lines: list[str] = data.splitlines()
    
    if use_test_data != True:
        data_file = Path.cwd() / "data.txt"
        with open(data_file, "r") as f:
            lines: list[str] = f.readlines()

    for i, line in enumerate(lines):
        lines[i] = line.strip()

    # Puzzle code
    line_len = len(lines[0])
    digits = {'0','1','2','3','4','5','6','7','8','9'}
    positions = {(-1,-1), (-1,+0), (-1,+1),
                 (+0,-1), (+0,+0), (+0,+1),
                 (+1,-1), (+1,+0), (+1,+1)}
    sum = 0

    for i, line in enumerate(lines):        
        for j, c in enumerate(line):
            if c != '*':
                continue
            else:
                numbers = []
                numbers += check_arround_gear(positions.copy(), digits, lines, i, j)
                if len(numbers) == 2:
                    sum += numbers[0] * numbers[1]
                
                print(f"gear({i}, {j}) numbers: {numbers}, sum: {sum}")


def check_arround_gear(positions: set[tuple[int]], digits: set[str], lines: list[str], i: int, j: int) -> list[str]:
    numbers = []
    while positions:
        m, n = positions.pop()
        #print(f"{positions} ---> ({m}, {n})")
        if safe_lines(lines, i+m , j+n) not in digits:
            continue
        number = safe_lines(lines, i+m , j+n)
        l = 0
        while True:
            l -= 1
            positions = positions - set([(m, n+l)])
            if safe_lines(lines, i+m , j+n+l) not in digits:
                break
            number = safe_lines(lines, i+m , j+n+l) + number
        r = 0
        while True:
            r += 1
            positions = positions - set([(m, n+r)])
            if safe_lines(lines, i+m , j+n+r) not in digits:
                break
            number = number + safe_lines(lines, i+m , j+n+r)
        numbers.append(int(number))
    return numbers

def safe_lines(lines: list[str], i: int, j: int) -> str:
    if (i < 0) or (j < 0):
        return '.'
    if (i >= len(lines)) or (j >= len(lines[0])):
        return '.'
    return lines[i][j]

main()