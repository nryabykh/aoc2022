"""
--- Day 2: Rock Paper Scissors ---
https://adventofcode.com/2022/day/2
"""

from common import BaseSolver


class Solver(BaseSolver):
    def __init__(self, day: int):
        super().__init__(day)
        self.wins = (
            ('rock', 'scissors'),
            ('scissors', 'paper'),
            ('paper', 'rock')
        )
        self.op_turns = {'a': 'rock', 'b': 'paper', 'c': 'scissors'}
        self.scores_turn = {'rock': 1, 'paper': 2, 'scissors': 3}
        self.scores_result = {'lose': 0, 'draw': 3, 'win': 6}

    def _solve(self):
        self.data = [d.lower().split() for d in self.data]
        return self._solve_one(), self._solve_two()

    def _solve_one(self):
        my_turns = {'x': 'rock', 'y': 'paper', 'z': 'scissors'}
        total = 0
        for turn in self.data:
            op, my = turn
            op, my = self.op_turns.get(op), my_turns.get(my)
            result = self._get_results(op, my)
            total += self.scores_turn.get(my) + self.scores_result.get(result)

        return total

    def _solve_two(self):
        targets = {'x': 'lose', 'y': 'draw', 'z': 'win'}
        total = 0
        for turn in self.data:
            op, result = turn
            op, result = self.op_turns.get(op), targets.get(result)
            my = self._get_turn_to_result(op, result)
            total += self.scores_turn.get(my) + self.scores_result.get(result)

        return total

    def _get_results(self, op_turn, my_turn):
        if op_turn == my_turn:
            return 'draw'

        return 'lose' if (op_turn, my_turn) in self.wins else 'win'

    def _get_turn_to_result(self, op_turn, result):
        if result == 'draw':
            return op_turn
        elif result == 'lose':
            return next(my for op, my in self.wins if op == op_turn)
        else:
            return next(my for my, op in self.wins if op == op_turn)
