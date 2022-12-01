from pathlib import Path

base_dir = Path(__file__).parent


def _get_filename(task_number: int, is_test: bool = False) -> str:
    return f'{task_number:02}{"_test" if is_test else ""}.txt'


def _read_file(filename: str):
    with open(base_dir / 'input' / filename) as f:
        lines = f.readlines()
        return [line.replace('\n', '') for line in lines]


def get_test_input(task_number: int) -> list[str]:
    return _read_file(_get_filename(task_number, is_test=True))


def get_input(task_number: int) -> list[str]:
    return _read_file(_get_filename(task_number, is_test=False))
