from pathlib import Path
from pprint import pprint

symbols = {}

def main():
    data_file = Path.cwd() / "data.txt"
    with open(data_file, "r") as f:
        data = f.read()
    
    for s in data:
        symbols[s] = symbols.get(s, 0) + 1

    pprint(symbols)

main()
