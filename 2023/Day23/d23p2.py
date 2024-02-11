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

    # Setup brute for search with PathClass objects
    PathClass.graph = graph
    PathClass.end = end
    start_path = PathClass([start])
    paths_q: deque[PathClass] = deque()
    paths_q.append(start_path)

    longest_distance = 0
    longest_path = None

    # Brute force calculate distance of longest paths
    i = 0
    while len(paths_q) > 0:
        if i % 1_000_000 == 0:
            print(f"i: {i}, Queue: {len(paths_q)}, Longest: {longest_distance}")
        i += 1
        p = paths_q.pop()               # LIFO -> always longest distance instance
        # print(p.node_path, p.distance)
        if p.at_end():
            if p.distance > longest_distance:
                longest_distance = p.distance
                longest_path = p
            continue
        
        new_paths = []
        for new_node, distance in graph[p.curr_node].items():
            if p.visited(new_node):
                continue
            new_p = PathClass(p.node_path)
            new_p.add_node(new_node)
            new_paths.append(new_p)
        
        new_paths.sort(key=lambda x: x.distance)
        for p in new_paths:
            paths_q.append(p)

    print("Longest =",longest_distance)
    print(longest_path.node_path)

    # ans: 6378



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

class PathClass():
    graph: defaultdict[dict]
    end: tuple[int]

    def __init__(self, node_path: list[tuple]) -> None:
        self.node_path = node_path.copy()
        self.distance = self.calc_distance()

    def calc_distance(self) -> int:
        distance = 0
        if len(self.node_path) == 1:
            return distance
        for curr, next in zip(self.node_path[0:-1], self.node_path[1:]):
            distance += self.graph[curr][next]
        return distance

    def add_node(self, node: tuple[int]) -> None:
        curr = self.node_path[-1]
        self.node_path.append(node)
        self.distance += self.graph[curr][node]

    def visited(self, node) -> bool:
        return node in self.node_path
    
    def at_end(self) -> bool:
        return True if self.node_path[-1] == self.end else False
    
    @property
    def curr_node(self) -> tuple[int]:
        return self.node_path[-1]
        

if __name__ == "__main__":
    main(sys.argv)


