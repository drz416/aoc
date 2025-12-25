# /// script
# requires-python = ">=3.14"
# dependencies = [
#     "matplotlib",
#     "networkx",
#     "scipy",
# ]
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

    devices: dict[str, list[str]] = {}
    for row in rows:
        name, outputs = row.split(": ")
        devices[name] = outputs.split()
    
    import networkx as nx
    import matplotlib.pyplot as plt

    # Sample data as a dictionary
    graph_data = devices

    # Create a directed graph
    G = nx.DiGraph()

    # Add nodes and directed edges from the dictionary
    for node, neighbors in graph_data.items():
        for neighbor in neighbors:
            G.add_edge(node, neighbor)

    # Draw the directed graph
    pos = nx.spring_layout(G)
    nx.draw(G, pos, with_labels=True, node_color='lightblue', node_size=50, font_size=8, font_weight=None, arrows=True, arrowstyle='->', arrowsize=20)
    plt.title("Directed Network Graph from Dictionary")
    plt.show()

    return

    

#----------------------------------------------------------------



# Data load and caling main()
#----------------------------------------------------------------
if __name__ == "__main__":
    # Prep Data
    rows: list[str]

    if len(sys.argv) == 1:
        # Paste test example data here
        test_data = """\
svr: aaa bbb
aaa: fft
fft: ccc
bbb: tty
tty: ccc
ccc: ddd eee
ddd: hub
hub: fff
eee: dac
dac: fff
fff: ggg hhh
ggg: out
hhh: out"""
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


