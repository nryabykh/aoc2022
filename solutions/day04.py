"""
--- Day 4: Camp Cleanup ---
https://adventofcode.com/2022/day/4
"""

from common import BaseSolver


class Solver(BaseSolver):
    def _prepare(self):
        self.data['split'] = [
            (
                *self._get_bounds(line.split(',')[0]),
                *self._get_bounds(line.split(',')[1])
            )
            for line in self.data['input']
        ]

    def _solve_one(self):
        return sum(
            (a <= x and b >= y) or (x <= a and y >= b)
            for a, b, x, y in self.data['split']
        )

    def _solve_two(self):
        return sum(
            not ((x > b) or (a > y))
            for a, b, x, y, in self.data['split']
        )

    @staticmethod
    def _get_bounds(s: str):
        return list(map(int, s.split('-')))

