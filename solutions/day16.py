"""

"""
import heapq
import itertools
import re
import sys
from dataclasses import dataclass

from common import BaseSolver


@dataclass
class Valve:
    name: str
    rate: int
    children: list[str]


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

    def _single_step(self, current: str, time_left: int, opened: set[str], depth: int) -> list:
        scores = []
        if depth == 0:
            return [(0, [])]
        # print(f'{current=}, {time_left=}, {opened=}, {depth=}')

        for v_name, valve in self.data['valves_nonzero'].items():
            if v_name in opened:
                continue

            tl_next = time_left - self.data['distances'][current][v_name] - 1
            next_profit = tl_next * valve.rate
            if next_profit > 0:
                opened_new = opened.copy()
                opened_new.add(v_name)
                # print(f'-- to the depth {depth-1}')
                next_scores = self._single_step(v_name, tl_next, opened_new, depth-1)
                # if depth > 1:
                    # print(f'from {depth=} and {v_name=}: {next_scores=}')
                if next_scores:
                    next_best, next_path = sorted(next_scores)[-1]
                    scores.append((next_profit + next_best if next_scores else 0, [v_name] + next_path))
                else:
                    scores.append((next_profit, [v_name]))

        return scores

    def _single_step_we(self, current: str, time_left: int, opened: set[str], depth: int) -> list:
        scores = []
        if depth == 0:
            return [(0, [], [])]
        # print(f'{current=}, {time_left=}, {opened=}, {depth=}')

        for v_name, valve in self.data['valves_nonzero'].items():
            if v_name in opened:
                continue

            tl_next = time_left - self.data['distances'][current][v_name] - 1
            next_profit = tl_next * valve.rate
            if next_profit <= 0:
                continue

            opened_new = opened.copy()
            opened_new.add(v_name)

            el_steps = sorted(self._single_step(current, time_left, opened_new, depth), reverse=True)
            el_path = []
            if el_steps:
                print(f'{el_steps=}')
                # el_best, el_path, *_ = el_steps
                # next_profit += el_best

            # print(f'-- to the depth {depth-1}')
            next_scores = self._single_step(v_name, tl_next, opened_new, depth)
            print(f'{next_scores=}')
            # if depth > 1:
                # print(f'from {depth=} and {v_name=}: {next_scores=}')
            if next_scores:
                next_best, next_path = sorted(next_scores)[-1]
                scores.append((next_profit + next_best if next_scores else 0, [v_name] + next_path, el_path))
                print(f'{scores=}')
            else:
                scores.append((next_profit, [v_name], el_path))
        print(f'{scores=}')
        return scores

    def _solve_one(self):
        current = 'AA'
        time_left = 30
        opened = set()

        prev_score, score, depth = None, 0, 1
        while score != prev_score:
            prev_score = score
            res = sorted(
                self._single_step(current, time_left, opened, depth=depth),
                reverse=True
            )
            print(f'{depth=}, {score=}')
            score, *_ = res[0]
            depth += 1

        return score

    def _solve_two(self):
        current = 'AA'
        time_left = 26
        opened = set()

        opened.add('DD')

        res = sorted(
            self._single_step(current, time_left, opened, depth=8),
            reverse=True
        )
        print(res[0])
        # prev_score, score, depth = None, 0, 1
        # while score != prev_score:
        #     prev_score = score
        #     res = sorted(
        #         self._single_step_we(current, time_left, opened, depth=depth),
        #         reverse=True
        #     )
        #     print(f'{depth=}, {score=}')
        #     score, *_ = res[0]
        #     depth += 1
        score, *_ = res[0]
        return score
