import sys
from importlib import import_module


def main(args: list[str]):
    tn = args[0]
    if not tn.isdigit():
        return

    tn = int(tn)
    is_test = True if len(args) > 1 and args[1] == 'test' else False

    func = getattr(import_module(f"solutions.task{tn:02}"), 'solve')
    func(is_test=is_test)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print('AoC solutions')
        exit(0)
    else:
        main(sys.argv[1:])
