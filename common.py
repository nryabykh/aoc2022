from dataclasses import dataclass
from pathlib import Path
from abc import ABC, abstractmethod
from typing import Any


class Reader:
    def __init__(self, day: int, is_test: bool):
        self.day = day
        self.test = is_test
        self.base_dir = Path(__file__).parent
        self.filename = f'{day:02}{"_test" if is_test else ""}.txt'

    def get_lines(self):
        return self.get_data().splitlines()

    def get_data(self):
        with open(self.base_dir / 'input' / self.filename) as f:
            return f.read()


@dataclass
class Answer:
    """
    Dataclass for answers. Contains answers both of the first and of the second parts
    """

    day: int
    one: Any
    two: Any

    def __repr__(self):
        return f'Answers for day {self.day}: part one = {self.one}, part two = {self.two}'


class BaseSolver(ABC):
    """
    Abstract class for solutions
    """

    def __init__(self, day: int):
        self.day = day
        self.data = {}

    def solve(self, test: bool) -> Answer:
        self.data['input'] = Reader(day=self.day, is_test=test).get_lines()
        self._prepare()
        one, two = self._solve()
        return Answer(self.day, one, two)

    def _prepare(self):
        pass

    def _solve(self):
        return self._solve_one(), self._solve_two()

    @abstractmethod
    def _solve_one(self):
        ...

    @abstractmethod
    def _solve_two(self):
        ...
