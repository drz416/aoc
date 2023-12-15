import re
from pathlib import Path

def main():
    # Prep Code
    use_test_data = False
    data = """\
Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53
Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19
Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1
Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83
Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36
Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11"""
    lines: list[str] = data.splitlines()
    
    if use_test_data != True:
        data_file = Path.cwd() / "data.txt"
        with open(data_file, "r") as f:
            lines: list[str] = f.readlines()

    for i, line in enumerate(lines):
        lines[i] = line.strip()

    # Puzzle code
    if use_test_data:
        cards = [1]*6
        pattern = r"Card\s+\d+:\s(.\d)\s(.\d)\s(.\d)\s(.\d)\s(.\d)\s.\s(.\d)\s(.\d)\s(.\d)\s(.\d)\s(.\d)\s(.\d)\s(.\d)\s(.\d)"
    else:
        pattern = r"Card\s+\d+:\s(.\d)\s(.\d)\s(.\d)\s(.\d)\s(.\d)\s(.\d)\s(.\d)\s(.\d)\s(.\d)\s(.\d)\s.\s(.\d)\s(.\d)\s(.\d)\s(.\d)\s(.\d)\s(.\d)\s(.\d)\s(.\d)\s(.\d)\s(.\d)\s(.\d)\s(.\d)\s(.\d)\s(.\d)\s(.\d)\s(.\d)\s(.\d)\s(.\d)\s(.\d)\s(.\d)\s(.\d)\s(.\d)\s(.\d)\s(.\d)\s(.\d)"
        cards = [1]*196
    p_obj = re.compile(pattern)

    for i, card in enumerate(lines):
        numbers: list[tuple[str]] = p_obj.findall(card)
        if use_test_data:
            winning = numbers[0][0:5]
            yours = numbers[0][5:]
        else:
            winning = numbers[0][0:10]
            yours = numbers[0][10:]
        matches = 0
        for your in yours:
            if your in winning:
                matches += 1
        if matches == 0:
            continue
        else:
            for j in range(matches):
                if (i + 1) + (j + 1) > len(lines):
                    break
                else:
                    cards[i+1+j] += cards[i]
        print(matches, cards, sum(cards))

main()