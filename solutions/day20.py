"""

"""

from common import BaseSolver


class Solver(BaseSolver):
    def _prepare(self):
        arr = list(map(int, self.data['input']))
        self.data['input'] = arr

    def _solve_one(self):
        ixs = {i: (i, v) for i, v in enumerate(self.data['input'])}
        for init in ixs:
            ixs = self._iter(ixs, init)

        final = self.get_results(ixs)
        ix0 = final.index(0)
        result = [final[(ix0 + i) % len(ixs)] for i in [1000, 2000, 3000]]
        return sum(result)

    def _solve_two(self):
        ixs = {i: (i, v*811589153) for i, v in enumerate(self.data['input'])}
        for j in range(10):
            for init in list(ixs.keys()):
                ixs = self._iter(ixs, init)

        final = self.get_results(ixs)
        ix0 = final.index(0)
        result = [final[(ix0 + i) % len(ixs)] for i in [1000, 2000, 3000]]
        return sum(result)

    @staticmethod
    def _iter(ixs: dict, init: int):
        size = len(ixs)
        current_ix, value = ixs[init]
        new_ix = (current_ix + value) % (size - 1)
        ixs[init] = (new_ix, value)
        for init_ix, (cur_ix, v) in ixs.items():
            if init_ix != init:
                if new_ix < current_ix:
                    if new_ix <= cur_ix < current_ix:
                        ixs[init_ix] = cur_ix + 1, v
                if new_ix > current_ix:
                    if current_ix < cur_ix <= new_ix:
                        ixs[init_ix] = cur_ix - 1, v
        return ixs

    @staticmethod
    def get_results(d):
        return [v for _, v in sorted(d.values())]
