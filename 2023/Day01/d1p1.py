import re
from pathlib import Path


data_file = Path.cwd() / "data.txt"
with open(data_file, "r") as f:
    data = f.readlines()

pattern1 = r"^\D*(\d)"
pattern2 = r"^\D*(\d).*(\d)\D*$"

pobj1 = re.compile(pattern1, re.MULTILINE)
pobj2 = re.compile(pattern2, re.MULTILINE)

sum = 0

for i, row in enumerate(data):
    #if i == 10: break
    row = row.strip()
    
    match = pobj2.search(row)
    if match != None:
        n1 = match[1]        
        n2 = match[2]
        sum += int(n1 + n2)
        print(f"{i}: {n1}{n2} -> {sum}")
        continue

    match = pobj1.search(row)
    if match != None:
        n1 = match[1]
        n2 = n1
        sum += int(n1 + n2)
        print(f"{i}: {n1}{n2} -> {sum}")
        continue

    print(f"Error, could not parse {row}")