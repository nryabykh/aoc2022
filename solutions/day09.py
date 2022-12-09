"""


"""

from common import BaseSolver


class Solver(BaseSolver):
    def _prepare(self):
        moves = list(map(lambda x: (x[0], int(x[1])), [move.split() for move in self.data['input']]))
        self.data['moves'] = moves
        self.data['pos'] = (0, 0)

    def _solve_one(self):
        xh, yh, xt, yt = 0, 0, 0, 0
        t_fields = {(0, 0)}
        for d, n in self.data['moves']:
            if d == 'R':
                for _ in range(n):
                    xh += 1
                    xt, yt = self._move_tail(xh, yh, xt, yt)
                    print(f'after: {xh=}, {yh=}, {xt=}, {yt=}')
                    t_fields.add((xt, yt))
            if d == 'L':
                for _ in range(n):
                    xh -= 1
                    xt, yt = self._move_tail(xh, yh, xt, yt)
                    print(f'after: {xh=}, {yh=}, {xt=}, {yt=}')
                    t_fields.add((xt, yt))
            if d == 'U':
                for _ in range(n):
                    yh += 1
                    xt, yt = self._move_tail(xh, yh, xt, yt)
                    print(f'after: {xh=}, {yh=}, {xt=}, {yt=}')
                    t_fields.add((xt, yt))
            if d == 'D':
                for _ in range(n):
                    yh -= 1
                    xt, yt = self._move_tail(xh, yh, xt, yt)
                    print(f'after: {xh=}, {yh=}, {xt=}, {yt=}')
                    t_fields.add((xt, yt))

        return len(t_fields)

    @staticmethod
    def _move_tail(xh, yh, xt, yt) -> tuple[int, int]:
        if abs(xh-xt) <= 1 and abs(yh-yt) <= 1:
            pass
        elif xh == xt:  # abs(hy-ty)>1 => ==2
            yt = yh - 1 if yh > yt else yh + 1
        elif yh == yt:
            xt = xh - 1 if xh > xt else xh + 1
        else:
            dx = (xh - xt) // abs(xh - xt)
            dy = (yh - yt) // abs(yh - yt)
            xt += dx
            yt += dy

        return xt, yt

    def _solve_two(self):
        xy = [(0, 0) for _ in range(10)]

        print(xy)
        print(f'current: {xy=}')
        t_fields = {(0, 0)}
        for d, n in self.data['moves']:
            if d == 'R':
                for _ in range(n):
                    xh, yh = xy[0]
                    xy[0] = (xh + 1, yh)
                    for i in range(1, 10):
                        xt, yt = self._move_tail(*xy[i-1], *xy[i])
                        xy[i] = (xt, yt)
                        print(f'after: {xy=}')
                    t_fields.add(xy[-1])
            if d == 'L':
                for _ in range(n):
                    xh, yh = xy[0]
                    xy[0] = (xh - 1, yh)
                    for i in range(1, 10):
                        xt, yt = self._move_tail(*xy[i - 1], *xy[i])
                        xy[i] = (xt, yt)
                        print(f'after: {xy=}')
                    t_fields.add(xy[-1])
            if d == 'U':
                for _ in range(n):
                    xh, yh = xy[0]
                    xy[0] = (xh, yh + 1)
                    for i in range(1, 10):
                        xt, yt = self._move_tail(*xy[i - 1], *xy[i])
                        xy[i] = (xt, yt)
                        print(f'after: {xy=}')
                    t_fields.add(xy[-1])
            if d == 'D':
                for _ in range(n):
                    xh, yh = xy[0]
                    xy[0] = (xh, yh - 1)
                    for i in range(1, 10):
                        xt, yt = self._move_tail(*xy[i - 1], *xy[i])
                        xy[i] = (xt, yt)
                        print(f'after: {xy=}')
                    t_fields.add(xy[-1])

        return len(t_fields)