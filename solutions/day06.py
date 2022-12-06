"""
--- Day 6: Tuning Trouble ---
https://adventofcode.com/2022/day/6
"""

from common import BaseSolver


class Solver(BaseSolver):
    def _prepare(self):
        pass

    def _get_index_of_unique_sequence(self, chars: int):
        line = self.data['input'][0]
        for i in range(chars-1, len(line)):
            sliced = line[i-(chars-1):i+1]
            if len(sliced) == len(set(sliced)):
                return i+1

    def _solve_one(self):
        return self._get_index_of_unique_sequence(chars=4)

    def _solve_two(self):
        return self._get_index_of_unique_sequence(chars=14)
