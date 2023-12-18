from pathlib import Path
from functools import reduce
from operator import mul

def main():
    # Prep Code
    use_test_data = False
    test_data = """\
Time:      71530
Distance:  940200"""
    lines: list[str] = test_data.splitlines()
    
    if use_test_data != True:
        data_file = Path.cwd() / "data2.txt"
        with open(data_file, "r") as f:
            lines: list[str] = f.readlines()

    for i, line in enumerate(lines):
        lines[i] = line.strip()

    # Puzzle code
    times: list[int] = lines[0].split(":")[1].split()
    distances: list[int] = lines[1].split(":")[1].split()

    print(times)
    print(distances)

    ways_to_beat: list[int] = []

    for i, time_distance in enumerate(zip(times, distances)):
        ways_to_beat.append(0)
        time = int(time_distance[0])
        distance = int(time_distance[1])
        
        for t in range(1, time):
            # d = vt
            d = t * (time - t)
            if d > distance:
                ways_to_beat[i] += 1

    print(ways_to_beat)
    print(reduce(mul, ways_to_beat))
    


main()