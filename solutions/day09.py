"""
--- Day 9: Rope Bridge ---
https://adventofcode.com/2022/day/9
"""

from common import BaseSolver


class Solver(BaseSolver):
    def _prepare(self):
        moves_str = ""
        for move in self.data['input']:
            d, n = move.split()
            moves_str += d * int(n)
        self.data['moves'] = moves_str
        self.data['steps'] = {
            'R': lambda x, y: (x + 1, y),
            'L': lambda x, y: (x - 1, y),
            'U': lambda x, y: (x, y + 1),
            'D': lambda x, y: (x, y - 1)
        }

    def _solve_one(self):
        xh, yh, xt, yt = 0, 0, 0, 0
        t_fields = {(0, 0)}

        for d in self.data['moves']:
            xh, yh = self.data['steps'][d](xh, yh)
            xt, yt = self._move_tail(xh, yh, xt, yt)
            t_fields.add((xt, yt))

        return len(t_fields)

    def _solve_two(self):
        rope_length = 10
        xy = [(0, 0) for _ in range(rope_length)]
        t_fields = {(0, 0)}

        for d in self.data['moves']:
            xy[0] = self.data['steps'][d](*xy[0])
            for i in range(1, rope_length):
                xy[i] = self._move_tail(*xy[i - 1], *xy[i])
            t_fields.add(xy[-1])

        return len(t_fields)

    @staticmethod
    def _move_tail(xh, yh, xt, yt) -> tuple[int, int]:
        if abs(xh - xt) <= 1 and abs(yh - yt) <= 1:
            pass
        elif xh == xt:
            yt = yh - 1 if yh > yt else yh + 1
        elif yh == yt:
            xt = xh - 1 if xh > xt else xh + 1
        else:
            xt += (xh - xt) // abs(xh - xt)
            yt += (yh - yt) // abs(yh - yt)

        return xt, yt
