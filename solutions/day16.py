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
        time_left = 30
        opened = {'AA': 0}
        score = 0

        from collections import deque

        queue_first = deque()
        queue_first.append((current, opened, time_left, score, 'AA'))  # time left after valve opening; score if no nothing till the end

        queue_second = deque()
        queue_second.append((current, opened, time_left, score, 'AA'))

        max_score = 0
        max_path = ('', '')
        paths_first = set()
        paths_second = set()


        # while queue_first or queue_second:
        #     opened1, opened2 = {}, {}
        #     if queue_first:
        #         v1, opened1, time_left1, score1, path1 = queue_first.pop()
        #     if queue_second:
        #         v2, opened2, time_left2, score2, path2 = queue_second.pop()
        #
        #     opened = {**opened1, **opened2}
        #
        #     if opened1:
        #         first_steps = self._get_next_steps(v1, opened, time_left1, score1, path1)
        #
        #     if opened
        #
        #     second_steps =





        print(max_score, max_path)

    def _get_next_steps(self, valve, opened, time_left, score, path):
        steps = []
        for next_v in self.data['valves_nonzero']:
            if next_v in opened:
                continue

            distance = self.data['distances'][valve][next_v]
            new_time_left = time_left - (distance + 1)
            if new_time_left <= 0:
                continue

            new_score = score + new_time_left * self.data['valves'][next_v].rate
            new_path = path + ' -> ' + next_v
            steps.append((
                next_v,
                {**opened, next_v: opened[valve] + distance + 1},
                new_time_left,
                new_score,
                new_path
            ))
            # path.add((new_score, new_path))
        return steps

    def _solve_queue(self):
        current = 'AA'
        time_left = 30
        opened = {'AA': 0}
        score = 0

        from collections import deque

        queue = deque()
        queue.append((current, opened, time_left, score, 'AA'))  # time left after valve opening; score if no nothing till the end

        max_score = 0
        max_path = ''

        while queue:
            current_v, opened, time_left, score, path = queue.pop()

            min_d, max_rate, cnt = sys.maxsize, 0, 0
            for next_v in self.data['valves_nonzero']:
                if next_v not in opened:
                    min_d = min(min_d, self.data['distances'][current_v][next_v])
                    max_rate = max(max_rate, self.data['valves'][next_v].rate)
                    cnt += 1
            if max_rate > 0 and score + (time_left - min_d - 1) * max_rate * cnt < max_score:
                continue

            for next_v in self.data['valves_nonzero']:
                if next_v in opened:
                    continue

                distance = self.data['distances'][current_v][next_v]
                new_time_left = time_left - (distance + 1)
                if new_time_left <= 0:
                    continue

                new_score = score + new_time_left * self.data['valves'][next_v].rate
                new_path = path + ' -> ' + next_v
                queue.append((
                    next_v,
                    {**opened, next_v: opened[current_v] + distance + 1},
                    new_time_left,
                    new_score,
                    new_path
                ))
                if new_score > max_score:
                    max_score = new_score
                    max_path = new_path

        print(max_score, max_path)
        return max_score
