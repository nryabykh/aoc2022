"""
--- Day 25: Full of Hot Air ---
https://adventofcode.com/2022/day/25
"""

import math
from typing import Union

from common import BaseSolver


class Solver(BaseSolver):
    def _prepare(self):
        pass

    def _solve_one(self):
        s = 0
        for line in self.data['input']:
            n = 0
            for i, c in enumerate(line[::-1]):
                if c.isdigit():
                    n += int(c) * pow(5, i)
                else:
                    m = -1 if c == '-' else -2
                    n += m * pow(5, i)
            s += n

        res = ''
        for i in range(int(math.log(s, 5)), -1, -1):
            q = s // pow(5, i)
            s = s % pow(5, i)
            res += str(q)

        res = list(res)
        settled = False
        while not settled:
            settled = True
            for i in range(1, len(res)):
                if res[i].isdigit() and int(res[i]) > 2:
                    res[i-1] = self._get_up(res[i-1])
                    res[i] = '-' if int(res[i]) == 4 else '='
                    settled = False

        return ''.join(res)

    @staticmethod
    def _get_up(x: Union[str, int]):
        if x.isdigit():
            return str(int(x) + 1)
        elif x == '-':
            return '0'
        elif x == '=':
            return '-'
        else:
            return str(x)

    def _solve_two(self):
        pass
