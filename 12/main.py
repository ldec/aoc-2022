from copy import deepcopy
from dataclasses import dataclass
from queue import Queue
from typing import List, Tuple, Optional
import networkx as nx
from networkx import dfs_predecessors, shortest_path

from utils.out import print
from utils.readers import OneColumnFileReader
import numpy as np
import matplotlib.pyplot as plt

class Coord:
    pass

@dataclass(unsafe_hash=True)
class Coord:
    x: int
    y: int
    shape: Tuple[int, int]
    elevation: int
    is_start: bool
    is_end: bool
    parent: Optional[Tuple[int, int]]

    def __str__(self):
        type = ""
        if self.is_start:
            type = "S"
        if self.is_end:
            type = "E"
        return f"{type}{self.elevation}-{self.x},{self.y}"

    def same_position(self, to_compare:Coord):
        return to_compare.x == self.x and to_compare.y == self.y

    def _check_next_step(self, map, next_x, next_y):
        next_elevation = map[next_y][next_x].elevation
        if self.elevation == next_elevation or self.elevation == next_elevation - 1:
            return map[next_y][next_x]
        return None

    def north(self, map) -> Optional[Coord]:
        if self.y == 0:
            return None
        return self._check_next_step(map, self.x, self.y - 1)

    def south(self, map) -> Optional[Coord]:
        if self.y == self.shape[0] - 1:
            return None
        return self._check_next_step(map, self.x, self.y + 1)

    def east(self, map) -> Optional[Coord]:
        if self.x == self.shape[1] - 1:
            return None
        return self._check_next_step(map, self.x + 1, self.y)

    def west(self, map) -> Optional[Coord]:
        if self.x == 0:
            return None
        return self._check_next_step(map, self.x - 1, self.y)


class MapReader(OneColumnFileReader):
    """
    Implementation of a map reader

    E.g.

    Sabqponm
    abcryxxl
    accszExk
    acctuvwj
    abdefghi
    """

    def read(self, *args):
        data = super(MapReader, self).read()
        shape = (len(data), len(data[0]))

        start = None
        end = None
        array = []
        for y, raw_raw in enumerate(data):
            row = []
            raw_row = list(raw_raw)
            for x, item in enumerate(raw_row):
                is_start = False
                is_end = False
                if item == "S":
                    is_start = True
                    item = "a"
                if item == "E":
                    is_end = True
                    item = "z"
                coord = Coord(
                    x=x,
                    y=y,
                    shape=shape,
                    elevation=ord(item) - 96,
                    is_start=is_start,
                    is_end=is_end,
                    parent=None
                )
                if coord.is_start:
                    start = coord
                if coord.is_end:
                    end = coord
                row.append(coord)

            array.append(row)

        return np.array(array), start, end

def add_to_graph(graph, current_node: Coord, next:Coord, direction:str):
    graph.add_node(next)
    graph.add_edge(current_node, next, direction=direction)
    return next

def add_parent(current: Coord, next:Coord):
    next = deepcopy(next)
    next.parent = (current.x, current.y)
    return next

def already_in_node(graph, start: Coord, current: Coord, next:Coord):
    # nodes = list(dfs_predecessors(graph, current))
    nodes = shortest_path(graph, start, current)
    for node in nodes:
        if node.same_position(next):
            return True

    return False

def explore(map, start, graph, current_node):
    nodes = [
        current_node.north(map),
        current_node.south(map),
        current_node.east(map),
        current_node.west(map),
    ]
    directions = ["N", "S", "E", "W"]

    # if current_node.x == 1 and current_node.y == 3:
    #     i = 1

    for next, direction in zip(nodes, directions):
        if next is not None:
            if not already_in_node(graph, start, current_node, next):
                next = add_parent(current_node, next)
                add_to_graph(graph, current_node, next, direction)
                if next.is_end:
                    shortest = shortest_path(graph, start, next)
                    print(f"Found path {len(shortest) - 1}")
                    return
                explore(map, start, graph, next)


def main():
    test_reader = MapReader("input-test.txt")
    test_data = test_reader.read()

    reader = MapReader("input.txt")
    prod_data = reader.read()

    data_sources = (
        ("Test data", test_data),
        ("Prod data", prod_data),
    )

    for data_source_name, data_source in data_sources:
        graph = nx.Graph()
        start = deepcopy(data_source[1])
        start.parent = (0,0)
        graph.add_node(start)
        explore(data_source[0], start, graph, start)


        pos = nx.spring_layout(graph)
        plt.figure(figsize=(10, 10))
        nx.draw(graph, with_labels=True, node_color='skyblue', edge_cmap=plt.cm.Blues, pos=pos)
        edge_labels = nx.get_edge_attributes(graph,'direction')  # key is edge, pls check for your case
        nx.draw_networkx_edge_labels(graph, pos, edge_labels=edge_labels, font_color='red')
        plt.show()


if __name__ == "__main__":
    main()
