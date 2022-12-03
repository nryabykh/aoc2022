"""
--- Day 2: Rock Paper Scissors ---
https://adventofcode.com/2022/day/2
"""

from common import BaseSolver


class Solver(BaseSolver):
    def _prepare(self):
        self.data = {
            'input': [d.lower().split() for d in self.data['input']],
            'wins': (
                ('rock', 'scissors'),
                ('scissors', 'paper'),
                ('paper', 'rock')),
            'op_turns': {'a': 'rock', 'b': 'paper', 'c': 'scissors'},
            'scores_turn': {'rock': 1, 'paper': 2, 'scissors': 3},
            'scores_result': {'lose': 0, 'draw': 3, 'win': 6}
        }

    def _solve_one(self):
        my_turns = {'x': 'rock', 'y': 'paper', 'z': 'scissors'}
        total = 0
        for turn in self.data['input']:
            op, my = turn
            op, my = self.data['op_turns'].get(op), my_turns.get(my)
            result = self._get_results(op, my)
            total += self.data['scores_turn'].get(my) + self.data['scores_result'].get(result)

        return total

    def _solve_two(self):
        targets = {'x': 'lose', 'y': 'draw', 'z': 'win'}
        total = 0
        for turn in self.data['input']:
            op, result = turn
            op, result = self.data['op_turns'].get(op), targets.get(result)
            my = self._get_turn_to_result(op, result)
            total += self.data['scores_turn'].get(my) + self.data['scores_result'].get(result)

        return total

    def _get_results(self, op_turn, my_turn):
        if op_turn == my_turn:
            return 'draw'

        return 'lose' if (op_turn, my_turn) in self.data['wins'] else 'win'

    def _get_turn_to_result(self, op_turn, result):
        if result == 'draw':
            return op_turn
        elif result == 'lose':
            return next(my for op, my in self.data['wins'] if op == op_turn)
        else:
            return next(my for my, op in self.data['wins'] if op == op_turn)
