"""
--- Day 1: Calorie Counting ---
https://adventofcode.com/2022/day/1
"""

from common import BaseSolver


class Solver(BaseSolver):
    def _prepare(self):
        self.data['carries'] = self._get_carries()

    def _solve_one(self):
        return max(self.data['carries'])

    def _solve_two(self):
        return sum(sorted(self.data['carries'])[-3:])

    def _get_carries(self):
        data = self.data['input']
        carries = []
        current = 0
        for ix, item in enumerate(data):
            if (item == '') or (ix == len(data) - 1):
                carries.append(current)
                current = 0
            else:
                current += int(item)
        return carries
