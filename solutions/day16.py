"""
--- Day 16: Proboscidea Volcanium ---
https://adventofcode.com/2022/day/16
"""

import heapq
import re
import sys
from collections import deque
from dataclasses import dataclass
from typing import Union

from common import BaseSolver


@dataclass
class Valve:
    name: str
    rate: int
    children: list[str]


@dataclass
class QueueItem:
    current: Union[str, tuple[str, str]]
    opened: dict
    time_left: Union[int, tuple[int, int]]
    score: int
    path: str
    last: str = None


class Solver(BaseSolver):
    def _prepare(self):
        valves = {}
        pattern = """Valve ([A-Z]{2}) has flow rate=(\d+); tunnels? leads? to valves? (.*)"""
        for line in self.data['input']:
            name, rate, children_str = re.findall(pattern, line)[0]
            valves[name] = Valve(name, int(rate), children_str.split(', '))

        # print(valves)
        self.data['valves'] = valves
        self.data['valves_nonzero'] = {k: v for k, v in valves.items() if v.rate > 0}

        distances = {}
        for k in valves:
            distances[k] = self._dijkstra(k)
        self.data['distances'] = distances
        # print(distances)

    def _dijkstra(self, start: str):
        """
        Dijkstra's algorithm for finding the shortest paths from start to any other point.
        """

        graph: dict[str, Valve] = self.data['valves']  # dict[str: Valve]
        distances = {k: 0 if k == start else sys.maxsize for k in graph}
        distances_heap = []
        for k, v in distances.items():
            heapq.heappush(distances_heap, (v, k))
        visited = set()
        while (
                len(visited) < len(graph) and
                any(dist != sys.maxsize for node, dist in distances.items() if node not in visited)
        ):
            distance_current, node_current = heapq.heappop(distances_heap)
            neighbours = graph.get(node_current).children
            for n in neighbours:
                if n in visited:
                    continue

                new_distance = distance_current + 1
                if new_distance < distances.get(n):
                    distances[n] = new_distance
                    heapq.heappush(distances_heap, (new_distance, n))
            visited.add(node_current)

        return distances

    def _solve_one(self):
        queue = deque()
        queue.append(QueueItem(current='AA', opened={'AA': 0}, time_left=30, score=0, path='AA'))

        max_score, max_path = 0, ''

        while queue:
            move = queue.pop()

            min_d, max_rate, cnt = sys.maxsize, 0, 0
            for next_v in self.data['valves_nonzero']:
                if next_v not in move.opened:
                    min_d = min(min_d, self.data['distances'][move.current][next_v])
                    max_rate = max(max_rate, self.data['valves'][next_v].rate)
                    cnt += 1
            if max_rate > 0 and move.score + (move.time_left - min_d - 1) * max_rate * cnt < max_score:
                continue

            for next_v in self.data['valves_nonzero']:
                if next_v in move.opened:
                    continue

                distance = self.data['distances'][move.current][next_v]
                new_time_left = move.time_left - (distance + 1)
                if new_time_left <= 0:
                    continue

                new_score = move.score + new_time_left * self.data['valves'][next_v].rate
                new_path = move.path + ' -> ' + next_v
                queue.append(QueueItem(
                    current=next_v,
                    opened={**move.opened, next_v: move.opened[move.current] + distance + 1},
                    time_left=new_time_left,
                    score=new_score,
                    path=new_path
                ))
                if new_score > max_score:
                    max_score, max_path = new_score, new_path

        print(f'{max_score=} for path {max_path}')
        return max_score

    def _solve_two(self):
        queue = deque()
        queue.append(QueueItem(
            current=('AA', 'AA'),
            opened={'AA': 0},
            time_left=(26, 26),
            score=0,
            path='AA',
            last='hum'
        ))

        max_score, max_path = 0, ''

        while queue:
            move = queue.pop()

            min_d, max_rate, cnt = sys.maxsize, 0, 0
            who_to_move = 'hum' if move.last == 'el' else 'el'
            current_v = move.current[0] if who_to_move == 'hum' else move.current[1]
            time_left = move.time_left[0] if who_to_move == 'hum' else move.time_left[1]

            for next_v in self.data['valves_nonzero']:
                if next_v not in move.opened:
                    min_d = min(min_d, self.data['distances'][current_v][next_v])  # min dist to closed valves
                    max_rate = max(max_rate, self.data['valves'][next_v].rate)  # max rate of closes valves
                    cnt += 1  # number or closed valves

            # if all closed valves are on min distance and we'll open all of them simultaneously -> potentially max score
            if max_rate > 0 and move.score + (max(move.time_left) - min_d - 1) * max_rate * cnt < max_score:
                continue

            for next_v in self.data['valves_nonzero']:
                if next_v in move.opened:
                    continue

                distance = self.data['distances'][current_v][next_v]
                new_time_left = time_left - (distance + 1)
                if new_time_left <= 0:
                    continue
                time_lefts = (new_time_left, move.time_left[1]) if who_to_move == 'hum' else (move.time_left[0], new_time_left)

                new_score = move.score + new_time_left * self.data['valves'][next_v].rate
                new_path = move.path + f' -> {who_to_move}' + next_v

                currents = (next_v, move.current[1]) if who_to_move == 'hum' else (move.current[0], next_v)

                queue.append(QueueItem(
                    current=currents,
                    opened={**move.opened, next_v: move.opened[current_v] + distance + 1},
                    time_left=time_lefts,
                    score=new_score,
                    path=new_path,
                    last=who_to_move
                ))

                if new_score > max_score:
                    max_score, max_path = new_score, new_path

        print(f'{max_score=} for path {max_path}')
        return max_score
