"""
--- Day 12: Hill Climbing Algorithm ---
https://adventofcode.com/2022/day/12
"""

import heapq
import sys
from typing import Callable

from common import BaseSolver

Coord = tuple[int, int]


class Solver(BaseSolver):
    def _prepare(self):
        data = self.data['input']
        height, width = len(data), len(data[0])
        graph, start, end = {}, None, None
        for i in range(height):
            for j in range(width):
                neighbours = [
                    (x, y)
                    for x, y in [(i - 1, j), (i + 1, j), (i, j - 1), (i, j + 1)]
                    if 0 <= x < height and 0 <= y < width]
                elevation = data[i][j]
                if data[i][j] == 'S':
                    start = (i, j)
                    elevation = 'a'
                if data[i][j] == 'E':
                    end = (i, j)
                    elevation = 'z'
                graph[(i, j)] = (elevation, *neighbours)

        self.data['graph'] = graph
        self.data['start'] = start
        self.data['end'] = end

    @staticmethod
    def _check_one_higher(current: str, neighbour: str) -> bool:
        return ord(neighbour) - ord(current) <= 1

    @staticmethod
    def _check_one_lower(current: str, neighbour: str) -> bool:
        return ord(current) - ord(neighbour) <= 1

    def _find_distances(self, start: Coord, check_func: Callable[..., bool]) -> dict[Coord, int]:
        """
        Dijkstra's algorithm for finding the shortest paths from start to any other point.
        """

        graph = self.data['graph']
        distances = {k: 0 if k == start else sys.maxsize for k in graph}
        distances_heap = []
        for k, v in distances.items():
            heapq.heappush(distances_heap, (v, k))
        visited = set()
        while (
                len(visited) < len(graph) and
                any(dist != sys.maxsize for vert, dist in distances.items() if vert not in visited)
        ):
            _, current = heapq.heappop(distances_heap)
            elevation, *neighbours = graph.get(current)
            for n in neighbours:
                n_elevation, *_ = graph.get(n)
                if (n in visited) or not check_func(elevation, n_elevation):
                    continue

                new_distance = distances.get(current) + 1
                if new_distance < distances.get(n):
                    distances[n] = new_distance
                    heapq.heappush(distances_heap, (new_distance, n))
            visited.add(current)

        return distances

    def _solve_one(self):
        distances = self._find_distances(
            start=self.data['start'],
            check_func=self._check_one_higher)
        return distances.get(self.data['end'])

    def _solve_two(self):
        # Run Dijkstra's algorithm using target point as a start. Then select shortest path to 'a' point.
        distances = self._find_distances(
            start=self.data['end'],
            check_func=self._check_one_lower)
        return min(
            distances.get(k)
            for k, (elevation, *_)
            in self.data['graph'].items()
            if elevation == 'a'
        )
