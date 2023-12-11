from pathlib import Path

def main():
    # Prep Code
    use_test_data = True
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
    symbols = {'#','$','%','&','*','+','-','/','=','@'}
    digits = {'0','1','2','3','4','5','6','7','8','9'}
    sum = 0

    for i, line in enumerate(lines):        
        j = 0
        while j < line_len:
            in_num = False
            if line[j] not in digits:
                j += 1
                continue
            else:
                in_num = True
                num = line[j]
                adjacent = []
                adjacent.append(check_arround_digit(symbols, lines, i, j))
                while in_num:
                    j += 1
                    if j >= line_len:
                        break
                    if line[j] not in digits:
                        in_num = False
                    else:
                        num += line[j]
                        adjacent.append(check_arround_digit(symbols, lines, i, j))
                if any(adjacent):
                    sum += int(num)
                print(f"Row: {i}, number: {num}, adjacent: {any(adjacent)}, sum: {sum}")


def check_arround_digit(symbols: set, lines: list[str], i: int, j: int) -> bool:
    adjacent = [False, False, False, False, False, False, False, False, False]
    grid = [(i-1,j-1), (i-1,j+0), (i-1,j+1),
            (i+0,j-1), (i+0,j+0), (i+0,j+1),
            (i+1,j-1), (i+1,j+0), (i+1,j+1),
    ]
    for i, coordinates in enumerate(grid):
        adjacent[i] = check_for_symbol(symbols, lines, coordinates[0], coordinates[1])
    return any(adjacent)

def check_for_symbol(symbols: set, lines: list[str], i: int, j: int) -> bool:
    if (i < 0) or (j < 0):
        return False
    if (i >= len(lines)) or (j >= len(lines[0])):
        return False
    return lines[i][j] in symbols

main()