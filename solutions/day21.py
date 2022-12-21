"""
--- Day 21: Monkey Math ---
https://adventofcode.com/2022/day/21
"""

from typing import Callable

from common import BaseSolver


class Solver(BaseSolver):
    def _prepare(self):
        values = {}
        expressions = {}
        for line in self.data['input']:
            key, expr = line.split(': ', 1)
            if expr.isdigit():
                values[key] = int(expr)
            else:
                left, op, right = expr.split()
                expressions[key] = (left, right, op, self._get_func(op))
        self.data['values'] = values
        self.data['expressions'] = expressions

    @staticmethod
    def _get_func(op: str) -> Callable[[int, int], int]:
        if op == '+':
            return lambda x, y: x + y
        elif op == '-':
            return lambda x, y: x - y
        elif op == '*':
            return lambda x, y: x * y
        elif op == '/':
            return lambda x, y: x // y
        else:
            return lambda x, y: int(x == y)

    def _solve_one(self):
        values = self.data['values'].copy()
        expr = self.data['expressions']
        return self._calculate_token(values, expr, 'root')

    def _solve_two(self):
        values = self.data['values']
        expr = self.data['expressions']
        left, right, _, _ = expr['root']
        expr['root'] = (left, right, '=', self._get_func('='))

        token = 'root'
        reverse_expr, reverse_values = {}, {'one': 1}
        while token != 'humn':
            left, right, op_str, op = expr[token]
            calc_left, calc_right = [
                self._calculate_token(self._pop_from_dict(values.copy(), 'humn'), expr, x)
                for x in [left, right]
            ]
            reversed_ops = {
                    '+': '--',
                    '-': '+-',
                    '*': '//',
                    '/': '*/',
                    '=': '**'
                }
            if calc_left is None:
                reverse_values[right] = calc_right
                reverse_expr[left] = (
                    token if op_str != '=' else 'one',
                    right,
                    reversed_ops[op_str][0],
                    self._get_func(reversed_ops[op_str][0])
                )
                token = left
            else:
                reverse_values[left] = calc_left
                leftn, rightn = (token, left) if op_str in '+*' else (left, token)
                reverse_expr[right] = (
                    leftn if op_str != '=' else 'one',
                    rightn,
                    reversed_ops[op_str][1],
                    self._get_func(reversed_ops[op_str][1])
                )
                token = right

        return self._calculate_token(reverse_values, reverse_expr, 'humn')

    @staticmethod
    def _calculate_token(values, expr, token):
        while token not in values:
            values_prev_len = len(values)
            for key, (left, right, op_str, op) in expr.items():
                if left in values and right in values:
                    values[key] = op(values[left], values[right])
            if len(values) == values_prev_len:
                return None
        return values[token]

    @staticmethod
    def _pop_from_dict(d, key):
        d.pop(key, None)
        return d
