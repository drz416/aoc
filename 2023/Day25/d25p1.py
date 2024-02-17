import sys
import re
from collections import deque, Counter
from pathlib import Path
from pprint import pprint

# Run with test data    -> python3 -m d#p#
# Run with puzzle data  -> python3 -m d#p# X (any argument)

def main(argv: list[str]):
    # Prep Code
    lines: list[str]

    if len(argv) == 1:
        test_data = """\
jqt: rhn xhk nvd
rsh: frs pzl lsr
xhk: hfx
cmg: qnr nvd lhk bvb
rhn: xhk bvb hfx
bvb: xhk hfx
pzl: lsr hfx nvd
qnr: nvd
ntq: jqt hfx bvb xhk
nvd: lhk
lsr: lhk
rzs: qnr cmg lsr rsh
frs: qnr lhk lsr"""
        lines = test_data.splitlines()
    else:
        data_file = Path.cwd() / "puzzle_data.txt"
        with open(data_file, "r") as f:
            lines = f.readlines()

    for i, line in enumerate(lines):
        lines[i] = line.strip()

    # Puzzle code
    #----------------------------------------------------------------

    # Build graph, set of nodes, and set of edges
    from collections import defaultdict
    from copy import deepcopy

    graph = defaultdict(set)

    for row in lines:
        row_split = row.split(': ')
        base_node, nodes = (row_split[0], row_split[1].split(' '))
        for node in nodes:
            graph[base_node].add(node)
            graph[node].add(base_node)

    all_nodes = set(graph.keys())

    all_edges: set[tuple[str]] = set()
    for base_node, neighbours in graph.items():
        for node in neighbours:
            if (base_node, node) in all_edges or (node, base_node) in all_edges:
                continue
            all_edges.add((base_node, node))
    # pprint(graph)
    # pprint(all_nodes)
    # pprint(all_edges)

    # Iterate through all 3 edge deletion combinations
    working_graph = deepcopy(graph)
    edges_to_remove = gen_indexes(all_edges)                # generator
    i = 0
    for edges in edges_to_remove:
        # remove 3 edges
        for node1, node2 in edges:
            remove_edge(working_graph, node1, node2)

        # traverse graph and test if split
        all, traversed = traverse_graph(all_nodes, working_graph)
        if i % 5000 == 0:
            print(f"{i:6}: {all=}, {traversed=}")
        if all == False:
            print(f"{i:6}: {all=}, {traversed=}")
            break
        
        # if not split, restore the 3 edges
        for node1, node2 in edges:
            restore_edge(working_graph, node1, node2)
        i += 1

    print(f"ans = {traversed * (len(all_nodes) - traversed)}")
    
def traverse_graph(all_nodes: set, graph_to_traverse: dict[set]) -> tuple[bool, int]:
    """Traverse all nodes, return tuple (bool, int)
bool:   True if it traversed all nodes, False otherwise
int:    Number of nodes traversed"""
    START_NODE = 'rhn'
    visited = set()
    traverse_q = deque()
    traverse_q.append(START_NODE)
    
    while len(traverse_q) > 0:
        node = traverse_q.popleft()
        visited.add(node)
        for neighbour in graph_to_traverse[node]:
            if neighbour in visited:
                continue
            traverse_q.append(neighbour)

    return (True, len(visited)) if visited == all_nodes else (False, len(visited))
       
def remove_edge(graph: dict[set], node1: str, node2: str) -> None:
    graph[node1].remove(node2)
    graph[node2].remove(node1)

def restore_edge(graph: dict[set], node1: str, node2: str) -> None:
    graph[node1].add(node2)
    graph[node2].add(node1)

def gen_indexes(all_edges: set) -> tuple[int]:
    for i in all_edges:
        for j in all_edges:
            for k in all_edges:
                if i == j or i == k or j == k:
                    continue
                yield (i, j, k)




if __name__ == "__main__":
    main(sys.argv)



# Example broken at
# hfx/pzl
# bvb/cmg
# nvd/jqt
    
    # print(traverse_all(set(graph.keys()), graph))
    # remove_edge(graph, 'hfx', 'pzl')
    # remove_edge(graph, 'bvb', 'cmg')
    # remove_edge(graph, 'nvd', 'jqt')
    # print(traverse_all(set(graph.keys()), graph))