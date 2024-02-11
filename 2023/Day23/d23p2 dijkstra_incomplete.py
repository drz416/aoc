import sys
import re
from collections import deque, Counter, defaultdict
from pathlib import Path
from pprint import pprint

# Run with test data    -> python3 -m d#p#
# Run with puzzle data  -> python3 -m d#p# X (any argument)

def main(argv: list[str]):
    # Prep Code
    lines: list[str]

    if len(argv) == 1:
        test_data = """\
#.#####################
#.......#########...###
#######.#########.#.###
###.....#.....###.#.###
###.#####.#.#.###.#.###
###.....#.#.#.....#...#
###.###.#.#.#########.#
###...#.#.#.......#...#
#####.#.#.#######.#.###
#.....#.#.#.......#...#
#.#####.#.#.#########.#
#.#...#...#...###.....#
#.#.#.#######.###.###.#
#...#...#.......#.###.#
#####.#.#.###.#.#.###.#
#.....#...#...#.#.#...#
#.#########.###.#.#.###
#...###...#...#...#.###
###.###.#.###.#####.###
#...#...#.#.....#...###
#.###.###.#.###.#.#.###
#.....###...###...#...#
#####################.#"""
        lines = test_data.splitlines()
    else:
        data_file = Path.cwd() / "puzzle_data2.txt"
        with open(data_file, "r") as f:
            lines = f.readlines()

    for i, line in enumerate(lines):
        lines[i] = line.strip()

    # Puzzle code
    #----------------------------------------------------------------

    # --> step 1 greate the graph (dictinoary of dictionaries)
    # --> step 2 dijkstra's algorithm
        

    # Initialize
    mp = lines
    start = (0, mp[0].index('.'))
    trail_start = (start[0] + 1, start[1])
    end = (len(mp) - 1, mp[-1].index('.'))
    Trail.mp: list[str] = mp
    Trail.end: tuple[int] = end

    # Setup data structures
    trail_q: deque[Trail] = deque()
    trail_q.append(Trail(trail_start, start, 1))
    graph = defaultdict(dict)

    # Scan paths to create graph
    while len(trail_q) > 0:
        trail = trail_q.popleft()
        if trail.move_to_node():
            # reached end, do nothing
            pass
        else:
            # reached node
            if trail.position not in graph:
                # unvisited location, start new trails
                for direction in trail.scan_directions():
                    new_position = trail.position[0]+direction[0], trail.position[1]+direction[1]
                    trail_q.append(Trail(new_position, trail.position, 1))
        # save graph edge
        graph[trail.start_node][trail.position] = trail.steps
        graph[trail.position][trail.start_node] = trail.steps

    # Graph is complete
    pprint(graph)
    print('')

    # Initialize Dijkstra
    visited: set[tuple[int]] = set()
    unvisited: set[tuple[int]] = set(graph.keys())

    distance_map = {}
    for node in unvisited:
        distance_map[node] = {
            "dist_from_start": None,
            "prev_node": None
        }
    distance_map[start]["dist_from_start"] = 0
    distance_map[start]["prev_node"] = None

    # Run Dijkstra
    while unvisited:
        current_node = node_w_shortest_distance(distance_map, unvisited)
        print(current_node)
        neighbours = graph[current_node]
        for neighbour, distance in neighbours.items():
            if neighbour in visited:
                continue
            curr_distance_to_start = -1 if distance_map[neighbour]["dist_from_start"] is None else distance_map[neighbour]["dist_from_start"]
            new_dist_to_start = (distance_map[current_node]["dist_from_start"]
                                  + distance)
            if new_dist_to_start > curr_distance_to_start:
                distance_map[neighbour]["dist_from_start"] = new_dist_to_start
                distance_map[neighbour]["prev_node"] = current_node
        # Label node as visited
        visited.add(current_node)
        unvisited.remove(current_node)


    pprint(distance_map)



class Trail():
    mp: list[str]
    end: tuple[int]
    directions = {
        0: (1, 0),
        1: (0, 1),
        2: (0, -1),
        3: (-1, 0)
    }

    def __init__(
            self,
            position: tuple[int],
            prev_position: tuple[int],
            steps: int
            ) -> None:
        self.position = position
        self.prev_position = prev_position
        self.start_node = prev_position
        self.steps = steps
    
    def scan_directions(self) -> list[tuple[int]]:
        new_directions = []
        for dx, dy in self.directions.values():
            if self.prev_position == (self.position[0] + dx, self.position[1] + dy):
                # coming from that direction
                continue
            if self.mp[self.position[0] + dx][self.position[1] + dy] == '#':
                # can't go into walls
                continue
            new_directions.append((dx, dy))
        return new_directions
    
    def move_to_node(self) -> bool:
        """Traverse trail until finding a node, or reaching the end. Return True if at end"""
        while True:
            if self.position == self.end:
                return True
            directions = self.scan_directions()
            if len(directions) == 0:
                raise ValueError(f"No directions found at {self.position}")
            if len(directions) == 1:
                # not at node, keep moving
                self.prev_position = self.position
                self.position = (self.position[0] + directions[0][0], self.position[1] + directions[0][1])
                self.steps += 1
                continue
            else:
                # reached a node, stop moving, return False as not at end
                return False        


def node_w_longest_distance(distance_map: dict, unvisited: set) -> tuple[int]:
    max_distance_node = None
    max_distance = -10
    for node in unvisited:
        if distance_map[node]["dist_from_start"] >= max_distance:
            max_distance_node = node
            max_distance = distance_map[node]["dist_from_start"]
    return max_distance_node

def node_w_shortest_distance(distance_map: dict, unvisited: set) -> tuple[int]:
    min_distance_node = None
    min_distance = 10**10
    for node in unvisited:
        if distance_map[node]["dist_from_start"] is None:
            continue
        if distance_map[node]["dist_from_start"] <= min_distance:
            min_distance_node = node
            min_distance = distance_map[node]["dist_from_start"]
    return min_distance_node

if __name__ == "__main__":
    main(sys.argv)


