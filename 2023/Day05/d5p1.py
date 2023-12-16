from pprint import pprint
from pathlib import Path

def main():
    # Prep Code
    use_test_data = False
    test_data = """\
seeds: 79 14 55 13

seed-to-soil map:
50 98 2
52 50 48

soil-to-fertilizer map:
0 15 37
37 52 2
39 0 15

fertilizer-to-water map:
49 53 8
0 11 42
42 0 7
57 7 4

water-to-light map:
88 18 7
18 25 70

light-to-temperature map:
45 77 23
81 45 19
68 64 13

temperature-to-humidity map:
0 69 1
1 0 69

humidity-to-location map:
60 56 37
56 93 4"""
    lines: list[str] = test_data.splitlines()
    
    if use_test_data != True:
        data_file = Path.cwd() / "data.txt"
        with open(data_file, "r") as f:
            lines: list[str] = f.readlines()

    for i, line in enumerate(lines):
        lines[i] = line.strip()

    # Puzzle code
    maps: list(list(tuple)) = []
    map_bucket: list(tuple) = []

    
    for i, line in enumerate(lines):
        if i == 0:
            seeds = line.split(": ")[1].split()
            for n, seed in enumerate(seeds):
                seeds[n] = int(seed)
            print(seeds)
            continue
        if line == "":
            continue
        if line == "seed-to-soil map:":
            map_bucket = []
            continue
        if line == "soil-to-fertilizer map:":
            maps.append(map_bucket)
            map_bucket = []
            continue
        if line == "fertilizer-to-water map:":
            maps.append(map_bucket)
            map_bucket = []
            continue
        if line == "water-to-light map:":
            maps.append(map_bucket)
            map_bucket = []
            continue
        if line == "light-to-temperature map:":
            maps.append(map_bucket)
            map_bucket = []
            continue
        if line == "temperature-to-humidity map:":
            maps.append(map_bucket)
            map_bucket = []
            continue
        if line == "humidity-to-location map:":
            maps.append(map_bucket)
            map_bucket = []
            continue
        map = line.split()
        for k, m in enumerate(map):
            map[k] = int(m)
        map_bucket.append(tuple(map))
    maps.append(map_bucket)
    pprint(maps)

    locations = []
    for seed in seeds:
        print(f"seed: {seed}")
        for map_group in maps:
            for map in map_group:
                lower = map[1]
                upper = map[1] + map[2] - 1
                if lower <= seed <= upper:
                    delta = seed - lower
                    seed = map[0] + delta
                    print(seed)
                    break
        print(f"location: {seed}")
        locations.append(seed)
        print(f"min: {min(locations)}")

main()