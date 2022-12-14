"""
--- Day 8: Treetop Tree House ---
https://adventofcode.com/2022/day/8
"""

import itertools
from functools import reduce
from typing import Iterable

from common import BaseSolver


class Solver(BaseSolver):
    def _prepare(self):
        data = [[int(c) for c in line] for line in self.data['input']]
        height, width = len(data), len(data[0])
        observables = []
        for i in range(height):
            row = data[i]
            for j in range(width):
                cur = row[j]
                col = [line[j] for line in data]

                lefts, rights = row[:j], row[(j+1):]
                tops, bottoms = col[:i], col[(i+1):]
                observables.append((cur, lefts, rights, tops, bottoms))

        self.data['observables'] = observables

    def _solve_one(self):
        return sum(
            any((not other) or (max(other) < cur) for other in others)
            for cur, *others in self.data['observables']
        )

    def _solve_two(self):
        scores = []
        for cur, *others in self.data['observables']:
            distances = [self._get_distance(cur, other, i % 2 == 0) for i, other in enumerate(others)]
            scores.append(self._get_product(distances))
        return max(scores)

    @staticmethod
    def _get_distance(cur: int, others: list[int], reverse: bool = False):
        others = others[::-1] if reverse else others
        observables = list(itertools.takewhile(lambda x: x < cur, others))
        is_all_observable = len(others) == len(observables)
        return len(observables) + (int(not is_all_observable))

    @staticmethod
    def _get_product(items: Iterable[int]):
        return reduce(lambda x, y: x*y, items)
