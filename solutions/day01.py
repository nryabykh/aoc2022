from common import get_data


def solve(is_test: bool):
    data = get_data(day=1, is_test=is_test)

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
