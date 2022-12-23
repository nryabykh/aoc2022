"""
--- Day 23: Unstable Diffusion ---
https://adventofcode.com/2022/day/23
"""

from common import BaseSolver


class Solver(BaseSolver):
    def _prepare(self):
        lines = self.data['input']
        elves = set()
        for y in range(len(lines)):
            for x in range(len(lines[0])):
                if lines[y][x] == '#':
                    elves.add((x, y))
        self.data['elves'] = elves

    def _solve_one(self):
        elves = self.data['elves'].copy()
        round_limit = 10
        round_number, moves = 0, 1
        while moves > 0 and round_number < round_limit:
            moves, elves = self._play_round(elves, round_number)
            round_number += 1
        return self._calc_score(elves)

    def _solve_two(self):
        elves = self.data['elves'].copy()
        round_number, moves = 0, 1
        while moves > 0:
            moves, elves = self._play_round(elves, round_number)
            round_number += 1
        return round_number

    def _play_round(self, elves: set, round_number: int):
        keys = 'nswe'
        moves, proposals, stays = 0, {}, []

        for x, y in elves:
            adj_by_dir = self._get_neighbors(x, y)
            all_adj = [*adj_by_dir['n'], *adj_by_dir['s'], *adj_by_dir['e'], *adj_by_dir['w']]
            if all(a not in elves for a in all_adj):
                stays.append((x, y))
                continue

            # choose proposals
            for k in (0, 1, 2, 3):
                ix = (round_number + k) % 4
                adj_dir = adj_by_dir[keys[ix]]
                move = adj_dir[1]
                if all(a not in elves for a in adj_dir):
                    if move in proposals:
                        proposals[move].append((x, y))
                    else:
                        proposals[move] = [(x, y)]
                    break
            else:
                stays.append((x, y))

        # make moves
        new_elves = []
        for k, vs in proposals.items():
            if len(vs) == 1:
                new_elves.append(k)
                moves += 1
            else:
                new_elves.extend(vs)

        new_elves.extend(stays)
        return moves, set(new_elves)

    @staticmethod
    def _calc_score(elves):
        xs = [x for x, _ in elves]
        ys = [y for _, y in elves]
        return (max(xs) - min(xs) + 1) * (max(ys) - min(ys) + 1) - len(elves)

    @staticmethod
    def _get_neighbors(x, y):
        return {
            'n': [(x - 1, y - 1), (x, y - 1), (x + 1, y - 1)],
            's': [(x - 1, y + 1), (x, y + 1), (x + 1, y + 1)],
            'w': [(x - 1, y - 1), (x - 1, y), (x - 1, y + 1)],
            'e': [(x + 1, y - 1), (x + 1, y), (x + 1, y + 1)],
        }

    @staticmethod
    def _print_map(lines):
        for line in lines:
            print(line)

    @staticmethod
    def _print_elves(elves):
        xs = [x for x, _ in elves]
        ys = [y for _, y in elves]
        for y in range(min(ys), max(ys)):
            row = ''
            for x in range(min(xs), max(xs)):
                row += '#' if (x, y) in elves else '.'
            print(row)
