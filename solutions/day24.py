"""
--- Day 24: Blizzard Basin ---
https://adventofcode.com/2022/day/24
"""

import math
from heapq import heappop, heappush

from common import BaseSolver


class Solver(BaseSolver):
    def _prepare(self):
        lines = self.data['input']
        x0, y0 = lines[0].index('.'), 0
        xt, yt = lines[-1].index('.'), len(lines) - 1

        x_borders = (0, len(lines[0]) - 1)
        y_borders = (0, len(lines) - 1)

        blizzards = [(x, y, c) for y, line in enumerate(lines) for x, c in enumerate(line) if c in '<>v^']

        self.data['blizzards'] = blizzards
        self.data['borders'] = (*x_borders, *y_borders)
        self.data['entries'] = ((x0, y0), (xt, yt))

    def _get_next(self, _x, _y, c):
        x_min, x_max, y_min, y_max = self.data['borders']
        d = {
            '>': lambda x, y: (x + 1, y) if x + 1 < x_max else (x_min + 1, y),
            '<': lambda x, y: (x - 1, y) if x - 1 > x_min else (x_max - 1, y),
            'v': lambda x, y: (x, y + 1) if y + 1 < y_max else (x, y_min + 1),
            '^': lambda x, y: (x, y - 1) if y - 1 > y_min else (x, y_max - 1)
        }
        return *d[c](_x, _y), c

    def _get_pattern(self):
        x_min, x_max, y_min, y_max = self.data['borders']
        pattern_length = math.lcm(x_max - x_min - 1, y_max - y_min - 1)

        moves, bl_pattern = 0, {}
        bl = self.data['blizzards']
        while moves < pattern_length:
            new_bl, bl_pattern[moves] = [], set()
            for x, y, c in bl:
                bl_pattern[moves].add((x, y))
                new_bl.append(self._get_next(x, y, c))
            moves, bl = moves + 1, new_bl

        return bl_pattern

    def _get_path_length(self, x_from, y_from, x_to, y_to, start_tick=0):
        x_min, x_max, y_min, y_max = self.data['borders']
        bl_pattern = self._get_pattern()
        pattern_len = len(bl_pattern)

        heap, seen, target, move = [], set(), False, start_tick
        heappush(heap, (move, x_from, y_from))

        while not target:
            move, x, y = heappop(heap)
            move += 1
            for xn, yn in [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1), (x, y)]:
                if xn == x_to and yn == y_to:
                    print(f'target {x_to},{y_to} reached at {move=}')
                    target = True
                elif (
                        (xn, yn) not in bl_pattern[move % pattern_len] and
                        ((x_min < xn < x_max and y_min < yn < y_max) or (xn == x_from and yn == y_from)) and
                        (move % pattern_len, xn, yn) not in seen
                ):
                    heappush(heap, (move, xn, yn))
                    seen.add((move % pattern_len, xn, yn))
        return move

    def _solve_one(self):
        (x0 , y0), (xt, yt) = self.data['entries']
        return self._get_path_length(x0, y0, xt, yt)

    def _solve_two(self):
        (x0, y0), (xt, yt) = self.data['entries']

        moves = []
        for xs, ys, xe, ye in [
            (x0, y0, xt, yt),
            (xt, yt, x0, y0),
            (x0, y0, xt, yt)
        ]:
            moves.append(self._get_path_length(xs, ys, xe, ye, 0 if not moves else moves[-1]))
        return moves[-1]
