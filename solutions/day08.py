"""

"""
import itertools
from typing import Iterable

from common import BaseSolver


class Solver(BaseSolver):
    def _prepare(self):
        pass

    def _solve_one(self):
        visible = 0
        data = [[int(c) for c in line] for line in self.data['input']]
        height, width = len(data), len(data[0])
        for i in range(height):
            for j in range(width):
                cur = data[i][j]
                if i == 0 or j == 0 or i == height-1 or j == width-1:
                    visible += 1
                    continue
                else:
                    leftmax = max(data[i][:j])
                    rightmax = max(data[i][(j+1):])
                    col = [line[j] for line in data]
                    topmax = max(col[:i])
                    bottommax = max(col[(i+1):])
                    if leftmax < cur or rightmax < cur or topmax < cur or bottommax < cur:
                        visible += 1

        return visible

    def _solve_two(self):
        scores = []
        data = [[int(c) for c in line] for line in self.data['input']]
        height, width = len(data), len(data[0])
        for i in range(height):
            for j in range(width):
                cur = data[i][j]
                if i == 0 or j == 0 or i == height-1 or j == width-1:
                    scores.append(0)
                    continue
                else:
                    lefts, rights = data[i][:j], data[i][(j+1):]
                    col = [line[j] for line in data]
                    tops, bottoms = col[:i], col[(i+1):]
                    scores.append(
                        self._get_product(
                            (
                                self._get_distance(cur, lefts, reverse=True),
                                self._get_distance(cur, rights),
                                self._get_distance(cur, tops, reverse=True),
                                self._get_distance(cur, bottoms)
                            )
                        )
                    )
        return max(scores)

    @staticmethod
    def _get_distance(cur: int, others: list[int], reverse: bool = False):
        others = others[::-1] if reverse else others
        observables = list(itertools.takewhile(lambda x: x < cur, others))
        is_all_observable = len(others) == len(observables)
        return len(observables) + (int(not is_all_observable))

    @staticmethod
    def _get_product(items: Iterable[int]):
        res = 1
        for i in items:
            res = res * i
        return res
