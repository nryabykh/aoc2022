"""
--- Day 5: Supply Stacks ---
https://adventofcode.com/2022/day/5
"""
import re

from common import BaseSolver


class Solver(BaseSolver):
    def _prepare(self):
        data = self.data['input']
        sep_ix = data.index("")
        data_stacks, data_moves = data[:sep_ix], data[sep_ix+1:]

        stacks = {}
        for line in data_stacks[:-1]:
            for i in range(len(line) // 4 + 1):
                crate = line[i*4 + 1]
                if crate != ' ':
                    if i+1 not in stacks:
                        stacks[i+1] = [crate]
                    else:
                        stacks[i+1].append(crate)

        self.data['stacks'] = stacks
        self.data['moves'] = data_moves

    def _solve_one(self):
        return self._make_moves(mover_type='single')

    def _solve_two(self):
        return self._make_moves(mover_type='multiple')

    def _make_moves(self, mover_type: str) -> str:
        stacks = self.data['stacks'].copy()
        for move in self.data['moves']:
            move = self._parse_move(move)
            stacks = self._make_move(stacks, move, mover_type)

        return self._get_upper_items(stacks)

    @staticmethod
    def _parse_move(move: str) -> list[int]:
        pattern = "move (\d+) from (\d+) to (\d+)"
        found = re.search(pattern, move)
        return list(map(int, found.groups()))

    @staticmethod
    def _make_move(stacks: dict, move: list[int], mover_type: str) -> dict:
        number, sender, receiver = move
        sender_stack = stacks[sender]
        to_send = sender_stack[:number]
        stacks[sender] = (
            sender_stack[number:]
            if len(sender_stack) > number
            else []
        )
        to_send_order = to_send if mover_type == 'multiple' else to_send[::-1]
        stacks[receiver] = to_send_order + stacks[receiver]
        return stacks

    @staticmethod
    def _get_upper_items(stacks: dict) -> str:
        ups = sorted((k, v[0]) for k, v in stacks.items())
        return ''.join([v for _, v in ups])
