"""
--- Day 3: Rucksack Reorganization ---
https://adventofcode.com/2022/day/3
"""

from common import BaseSolver


class Solver(BaseSolver):
    def _prepare(self):
        self.inner['scores'] = (
            {char: idx + 1 for idx, char in enumerate('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ')}
        )

    def _solve_one(self):
        total = 0
        for line in self.data:
            l = len(line)
            first, second = line[:l // 2], line[l // 2:]
            common_char = set(first).intersection(set(second)).pop()
            total += self.inner['scores'][common_char]

        return total

    def _solve_two(self):
        total = 0
        for i in range(len(self.data) // 3):
            start, end = i * 3, (i+1) * 3
            group = self.data[start:end]
            common_char = set.intersection(*(set(r) for r in group)).pop()
            total += self.inner['scores'][common_char]

        return total
