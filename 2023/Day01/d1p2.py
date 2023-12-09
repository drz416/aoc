import re
from pathlib import Path

def main():
    data_file = Path.cwd() / "data.txt"
    with open(data_file, "r") as f:
        data = f.readlines()

    pattern1 = r"^.*(one|two|three|four|five|six|seven|eight|nine|\d)"
    pattern2 = (r"^.*?(one|two|three|four|five|six|seven|eight|nine|\d)"
        + r".*"
        + r"(one|two|three|four|five|six|seven|eight|nine|\d).*$"
    )

    pobj1 = re.compile(pattern1, re.MULTILINE)
    pobj2 = re.compile(pattern2, re.MULTILINE)

    sum = 0

    for i, row in enumerate(data):
        #if i == 20: break
        row = row.strip()

        match = pobj2.search(row)
        if match != None:
            n1 = match[1]        
            n2 = match[2]
            sum += int(n_to_num(n1) + n_to_num(n2))
            print(f"{i}: {n1}{n2} -> {sum}")
            continue

        match = pobj1.search(row)
        if match != None:
            n1 = match[1]
            n2 = n1
            sum += int(n_to_num(n1) + n_to_num(n2))
            print(f"{i}: {n1}{n2} -> {sum}")
            continue

        print(f"Error, could not parse {row}")

def n_to_num(n: str) -> int:
    if n in ("one", "1"):
        return "1"
    elif n in ("two", "2"):
        return "2"
    elif n in ("three", "3"):
        return "3"
    elif n in ("four", "4"):
        return "4"
    elif n in ("five", "5"):
        return "5"
    elif n in ("six", "6"):
        return "6"
    elif n in ("seven", "7"):
        return "7"
    elif n in ("eight", "8"):
        return "8"
    elif n in ("nine", "9"):
        return "9"
    print(f"Can't parse {n}")
    raise TypeError

main()