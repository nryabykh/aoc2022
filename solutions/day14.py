"""
--- Day 14: Regolith Reservoir ---
https://adventofcode.com/2022/day/14
"""

from common import BaseSolver


class Solver(BaseSolver):
    def _prepare(self):
        walls = set()
        for wall in self.data['input']:
            points = wall.split(' -> ')
            for i in range(len(points) - 1):
                x_from, y_from = list(map(int, points[i].split(',')))
                x_to, y_to = list(map(int, points[i + 1].split(',')))
                if x_from == x_to:
                    start, end = (y_from, y_to) if y_from < y_to else (y_to, y_from)
                    for y in range(start, end + 1):
                        walls.add((x_from, y))
                if y_from == y_to:
                    start, end = (x_from, x_to) if x_from < x_to else (x_to, x_from)
                    for x in range(start, end + 1):
                        walls.add((x, y_from))

        self.data['walls'] = walls

    def _solve_one(self):
        walls = self.data['walls'].copy()
        abyss_start = max(y for x, y in walls) + 1

        sands = 0
        x_sand, y_sand = 500, 0
        while y_sand < abyss_start:
            x_new, y_new = self._get_next(x_sand, y_sand, walls)
            if (x_new, y_new) == (x_sand, y_sand):
                walls.add((x_sand, y_sand))
                sands += 1
                x_sand, y_sand = 500, 0
            else:
                x_sand, y_sand = x_new, y_new

        return sands

    def _solve_two(self):
        walls = self.data['walls'].copy()
        my = max(y for x, y in walls) + 2
        for x in range(500 - my - 10, 500 + my + 10):
            walls.add((x, my))

        sands = 0
        x_sand, y_sand = 500, 0
        while True:
            x_new, y_new = self._get_next(x_sand, y_sand, walls)
            if (x_new, y_new) == (x_sand, y_sand):
                walls.add((x_sand, y_sand))
                sands += 1
                if x_sand == 500 and y_sand == 0:
                    break
                x_sand, y_sand = 500, 0
            else:
                x_sand, y_sand = x_new, y_new

        return sands

    @staticmethod
    def _get_next(x, y, walls) -> tuple[int, int]:
        variants = [(x, y + 1), (x - 1, y + 1), (x + 1, y + 1), (x, y)]
        return [v for v in variants if v not in walls].pop(0)
