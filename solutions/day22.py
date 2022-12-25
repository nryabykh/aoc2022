"""
--- Day 22: Monkey Map ---
https://adventofcode.com/2022/day/22
"""

import re
from typing import Callable

from common import BaseSolver


class Solver(BaseSolver):
    def _prepare(self):
        raw = self.data['raw']
        tiles, path = raw.split('\n\n')
        tiles = tiles.split('\n')
        max_len = max(len(tile) for tile in tiles)
        tiles = [tile + ' '*(max_len - len(tile)) for tile in tiles]
        self.data['tiles'] = tiles

        cols = [''.join(tile[j] for tile in tiles) for j in range(len(tiles[0]))]
        self.data['cols'] = cols

        pattern = "(\d+[LR])"
        steps = [(int(s[:-1]), s[-1]) for s in re.findall(pattern, path)]
        last = int(path[len(''.join(str(s) + d for s, d in steps)):])
        steps.append((last, ''))

        self.data['steps'] = steps

    def _solve_one(self):
        return self._solve_single(self._get_wrap)

    def _solve_two(self):
        return self._solve_single(self._get_cube_wrap if not self.data['is_test'] else self._get_cube_wrap_test)

    def _solve_single(self, wrapper: Callable[[int, int, str], tuple[int, int, str]]):
        dirs = 'rdlu'
        tiles = self.data['tiles'].copy()
        cols = self.data['cols']
        x, y = tiles[0].index('.'), 0
        dir_ix = 0

        for steps, next_dir in self.data['steps']:
            d = dirs[dir_ix % 4]
            for step in range(steps):
                xn, yn, dn = self._get_next(x, y, d)
                if (
                        (d == 'r' and xn >= len(tiles[yn])) or
                        (d == 'l' and xn < 0) or
                        (d == 'd' and yn >= len(cols[xn])) or
                        (d == 'u' and yn < 0) or
                        tiles[yn][xn] == ' '
                ):
                    # out of map or empty tile
                    xn, yn, dn = wrapper(xn, yn, d)

                # wall, take next instruction
                if tiles[yn][xn] == '#':
                    break

                x, y, d = xn, yn, dn
                dir_ix = dirs.index(dn)

            # end of step, next instruction
            next_dirs = {'R': lambda q: q + 1, 'L': lambda q: q - 1}
            dir_ix = next_dirs.get(next_dir, lambda q: q)(dir_ix)

        return 1000 * (y + 1) + 4 * (x + 1) + dir_ix % 4

    @staticmethod
    def _get_next(_x, _y, d):
        nexts = {
            'r': lambda x, y: (x + 1, y, 'r'),
            'l': lambda x, y: (x - 1, y, 'l'),
            'd': lambda x, y: (x, y + 1, 'd'),
            'u': lambda x, y: (x, y - 1, 'u')
        }
        return nexts[d](_x, _y)

    def _get_wrap(self, _x, _y, d):
        y_max = len(self.data['tiles']) - 1
        x_max = len(self.data['tiles'][0]) - 1
        _x = 0 if _x < 0 else (x_max if _x > x_max else _x)
        _y = 0 if _y < 0 else (y_max if _y > y_max else _y)
        row = self.data['tiles'][_y]
        col = self.data['cols'][_x]

        wraps = {
            'r': (len(row) - len(row.lstrip()), _y, 'r'),
            'l': (len(row.rstrip()) - 1, _y, 'l'),
            'd': (_x, len(col) - len(col.lstrip()), 'd'),
            'u': (_x, len(col.rstrip()) - 1, 'u'),
        }
        return wraps[d]

    @staticmethod
    def _get_cube_wrap_test(x, y, d):
        a_up = 8 <= x < 12 and y < 0 and d == 'u'
        a_left = x < 8 and 0 <= y < 4 and d == 'l'
        a_right = x >= 12 and 0 <= y < 4 and d == 'r'

        b_up = 0 <= x < 4 and y < 4 and d == 'u'
        b_left = x < 0 and 4 <= y < 8 and d == 'l'
        b_down = 0 <= x < 4 and y >= 8 and d == 'd'

        c_up = 4 <= x < 8 and y < 4 and d == 'u'
        c_down = 4 <= x < 8 and y >= 8 and d == 'd'

        d_right = x >= 12 and 4 <= y < 8 and d == 'r'

        e_left = x < 8 and 8 <= y < 12 and d == 'l'
        e_down = 8 <= x < 12 and y >= 12 and d == 'd'

        f_up = 12 <= x < 16 and y < 8 and d == 'u'
        f_right = x >= 16 and 8 <= y < 12 and d == 'r'
        f_down = 12 <= x < 16 and y >= 12 and d == 'd'

        if a_up:
            return 11 - x, 4, 'd'
        elif a_left:
            return 4 + y, 4, 'd'
        elif a_right:
            return 15, 15 - y, 'l'
        elif b_up:
            return 11 - x, 0, 'd'
        elif b_left:
            return 15 - (y - 4), 15, 'u'
        elif b_down:
            return 15 - x, 15, 'u'
        elif c_up:
            return 8, x - 4, 'r'
        elif c_down:
            return 8, 11 - (x - 4), 'r'
        elif d_right:
            return 15 - (y - 4), 8, 'd'
        elif e_left:
            return 4 + (11 - x), 7, 'u'
        elif e_down:
            return 11 - x, 7, 'u'
        elif f_up:
            return 11, 4 + (15 - x), 'l'
        elif f_right:
            return 11, 15 - x, 'l'
        elif f_down:
            return 0, 4 + (15 - x), 'r'
        else:
            raise ValueError(f'No option for {x=}, {y=}, {d=}')

    @staticmethod
    def _get_cube_wrap(x, y, d):
        """
        Works only with my input and my cube net. Sorry for hardcode.
        """

        a_up = 50 <= x < 100 and y < 0 and d == 'u'
        a_left = x < 50 and 0 <= y < 50 and d == 'l'

        b_up = 100 <= x < 150 and y < 0 and d == 'u'
        b_right = x >= 150 and 0 <= y < 50 and d == 'r'
        b_down = 100 <= x < 150 and y >= 50 and d == 'd'

        c_right = x >= 100 and 50 <= y < 100 and d == 'r'
        c_left = x < 50 and 50 <= y < 100 and d == 'l'

        d_up = 0 <= x < 50 and y < 100 and d == 'u'
        d_left = x < 0 and 100 <= y < 150 and d == 'l'

        e_right = x >= 100 and 100 <= y < 150 and d == 'r'
        e_down = 50 <= x < 100 and y >= 150 and d == 'd'

        f_left = x < 0 and 150 <= y < 200 and d == 'l'
        f_down = y >= 200 and 0 <= x < 50 and d == 'd'
        f_right = x >= 50 and 150 <= y < 200 and d == 'r'

        if a_up:
            return 0, 150 + (x - 50), 'r'  # to F
        elif a_left:
            return 0, 149 - y, 'r'  # to D
        elif b_up:
            return x - 100, 199, 'u'  # to F
        elif b_right:
            return 99, 149 - y, 'l'  # to E
        elif b_down:
            return 99, 50 + (x - 100), 'l'  # to C
        elif c_right:
            return 100 + (y - 50), 49, 'u'  # to B
        elif c_left:
            return y - 50, 100, 'd'  # to D
        elif d_up:
            return 50, 50 + x, 'r'  # to C
        elif d_left:
            return 50, 149 - y, 'r'  # to A
        elif e_right:
            return 149, 149 - y, 'l'  # to B
        elif e_down:
            return 49, 150 + (x - 50), 'l'  # to F
        elif f_left:
            return 50 + (y - 150), 0, 'd'  # to A
        elif f_down:
            return 100 + x, 0, 'd'  # to B
        elif f_right:
            return 50 + (y - 150), 149, 'u'  # to E
        else:
            raise ValueError(f'No option for {x=}, {y=}, {d=}')
