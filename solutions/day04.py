"""
--- Day 4: Camp Cleanup ---
https://adventofcode.com/2022/day/4
"""

from common import BaseSolver


def _get_bounds(s: str):
    return list(map(int, s.split('-')))


class Solver(BaseSolver):
    def _prepare(self):
        split = []
        for line in self.data['input']:
            first, second = line.split(',')
            a, b = _get_bounds(first)  # a <= b
            x, y = _get_bounds(second)  # x <= y
            split.append((a, b, x, y))
        self.data['split'] = split

    def _solve_one(self):
        return sum((a <= x and b >= y) or (x <= a and y >= b) for a, b, x, y in self.data['split'])

    def _solve_two(self):
        return sum(not ((x > b) or (a > y)) for a, b, x, y, in self.data['split'])
