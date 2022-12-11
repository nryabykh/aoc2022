"""
--- Day 11: Monkey in the Middle ---
https://adventofcode.com/2022/day/11
"""

from dataclasses import dataclass
from typing import Callable

from common import BaseSolver

Unary = Callable[[int], int]


@dataclass
class Monkey:
    def __init__(
            self,
            wl: list[int],
            divisor: int,
            operator: Unary,
            tester: Unary
    ):
        self.wl = wl
        self.divisor = divisor
        self.operator = lambda x: operator(x)
        self.tester = tester
        self.post_processing: Unary = lambda x: x
        self.inspected: int = 0

    def receive(self, new_wl):
        self.wl.append(new_wl)

    def inspect(self):
        mails = []
        for wl in self.wl:
            new_wl = self.post_processing(self.operator(wl))
            recipient = self.tester(new_wl)
            mails.append((recipient, new_wl))
        self.inspected += len(mails)
        self.wl = []
        return mails


class MonkeyService:
    def __init__(self):
        self.monkeys: list[Monkey] = []

    def register(self, m: Monkey):
        self.monkeys.append(m)

    def get_div_product(self) -> int:
        div = 1
        for mon in self.monkeys:
            div *= mon.divisor
        return div

    def set_post_processing(self, func: Unary):
        for mon in self.monkeys:
            mon.post_processing = func

    def serve_all(self):
        for mon in self.monkeys:
            mails = mon.inspect()
            for recipient, wl in mails:
                self.send(recipient, wl)

    def play_rounds(self, n: int):
        for _ in range(n):
            self.serve_all()

    def send(self, receiver, wl):
        self.monkeys[receiver].receive(wl)


class Solver(BaseSolver):
    def _prepare(self):
        lines = self.data['input']
        self.data['monkeys'] = []

        for i in range((len(lines)+1) // 7):
            start, end = i * 7, i * 7 + 6
            _, items, operation, test, test_true, test_false = lines[start:end]

            wls = list(map(int, items.split('Starting items: ')[-1].split(', ')))
            op_left, operator, op_right = operation.split('Operation: new = ')[-1].split()
            operator = self._get_operator_func(op_left, operator, op_right)
            divisor, tester = self._get_divisor_and_test_func(test, test_true, test_false)
            self.data['monkeys'].append((wls, operator, divisor, tester))

    @staticmethod
    def _get_operator_func(op1: str, mod: str, op2: str) -> Unary:
        if mod == '*':
            if (not op1.isdigit()) and (not op2.isdigit()):
                return lambda x: x * x
            else:
                multiplier = int(op1) if op1.isdigit() else int(op2)
                return lambda x: x * multiplier
        else:
            add = int(op1) if op1.isdigit() else int(op2)
            return lambda x: x + add

    @staticmethod
    def _get_divisor_and_test_func(*args) -> tuple[int, Unary]:
        mod, rec_true, rec_false = (int(s.split()[-1]) for s in args)
        return mod, lambda x: rec_true if x % mod == 0 else rec_false

    def _init_service(self) -> MonkeyService:
        service = MonkeyService()
        for wls, operator, divisor, tester in self.data['monkeys']:
            service.register(Monkey(
                wl=wls.copy(), operator=operator, divisor=divisor, tester=tester
            ))
        return service

    def _solve_one(self):
        service = self._init_service()
        service.set_post_processing(lambda x: x // 3)
        service.play_rounds(20)
        ins1, ins2, *_ = sorted((m.inspected for m in service.monkeys), reverse=True)
        return ins1 * ins2

    def _solve_two(self):
        service = self._init_service()
        common_div = service.get_div_product()
        service.set_post_processing(lambda x: x % common_div)
        service.play_rounds(10000)
        ins1, ins2, *_ = sorted((m.inspected for m in service.monkeys), reverse=True)
        return ins1 * ins2
