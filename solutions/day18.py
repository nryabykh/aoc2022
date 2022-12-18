"""
--- Day 18: Boiling Boulders ---
https://adventofcode.com/2022/day/18
"""

from common import BaseSolver


class Solver(BaseSolver):
    def _prepare(self):
        self.data['input'] = [list(map(int, line.split(','))) for line in self.data['input']]

    def _solve_one(self):
        area, cubes = 0, set()

        for x, y, z in self.data['input']:
            cube_adj = [(x, y, z - 1), (x, y, z + 1), (x, y - 1, z), (x, y + 1, z), (x - 1, y, z), (x + 1, y, z)]
            rem = sum(c in cubes for c in cube_adj)
            area += (6 - 2 * rem)
            cubes.add((x, y, z))
        return area

    def _solve_two(self):
        pass
