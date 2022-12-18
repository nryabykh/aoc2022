"""
--- Day 18: Boiling Boulders ---
https://adventofcode.com/2022/day/18
"""
from collections import deque

from common import BaseSolver


class Solver(BaseSolver):
    def _prepare(self):
        self.data['input'] = [list(map(int, line.split(','))) for line in self.data['input']]
        self.data['input'] = [(x, y, z) for x, y, z in self.data['input']]
        pass

    @staticmethod
    def _get_adjs(x, y, z):
        return [(x, y, z - 1), (x, y, z + 1), (x, y - 1, z), (x, y + 1, z), (x - 1, y, z), (x + 1, y, z)]

    def _solve_one(self):
        area, cubes = 0, set()
        for x, y, z in self.data['input']:
            cube_adj = self._get_adjs(x, y, z)
            area += (6 - 2 * sum(c in cubes for c in cube_adj))
            cubes.add((x, y, z))
        return area

    def _solve_two(self):
        area = self._solve_one()
        cubes = set(self.data['input'])
        queue, checked = deque(), cubes.copy()

        min_x, min_y, min_z = [min(line[i] for line in cubes) for i in range(3)]
        max_x, max_y, max_z = [max(line[i] for line in cubes) for i in range(3)]

        x, y, z = min_x - 1, min_y - 1, min_z - 1
        queue.append((x, y, z))
        while queue:
            x, y, z = queue.popleft()
            adjs = self._get_adjs(x, y, z)
            for xa, ya, za in adjs:
                if min_x - 1 <= xa <= max_x + 1 and min_y - 1 <= ya <= max_y + 1 and min_z - 1 <= za <= max_z + 1:
                    if (xa, ya, za) not in checked:
                        queue.append((xa, ya, za))
                        checked.add((xa, ya, za))

        for x, y, z in cubes:
            adjs = self._get_adjs(x, y, z)
            inners = sum(adj not in checked for adj in adjs)
            area -= inners
        return area
