"""
--- Day 17: Pyroclastic Flow ---
https://adventofcode.com/2022/day/17
"""

from common import BaseSolver

WIDE = 7


class Solver(BaseSolver):
    def _prepare(self):
        self.data['figures'] = {
            '-': [(0, 0), (1, 0), (2, 0), (3, 0)],
            '+': [(0, 1), (1, 0), (1, 1), (1, 2), (2, 1)],
            '_I': [(0, 0), (1, 0), (2, 0), (2, 1), (2, 2)],
            'I': [(0, 0), (0, 1), (0, 2), (0, 3)],
            'o': [(0, 0), (1, 0), (0, 1), (1, 1)]
        }

    def _move_till_rest(self, tick: int, coords, rocks):
        jets = self.data['input'][0]
        collision = False

        while not collision:
            jet = jets[tick % len(jets)]

            coords = self._move_jet(coords, jet, rocks)
            collision, coords = self._move_down(coords, rocks)
            tick += 1

        return tick, coords

    def _solve_one(self):
        rocks_number = 2022
        figures = list(self.data['figures'].keys())

        rock_cnt, tick, max_y = 0, 0, 0
        rocks = set()
        while rock_cnt < rocks_number:
            fig = figures[rock_cnt % 5]
            coords = [(x + 2, y + max_y + 4) for (x, y) in self.data['figures'][fig]]

            tick, coords = self._move_till_rest(tick, coords, rocks)
            for c in coords:
                rocks.add(c)

            rock_cnt += 1
            max_y = max(max_y, max(y for x, y in coords))

        return max_y

    @staticmethod
    def _move_jet(coords, jet, rocks):
        shift = 1 if jet == '>' else -1
        new_coords = [(x + shift, y) for (x, y) in coords]
        for x, y in new_coords:
            if x < 0 or x == WIDE or (x, y) in rocks:
                return coords
        return new_coords

    @staticmethod
    def _check_collision(coords, rocks):
        return any(c in rocks for c in coords)

    @staticmethod
    def _move_down(coords, rocks):
        new_coords = [(x, y - 1) for (x, y) in coords]
        for x, y in new_coords:
            if (x, y) in rocks or y == 0:
                return True, coords
        return False, new_coords

    @staticmethod
    def get_snapshot(lines: int, rocks: set):
        max_y = max(y for _, y in rocks) if rocks else 0
        lower = 0 if max_y <= lines else max_y - lines

        return '\n'.join(
            (''.join('#' if (j, i) in rocks else '.' for j in range(WIDE))) for i in range(max_y, lower, -1))

    def _solve_two(self):
        rocks_number = 1000000000000
        figures = list(self.data['figures'].keys())
        jets = self.data['input'][0]

        rock_cnt, tick, max_y = 0, 0, 0
        rocks, start_conditions, pattern_detected = set(), {}, False
        snapshot_lines = 7

        while rock_cnt < rocks_number:
            fig = figures[rock_cnt % 5]

            csn = self.get_snapshot(snapshot_lines, rocks)
            if not pattern_detected and (fig, tick % len(jets), csn) in start_conditions:
                height_before_pattern, figs_before_pattern = start_conditions[(fig, tick % len(jets), csn)]
                pattern_height = max_y - height_before_pattern
                pattern_figs = rock_cnt - figs_before_pattern
                number_of_copies = (rocks_number - figs_before_pattern) // pattern_figs
                rock_cnt = rock_cnt + (number_of_copies - 1) * pattern_figs
                new_rocks = set()
                for x, y in rocks:
                    new_rocks.add((x, y + (number_of_copies - 1) * pattern_height))
                pattern_detected = True
                rocks = new_rocks
                max_y = max(max_y, max(y for x, y in rocks))
                print(f'{height_before_pattern=}, {figs_before_pattern=}, {pattern_height=}, {pattern_figs=}, {number_of_copies=}, {rock_cnt=}, {fig=}')

            if rock_cnt == rocks_number:
                break

            coords = [(x + 2, y + max_y + 4) for (x, y) in self.data['figures'][fig]]
            start_conditions[(fig, tick % len(jets), self.get_snapshot(snapshot_lines, rocks))] = (max_y, rock_cnt)

            tick, coords = self._move_till_rest(tick, coords, rocks)
            for c in coords:
                rocks.add(c)

            rock_cnt += 1
            max_y = max(max_y, max(y for x, y in coords))

        return max_y
