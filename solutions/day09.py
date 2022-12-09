"""
--- Day 9: Rope Bridge ---
https://adventofcode.com/2022/day/9
"""

from common import BaseSolver

Coord = tuple[int, int]


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
        return len(self._get_tail_fields(rope_length=2))

    def _solve_two(self):
        return len(self._get_tail_fields(rope_length=10))

    def _get_tail_fields(self, rope_length: int) -> set[Coord]:
        xy = [(0, 0) for _ in range(rope_length)]
        t_fields = {(0, 0)}

        for d in self.data['moves']:
            xy = self._move_rope(d, xy, rope_length)
            t_fields.add(xy[-1])

        return t_fields

    def _move_rope(self, direction: str, xy: list[Coord], rope_length: int) -> list[Coord]:
        xy[0] = self.data['steps'][direction](*xy[0])
        for i in range(1, rope_length):
            xy[i] = self._move_tail(*xy[i - 1], *xy[i])
        return xy

    @staticmethod
    def _move_tail(xh, yh, xt, yt) -> Coord:
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
