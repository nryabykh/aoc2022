"""

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

    def _solve_one(self):
        figures = list(self.data['figures'].keys())
        jets = self.data['input'][0]

        rock_cnt, tick, max_y = 0, 0, 0
        rocks = set()
        moves = []
        while rock_cnt < 2022:
            fig = figures[rock_cnt % 5]
            coords = [(x + 2, y + max_y + 4) for (x, y) in self.data['figures'][fig]]
            # print(f'{fig=} init {coords=}')
            collision = False
            fig_jets = ""
            while not collision:
                jet = jets[tick % len(jets)]
                # print(jet)

                coords = self._move_jet(coords, jet, rocks)
                collision, coords = self._move_down(coords, rocks)
                # print(fig, coords)
                tick += 1
                fig_jets += jet
            for c in coords:
                rocks.add(c)
            # print(f'{sorted(rocks)=}')
            rock_cnt += 1
            max_y = max(max_y, max(y for x, y in coords))
            # print(rock_cnt, max_y)
            max_row_len = sum(1 for (x, y) in rocks if y == max_y)
            moves.append((fig, fig_jets, max_row_len, max_y))

        for m in moves:
            print(m)

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

    def _solve_two(self):
        figures = list(self.data['figures'].keys())
        jets = self.data['input'][0]
        print(len(jets))


        # dH = max(0, y[fig] - (len(jet) - 4))