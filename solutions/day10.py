"""
--- Day 10: Cathode-Ray Tube ---
https://adventofcode.com/2022/day/10
"""
from typing import Iterable

from common import BaseSolver


class Solver(BaseSolver):
    def _prepare(self):
        actions = [0 if line.startswith('noop') else int(line.split()[-1]) for line in self.data['input']]
        self.data['actions'] = actions

    def _solve_one(self):
        cycle, strength, x = 1, 0, 1
        for n in self.data['actions']:
            # check current register
            strength = self._update_strength(strength, cycle, x)

            # if noop, just go to next tick
            if n == 0:
                cycle += 1
                continue

            # if addX, check the next tick, jump over it, and update register
            strength = self._update_strength(strength, cycle + 1, x)
            cycle += 2
            x += n

        return strength

    def _solve_two(self):
        cycle, x = 0, 1
        row, crt = "", []
        for n in self.data['actions']:
            # if end of row, append it to crt and reset
            if len(row) >= 40:
                crt.append(row[:40])
                row = row[40:]

            # update sprite and row
            sprite = (x - 1, x, x + 1)
            row = self._update_row(row, sprite, cycle)

            # if noop, go to the next tick
            if n == 0:
                cycle += 1
                continue

            # if addX, update row on the next tick, jump over the next tick, update register
            row = self._update_row(row, sprite, cycle + 1)
            cycle += 2
            x += n
        crt.append(row)

        return '\n' + '\n'.join(crt)

    @staticmethod
    def _update_strength(strength, cycle, x):
        return strength + cycle * x * (cycle % 40 == 20)

    @staticmethod
    def _update_row(row: str, sprite: Iterable[int], cycle: int):
        pixel = '#' if cycle % 40 in sprite else '.'
        return row + pixel
