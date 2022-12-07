"""
--- Day 7: No Space Left On Device ---
https://adventofcode.com/2022/day/7
"""

from dataclasses import dataclass
from typing import Optional

from common import BaseSolver

PART_ONE_SIZE_LIMIT = 100000
TOTAL_DISK_SPACE = 70000000
NEED_UNUSED_SPACE = 30000000


@dataclass
class Item:
    name: str
    size: Optional[int]


class Solver(BaseSolver):
    def _prepare(self):
        self.data['dirs'] = self._create_fs_tree()
        self.data['sizes'] = self._get_dir_sizes()

    def _create_fs_tree(self):
        dirs, current_dir_path = {}, []
        for cmd in self.data['input']:
            if cmd.startswith('$'):
                cmd, arg, *others = (cmd[2:] + " _").split()
                if cmd == 'cd':
                    if arg == '..':
                        _ = current_dir_path.pop()
                    else:
                        current_dir_path.append(arg)

                    path = '/'.join(current_dir_path)
                    if path not in dirs:
                        dirs[path] = []
            else:
                mod, name = cmd.split()
                path_current_dir = '/'.join(current_dir_path)
                path = f'{path_current_dir}/{name}'
                size = None if mod == 'dir' else int(mod)

                dirs[path_current_dir].append(Item(name=path, size=size))

        return dirs

    def _get_dir_sizes(self):
        sizes = {}
        dirs = self.data['dirs']
        while len(sizes) != len(dirs):
            for d in dirs:
                item_sizes = [sizes.get(item.name, item.size) for item in dirs[d]]
                if None not in item_sizes:
                    sizes[d] = sum(item_sizes)

        return sizes

    def _solve_one(self):
        sizes = self.data['sizes']
        return sum(v for k, v in sizes.items() if v <= PART_ONE_SIZE_LIMIT)

    def _solve_two(self):
        sizes = self.data['sizes']
        total_used = sizes['/']
        to_free = NEED_UNUSED_SPACE - (TOTAL_DISK_SPACE - total_used)
        return min(s for _, s in sizes.items() if s > to_free)
