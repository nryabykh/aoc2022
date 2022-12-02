from pathlib import Path

base_dir = Path(__file__).parent


def _get_filename(day: int, is_test: bool = False) -> str:
    return f'{day:02}{"_test" if is_test else ""}.txt'


def _read_file(filename: str):
    with open(base_dir / 'input' / filename) as f:
        lines = f.readlines()
        return [line.replace('\n', '') for line in lines]


def get_test_input(day: int) -> list[str]:
    return _read_file(_get_filename(day, is_test=True))


def get_input(day: int) -> list[str]:
    return _read_file(_get_filename(day, is_test=False))


def get_data(day: int, is_test: bool) -> list[str]:
    return get_input(day) if not is_test else get_test_input(day)
