from pprint import pprint

import sys
from pathlib import Path

# Run with test data    -> python3 -m d#p#
# Run with puzzle data  -> python3 -m d#p# X (any argument)

def main(argv: list[str]):
    # Prep Code
    lines: list[str]

    if len(argv) == 1:
        test_data = """\
2413432311323
3215453535623
3255245654254
3446585845452
4546657867536
1438598798454
4457876987766
3637877979653
4654967986887
4564679986453
1224686865563
2546548887735
4322674655533"""
        lines = test_data.splitlines()
    else:
        data_file = Path.cwd() / "puzzle_data.txt"
        with open(data_file, "r") as f:
            lines = f.readlines()

    for i, line in enumerate(lines):
        lines[i] = line.strip()

    # Puzzle code
    #----------------------------------------------------------------

    end_node = (len(lines)-1, len(lines[0])-1)
    rmax, cmax = end_node[0], end_node[1]

    # Setup lookup dictionary and unvisited set
    node_map = {}
    unvisited: set[tuple[int]] = set()
    visited: set[tuple[int]] = set()

    for i, line in enumerate(lines):
        for j, distance in enumerate(line):
            node_map[(i, j)] = {"distance": int(distance),
                                "distance_from_start": 10**20,
                                "previous_node": None,
                                "previous_direction": None
                                }
            unvisited.add((i, j))

    # Initialize Dijkstra
    current_node = (0, 0)
    node_map[(0, 0)]["distance_from_start"] = 0
    neighbour: tuple[int]
    i = 0

    # Start Dijkstra
    while unvisited:
        # print(i)
        # i += 1
        neighbours: list[neighbour] = []
        neighbours = get_neighbours(neighbours, node_map, current_node, visited, rmax, cmax)
        if neighbours:    
            for neighbour in neighbours:
                distance_to_start = (node_map[neighbour]["distance"]
                                + node_map[current_node]["distance_from_start"])
                if distance_to_start < node_map[neighbour]["distance_from_start"]:
                    node_map[neighbour]["distance_from_start"] = distance_to_start
                    node_map[neighbour]["previous_node"] = current_node
                    node_map[neighbour]["previous_direction"] = get_direction(current_node, neighbour)
        unvisited.remove(current_node)
        visited.add(current_node)
        current_node = find_closest(node_map, unvisited)
        # print(len(unvisited))

    # pprint(node_map)
    # print('')
    # print(current_node)
    # print('')
    # pprint(visited)
    # print('')
    # pprint(unvisited)

    pprint(shortest_path(node_map, end_node))
    print(f"Shortest: {node_map[end_node]['distance_from_start']}")


    
def get_neighbours(
        neighbours: list[tuple[int]],
        node_map: dict,
        current_node: tuple[int],
        visited: set[tuple[int]],
        rmax: int,
        cmax: int
        ) -> list[tuple[int]]:
    
    possible_directions = {(-1, 0), (0, 1), (1, 0), (0, -1)}

    last_node = node_map[current_node]["previous_node"]
    if last_node is not None:
        second_last_node = node_map[last_node]["previous_node"]
        if second_last_node is not None:
            third_last_node = node_map[second_last_node]["previous_node"]
            if third_last_node is not None:
                if last_node[0] == second_last_node[0] + 1 == third_last_node[0] + 2:
                    possible_directions -= {(1, 0)}
                if last_node[0] + 2 == second_last_node[0] + 1 == third_last_node[0]:
                    possible_directions -= {(-1, 0)}
                if last_node[1] == second_last_node[1] + 1 == third_last_node[1] + 2:
                    possible_directions -= {(0, 1)}
                if last_node[1] + 2 == second_last_node[1] + 1 == third_last_node[1]:
                    possible_directions -= {(0, 1)}

    for r, c in possible_directions:
        if (current_node[0]+r) < 0 or (current_node[0]+r) > rmax:
            continue
        if (current_node[1]+c) < 0 or (current_node[1]+c) > cmax:
            continue
        if (current_node[0]+r, current_node[1]+c) in visited:
            continue
        neighbours.append((current_node[0]+r, current_node[1]+c))
    return neighbours

def find_closest(node_map: dict, unvisited: set[tuple[int]]) -> tuple[int]:
    """Return node with smalleset distance to start"""
    min_distance = 10**20
    min_node = None
    for node in unvisited:
        if node_map[node]["distance_from_start"] < min_distance:
            min_distance = node_map[node]["distance_from_start"]
            min_node = node
    return min_node

def shortest_path(node_map: dict, end_node: tuple[int]) -> list[tuple[int]]:
    path = []
    path.append(end_node)
    current_node = end_node
    while current_node != (0, 0):
        facing = node_map[current_node]["previous_direction"]
        current_node = node_map[current_node]["previous_node"]
        path.append(current_node + (facing,))
    path.reverse()
    return path

def get_direction(current_node: tuple[int], neighbour: tuple[int]) -> str:
    if neighbour[0] > current_node[0]:
        return 's'
    if neighbour[0] < current_node[0]:
        return 'n'
    if neighbour[1] > current_node[1]:
        return 'e'
    if neighbour[1] < current_node[1]:
        return 'w'
    raise ValueError("Current node and Neighbour have the same position")



main(sys.argv)


