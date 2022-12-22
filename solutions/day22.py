"""

"""
import re

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
        dirs = 'rdlu'
        tiles = self.data['tiles']
        cols = self.data['cols']
        x, y = tiles[0].index('.'), 0
        dir_ix = 0
        # dir_draw = '>v<^'

        for steps, next_dir in self.data['steps']:
            d = dirs[dir_ix % 4]
            # print(f'new instruction: {steps} steps in {d}')
            for step in range(steps):
                xn, yn = self._get_next(x, y, d)
                # print(f'current {x=} {y=} {d=} next {xn=} {yn=}')
                if (
                        (d == 'r' and xn >= len(tiles[yn])) or
                        (d == 'l' and xn < 0) or
                        (d == 'd' and yn >= len(cols[xn])) or
                        (d == 'u' and yn < 0) or
                        tiles[yn][xn] == ' '
                ):
                    xn, yn = self._get_wrap(x, y, d)
                    # print(f'out of map or empty tile, wrap to {xn=}, {yn=}')

                if tiles[yn][xn] == '#':
                    # print(f'wall, take next instruction')
                    break

                x, y = xn, yn
                cur_tile = tiles[y]
                # tiles[y] = cur_tile[:x] + dir_draw[dir_ix % 4] + (cur_tile[x+1:] if x+1 < len(cur_tile) else '')
            if next_dir == 'R':
                dir_ix += 1
            elif next_dir == 'L':
                dir_ix -= 1
            else:
                dir_ix = dir_ix

        # for tile in tiles:
        #     print(tile)

        # print(x + 1, y + 1)
        return 1000 * (y + 1) + 4 * (x + 1) + dir_ix % 4

    def _get_wrap(self, _x, _y, d):
        row = self.data['tiles'][_y]
        col = self.data['cols'][_x]

        wraps = {
            'r': (len(row) - len(row.lstrip()), _y),
            'l': (len(row.rstrip()) - 1, _y),
            'd': (_x, len(col) - len(col.lstrip())),
            'u': (_x, len(col.rstrip()) - 1),
        }
        return wraps[d]

    @staticmethod
    def _get_next(_x, _y, direction):
        nexts = {
            'r': lambda x, y: (x + 1, y),
            'l': lambda x, y: (x - 1, y),
            'd': lambda x, y: (x, y + 1),
            'u': lambda x, y: (x, y - 1)
        }
        return nexts[direction](_x, _y)

    def _solve_two(self):
        pass
