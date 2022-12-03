"""
--- Day 1: Calorie Counting ---
https://adventofcode.com/2022/day/1
"""

from common import BaseSolver


class Solver(BaseSolver):
    def _prepare(self):
        self.inner['carries'] = self._get_carries()

    def _solve_one(self):
        return max(self.inner['carries'])

    def _solve_two(self):
        return sum(sorted(self.inner['carries'])[-3:])

    def _get_carries(self):
        carries = []
        current = 0
        for ix, item in enumerate(self.data):
            if (item == '') or (ix == len(self.data) - 1):
                carries.append(current)
                current = 0
            else:
                current += int(item)
        return carries
