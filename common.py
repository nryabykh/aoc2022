import time
from abc import ABC, abstractmethod
from dataclasses import dataclass
from importlib import import_module
from pathlib import Path
from typing import Any


class Reader:
    def __init__(self, day: int, is_test: bool, input_path: str = None):
        self.day = day
        self.test = is_test
        self.base_dir = Path(__file__).parent
        self.filename = f'{day:02}{"_test" if is_test else ""}.txt'
        self.path = (self.base_dir / 'input' / self.filename) if (input_path is None) else Path(input_path)

    def get_lines(self):
        return self.get_data().splitlines()

    def get_data(self):
        with open(self.path) as f:
            return f.read()

    def path_exists(self) -> bool:
        return self.path.exists()


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

    def solve(self, input_path: str = None, test: bool = False, part: int = None) -> Answer:
        reader = Reader(day=self.day, is_test=test, input_path=input_path)
        self.data['is_test'] = test
        self.data['input'] = reader.get_lines()
        self.data['raw'] = reader.get_data()
        self._prepare()
        one, two = self._solve(part)
        return Answer(self.day, one, two)

    def _prepare(self):
        pass

    def _solve(self, part: int):
        start_time = time.time()
        ans_one = self._solve_one() if part == 1 or part is None else None
        first_time = time.time()
        print(f' --- Elapsed time for part one = {first_time - start_time:.2f}s ---')
        ans_two = self._solve_two() if part == 2 or part is None else None
        print(f' --- Elapsed time for part two = {time.time() - first_time:.2f}s ---')
        return ans_one, ans_two

    @abstractmethod
    def _solve_one(self):
        ...

    @abstractmethod
    def _solve_two(self):
        ...


def get_module(_day: int):
    return getattr(import_module(f"solutions.day{_day:02}"), 'Solver')
