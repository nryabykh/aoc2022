"""
--- Day 13: Distress Signal ---
https://adventofcode.com/2022/day/13
"""

from common import BaseSolver


class Solver(BaseSolver):
    def _prepare(self):
        data = [[p[1:-1] for p in pack.split('\n')] for pack in self.data['raw'].split('\n\n')]
        unpacked = []
        for left, right in data:
            unpacked.append(
                (*self._single_parse(left), *self._single_parse(right))
            )
        self.data['parsed'] = unpacked
        # for i, u in enumerate(unpacked):
        #     print(f'{i=}', u)

    @staticmethod
    def _single_parse(line):
        lists_dict, lists_cnt = {}, 0
        while '[' in line:
            last_open = line.rfind('[')
            last_close = line.find(']', last_open)
            last_list = line[last_open:last_close + 1]
            ix = f'list{lists_cnt}'
            lists_dict[ix] = last_list[1:-1].split(',')
            line = line.replace(last_list, ix)
            lists_cnt += 1

        return line.split(','), lists_dict

    @staticmethod
    def _check_ints(left: int, right: int):
        # print(f'checking int: {left=}, {right=}')
        return int(left) <= int(right)

    def _check_lists(self, left: list, right: list, lefts_dict: dict, rights_dict: dict) -> int:
        # print(f'checking lists: {left=}, {right=}, {len(left)=}, {len(right)=}')
        min_len = min(len(left), len(right))
        for i in range(min_len):
            left_c, right_c = left[i], right[i]
            res = self._check(left_c, right_c, lefts_dict, rights_dict)
            if res == -1:
                continue
            else:
                return res
        return -1 if len(right) == len(left) else len(right) > len(left)

    def _check(self, left, right, lefts_dict, rights_dict) -> int:
        # print(f'global check: {left=}, {right=}')
        if not left and right:
            return True
        if left and not right:
            return False
        if not left and not right:
            return True
        if left.isdigit() and right.isdigit():
            if int(left) == int(right):
                return -1
            else:
                return int(int(left) < int(right))
        elif left.isdigit():
            return self._check_lists([left], rights_dict.get(right), {}, rights_dict)
        elif right.isdigit():
            return self._check_lists(lefts_dict.get(left), [right], lefts_dict, {})
        else:
            return self._check_lists(lefts_dict.get(left), rights_dict.get(right), lefts_dict, rights_dict)

    def _solve_one(self):
        total = 0
        for i, (left, lefts_dict, right, rights_dict) in enumerate(self.data['parsed']):
            # print(f'=== START PACK {i+1} ===')
            # print(f'=== DATA: {left=}, {right=}, {lefts_dict=}, {rights_dict=}')
            result = bool(self._check_lists(left, right, lefts_dict, rights_dict))
            # print(f'=== FINISH PACK {i+1}, {result=}')
            if result:
                total += i+1
        return total

    def _compare(self, l, ld, r, rd):
        return bool(self._check_lists(l, r, ld, rd))

    def _solve_two(self):
        all_packages = []
        for (left, lefts_dict, right, rights_dict) in self.data['parsed']:
            all_packages.append((left, lefts_dict))
            all_packages.append((right, rights_dict))

        swaps = 1
        while swaps > 0:
            swaps = 0
            for i in range(len(all_packages) - 1):
                left, right = all_packages[i], all_packages[i+1]
                is_ok = self._compare(*left, *right)
                if not is_ok:
                    swaps += 1
                    all_packages[i] = right
                    all_packages[i+1] = left
                    # print(f'swap {left=}, {right=}')
        # print(all_packages)

        # insert [[2]], [[6]]

        line2, d2 = ['list0'], {'list0': ['2']}
        line6, d6 = ['list0'], {'list0': ['6']}

        i2, i6 = 0, 0
        for i, (line, sd) in enumerate(all_packages):
            if self._compare(line, sd, line2, d2):
                i2 = i
            if self._compare(line, sd, line6, d6):
                i6 = i

        return (i2 + 2) * (i6 + 3)
