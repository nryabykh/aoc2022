"""

"""
import sys
import time

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

    def _solve_one(self):
        rocks_number = 2022
        figures = list(self.data['figures'].keys())
        jets = self.data['input'][0]

        rock_cnt, tick, max_y = 0, 0, 0
        rocks = set()
        while rock_cnt < rocks_number:
            fig = figures[rock_cnt % 5]
            coords = [(x + 2, y + max_y + 4) for (x, y) in self.data['figures'][fig]]
            collision = False
            fig_jets = ""

            while not collision:
                jet = jets[tick % len(jets)]

                coords = self._move_jet(coords, jet, rocks)
                collision, coords = self._move_down(coords, rocks)
                tick += 1
                fig_jets += jet

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

    def _get_lines(self, coords: set) -> dict:
        lines = {}
        for x, y in coords:
            if y in lines:
                lines[y].append(x)
            else:
                lines[y] = [x]
        for y in lines:
            lines[y] = sorted(lines[y])
        return lines

    def _check_pattern(self, lines, n=4):
        y = max(lines.keys())
        keys = list(lines.keys())
        checked_pattern = [lines[k] for k in keys[-n:]]
        start_ix = -1
        for k in keys[:-n]:
            res = all(lines[k + i] == check_line for i, check_line in enumerate(checked_pattern))
            if res:
                start_ix = k

        return start_ix

    def _solve_two(self):
        rocks_number = 1000000000000
        figures = list(self.data['figures'].keys())
        jets = self.data['input'][0]

        rock_cnt, tick, max_y = 0, 0, 0
        rocks = set()
        start_conditions = {}
        pattern_detected = False
        while rock_cnt < rocks_number:
            fig = figures[rock_cnt % 5]

            if not pattern_detected and (fig, tick % len(jets)) in start_conditions:
                height_before_pattern, figs_before_pattern = start_conditions[(fig, tick % len(jets))]
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
                print(f'{height_before_pattern=}, {pattern_height=}, {pattern_figs=}, {number_of_copies=}, {rock_cnt=}')
                print(f'{fig}, {figures[rock_cnt % 5]}')

            if rock_cnt == rocks_number:
                break

            coords = [(x + 2, y + max_y + 4) for (x, y) in self.data['figures'][fig]]
            collision = False
            fig_jets = ""

            start_conditions[(fig, tick % len(jets))] = (max_y, rock_cnt)
            while not collision:
                jet = jets[tick % len(jets)]

                coords = self._move_jet(coords, jet, rocks)
                collision, coords = self._move_down(coords, rocks)
                tick += 1
                fig_jets += jet

            for c in coords:
                rocks.add(c)

            rock_cnt += 1
            max_y = max(max_y, max(y for x, y in coords))

        return max_y
