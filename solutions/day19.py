"""
--- Day 19: Not Enough Minerals ---
https://adventofcode.com/2022/day/19
"""

import math
import re

from common import BaseSolver
from collections import deque


class Solver(BaseSolver):
    def _prepare(self):
        re_ore = """Each ore robot costs (\d+) ore"""
        re_clay = """Each clay robot costs (\d+) ore"""
        re_obsidian = """Each obsidian robot costs (\d+) ore and (\d+) clay"""
        re_geode = """Each geode robot costs (\d+) ore and (\d+) obsidian"""

        # (ore, clay, obsidian)
        all_costs = []
        for line in self.data['input']:
            costs = {}
            ore = re.findall(re_ore, line)
            costs['ore'] = dict(ore=int(ore[0]), clay=0, obsidian=0, geode=0)
            clay = re.findall(re_clay, line)
            costs['clay'] = dict(ore=int(clay[0]), clay=0, obsidian=0, geode=0)
            ob_ore, ob_clay = re.findall(re_obsidian, line)[0]
            costs['obsidian'] = dict(ore=int(ob_ore), clay=int(ob_clay), obsidian=0, geode=0)
            g_ore, g_obs = re.findall(re_geode, line)[0]
            costs['geode'] = dict(ore=int(g_ore), clay=0, obsidian=int(g_obs), geode=0)

            all_costs.append(costs)

        self.data['costs'] = all_costs

    def _solve_one(self):
        quantity_level = 0
        for bp, cost in enumerate(self.data['costs'], start=1):
            max_score = self._solve_single_bp(24, cost)
            quantity_level += bp * max_score
        return quantity_level

    def _solve_two(self):
        quantity_level = 1
        for bp, cost in enumerate(self.data['costs'][:3], start=1):
            max_score = self._solve_single_bp(32, cost)
            quantity_level *= max_score
        return quantity_level

    @staticmethod
    def _solve_single_bp(time_init: int, cost: dict):
        keys = ['ore', 'clay', 'obsidian', 'geode']
        cost_list = [list(v.values()) for _, v in cost.items()]

        queue = deque()
        time_left = time_init
        robots, resources = [1, 0, 0, 0], [0, 0, 0, 0]
        actions = []  # (action, action_time)
        score, max_score = 0, 0
        max_costs = [max(c[i] for c in cost_list) for i in (0, 1, 2, 3)]

        queue.append((time_left, robots, resources, actions, score))

        while queue:
            state = queue.pop()
            time_left, robots, resources, actions, score = state
            # print(f'handle queue item {state=}')

            if time_left <= 0:
                if score > max_score:
                    max_score = score
                continue

            # if no geode robots, make rough estimate if we'll create one geode robot per minute
            if robots[-1] == 0:
                potential_g = (time_left - 1) * time_left // 2
                if potential_g <= max_score:
                    continue

            # if no obsidian robots, make rough estimate if we'll create one OR per minute and then 1 GR per minute
            if robots[2] == 0:
                tg = math.ceil((1 + math.sqrt(8 * cost_list[3][2])) / 2)
                potential_g = (time_left - tg - 1) * (time_left - tg) // 2
                if potential_g <= max_score:
                    continue

            # add to queue 'do nothing'
            new_resources = [resources[i] + robots[i] * time_left for i in (0, 1, 2, 3)]
            score = new_resources[-1]
            queue.append(
                (0, robots, new_resources, actions + [('stay', time_left)], score)
            )

            # select robot to build
            for i in (0, 1, 2, 3):
                # continue if number of robots >= max costs of this resource
                if i != 3 and robots[i] >= max_costs[i]:
                    continue

                # no ores after 15th move
                if time_left < time_init - 15 and i == 0:
                    continue

                # no clays after 20th move
                if time_left < time_init - 25 and i == 1:
                    continue

                # check all resources
                time_to_farm = []
                for j in (0, 1, 2):
                    if cost_list[i][j] == 0:
                        time_to_farm.append(0)
                        continue

                    if robots[j] == 0:
                        time_to_farm.append(-1)
                        continue

                    time_to_farm.append(
                        max(
                            0,
                            math.ceil((cost_list[i][j] - resources[j]) / robots[j])
                        )
                    )

                # print(f'robot {i=}, {cost_list[i]=}, {time_to_farm=}')
                if -1 in time_to_farm:
                    continue

                time_to_farm = max(time_to_farm)
                if time_left < time_to_farm + 1:
                    continue

                new_resources = [r + robots[k] * (time_to_farm + 1) - cost_list[i][k] for k, r in enumerate(resources)]
                queue.append(
                    (
                        time_left - time_to_farm - 1,
                        [r + 1 if k == i else r for k, r in enumerate(robots)],
                        new_resources,
                        actions + [(keys[i], 24 - (time_left - time_to_farm) + 1)],
                        new_resources[-1]
                    )
                )
                # print(f'append {queue[-1]}')
        return max_score
