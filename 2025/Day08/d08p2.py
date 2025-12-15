# /// script
# requires-python = ">=3.14"
# dependencies = []
# ///
#
# to add dependencies -> uv add --script <file> <module>
# to remove dependencies -> uv remove --script <file> <module>
# to run with test data    -> uv run --script d#p#
# to run with puzzle data  -> uv run --script d#p# X (any argument)



# Template Imports
#----------------------------------------------------------------
import sys
import re
from pathlib import Path
from pprint import pprint
from time import time, time_ns
from collections import deque, Counter, defaultdict
from functools import partial, lru_cache
from itertools import product, combinations
#----------------------------------------------------------------


# Solution Code
#----------------------------------------------------------------

def main(rows: list[str]):

    boxes: list[tuple[int]] = []
    for row in rows:
        x, y, z = row.split(",")
        boxes.append((int(x), int(y), int(z)))

    # Map all distances
    distances: list[tuple] = []
    for box1, box2 in combinations(boxes, 2):
        distance = ((box1[0]-box2[0])**2
            + (box1[1]-box2[1])**2
            + (box1[2]-box2[2])**2
        )**(0.5)
        distances.append((distance, box1, box2))

    # Arrange the distances from shortest to longest
    distances.sort()

    # Link up circuits
    box_locations: dict[tuple[int], int] = {}
    circuits: dict[int, set[tuple[int]]] = {}
    circuit_id = 0

    for _, box1, box2 in distances:
        if (box1 not in box_locations) and (box2 not in box_locations):
            # Both boxes not in a circuit, create a new circuit
            circuit_id += 1
            box_locations[box1] = circuit_id
            box_locations[box2] = circuit_id
            circuits[circuit_id] = {box1, box2}
        elif (box1 in box_locations) and (box2 not in box_locations):
            # Box1 is part of circuit but not Box2, add Box2 to existing circuit
            this_circuit = box_locations[box1]
            box_locations[box2] = this_circuit
            circuits[this_circuit].add(box2)
        elif (box1 not in box_locations) and (box2 in box_locations):
            # Box2 is part of circuit but not Box1, add Box1 to existing circuit
            this_circuit = box_locations[box2]
            box_locations[box1] = this_circuit
            circuits[this_circuit].add(box1)
        else:
            # (box1 in box_locations) and (box2 in box_locations):
            # Both boxes are in a circuit...
            if box_locations[box1] == box_locations[box2]:
                # ... and they're the same, ignore
                pass
            else:
                # ... they are different, merge them
                base_circuit = box_locations[box1]
                other_circuit = box_locations[box2]
                for box in circuits[other_circuit]:
                    box_locations[box] = base_circuit
                    circuits[base_circuit].add(box)
                del(circuits[other_circuit])
                
        if len(circuits) == 1:
            # Check for final link
            if len(circuits[box_locations[box1]]) == len(boxes):
                final_box1 = box1
                final_box2 = box2
                break

    # Calc answer
    print(final_box1, final_box2)
    ans = final_box1[0] * final_box2[0]


    print(f"\nAns: {ans}")

    # ans: 100011612




#----------------------------------------------------------------



# Data load and caling main()
#----------------------------------------------------------------
if __name__ == "__main__":
    # Prep Data
    rows: list[str]

    if len(sys.argv) == 1:
        # Paste test example data here
        test_data = """\
162,817,812
57,618,57
906,360,560
592,479,940
352,342,300
466,668,158
542,29,236
431,825,988
739,650,466
52,470,668
216,146,977
819,987,18
117,168,530
805,96,715
346,949,466
970,615,88
941,993,340
862,61,35
984,92,344
425,690,689"""
        rows = test_data.splitlines()
    else:
        data_file = Path.cwd() / "puzzle_data.txt"
        with open(data_file, "r") as f:
            rows = f.readlines()

    for i, line in enumerate(rows):
        rows[i] = line.strip()
    
    start_time = time()
    main(rows)
    print("")
    print(f"Time in main(): {time() - start_time:.06f}s")
#----------------------------------------------------------------


