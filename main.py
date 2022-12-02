import argparse
from importlib import import_module


parser = argparse.ArgumentParser()
parser.add_argument('-d', '--day', type=int)
parser.add_argument('-t', '--test', action='store_true')


def main(_day: int, _test: bool):
    func = getattr(import_module(f"solutions.day{_day:02}"), 'solve')
    func(is_test=_test)


if __name__ == "__main__":
    args = parser.parse_args()
    if args.day is None:
        print('No day specified, run the 1st day puzzle as example...')

    day = args.day if args.day is not None else 1
    main(day, args.test)
