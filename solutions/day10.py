"""
--- Day 10: Cathode-Ray Tube ---
https://adventofcode.com/2022/day/10
"""

from common import BaseSolver


class Solver(BaseSolver):
    def _prepare(self):
        actions = [0 if line.startswith('noop') else int(line.split()[-1]) for line in self.data['input']]
        self.data['actions'] = actions

    def _solve_one(self):
        cycle, strength, x = 1, 0, 1
        for n in self.data['actions']:
            strength = self._update_strength(strength, cycle, x)

            if n == 0:
                cycle += 1
                continue

            strength = self._update_strength(strength, cycle + 1, x)
            cycle += 2
            x += n

        return strength

    def _solve_two(self):
        cycle, x = 0, 1
        row, crt = "", []
        for n in self.data['actions']:
            if len(row) >= 40:
                crt.append(row[:40])
                row = row[40:]

            sprite = (x - 1, x, x + 1)
            pixel = '#' if cycle % 40 in sprite else '.'
            row += pixel

            if n == 0:
                cycle += 1
                continue

            pixel = '#' if (cycle + 1) % 40 in sprite else '.'
            row += pixel
            cycle += 2
            x += n
        crt.append(row)

        crt = '\n' + '\n'.join(crt)
        return crt

    @staticmethod
    def _update_strength(strength, cycle, x):
        return strength + cycle * x * (cycle % 40 == 20)
