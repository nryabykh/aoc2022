from common import get_input, get_test_input


def solve(is_test: bool):
    data = get_input(1) if not is_test else get_test_input(1)

    carries =[]
    current = 0
    for ix, item in enumerate(data):
        if (item == '') or (ix == len(data)-1):
            carries.append(current)
            current = 0
        else:
            current += int(item)

    # Part one
    print(max(carries))

    # Part two
    print(sum(sorted(carries)[-3:]))
