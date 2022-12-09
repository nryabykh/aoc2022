import argparse

from common import get_module

parser = argparse.ArgumentParser()
parser.add_argument('-d', '--day', type=int, help='Number of day (from 1 to 25)')
parser.add_argument('-i', '--input', type=str, help='Relative path to custom input file')
parser.add_argument('-t', '--test', action='store_true', help='Use test data')


def main(_day: int, _test: bool, _file: str):
    cls = get_module(_day)
    print(
        cls(_day).solve(_file, _test)
    )


if __name__ == "__main__":
    args = parser.parse_args()
    if args.day is None:
        print('No day specified, run the 1st day puzzle as example...')

    day = args.day if args.day is not None else 1
    main(day, args.test, args.input)
