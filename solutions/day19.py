"""

"""
import math
import re
from dataclasses import dataclass

from common import BaseSolver
from collections import deque

@dataclass
class Step:
    tick: int
    created_robot: str
    robots: dict  # after
    resources: dict  # after
    steps: set[int]
    stepsr: str

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
        keys = ['ore', 'clay', 'obsidian', 'geode']

        quantity_level = 0
        for bp, cost in enumerate(self.data['costs'], start=1):
            cost_list = []
            for robot, v in cost.items():
                cost_list.append(list(v.values()))

            queue = deque()
            time_left = 24
            robots = [1, 0, 0, 0]
            resources = [0, 0, 0, 0]
            actions = []  # (action, action_time)
            score = 0
            max_score = 0
            best_path = []
            max_costs = [max(c[i] for c in cost_list)for i in (0, 1, 2, 3)]

            queue.append((time_left, robots, resources, actions, score))

            moves = 0
            # while queue and moves < 20:
            while queue:
                moves += 1
                # state at the beginning of step
                state = queue.pop()
                time_left, robots, resources, actions, score = state
                # print(f'handle queue item {state=}')

                if time_left <= 0:
                    if score > max_score:
                        max_score = score
                        best_path = actions
                    continue

                if robots[-1] == 0:
                    potential_g = (time_left - 1) * time_left // 2
                    if potential_g <= max_score:
                        continue

                # do nothing
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

            print(bp, max_score, best_path)
            quantity_level += bp * max_score
        return quantity_level

    def _solve_two(self):
        keys = ['ore', 'clay', 'obsidian', 'geode']

        quantity_level = 1
        init_time = 32
        for bp, cost in enumerate(self.data['costs'][:3], start=1):
            cost_list = []
            for robot, v in cost.items():
                cost_list.append(list(v.values()))

            queue = deque()
            time_left = init_time
            robots = [1, 0, 0, 0]
            resources = [0, 0, 0, 0]
            actions = []  # (action, action_time)
            score = 0
            max_score = 0
            best_path = []
            max_costs = [max(c[i] for c in cost_list)for i in (0, 1, 2, 3)]

            queue.append((time_left, robots, resources, actions, score))

            moves = 0
            # while queue and moves < 20:
            while queue:
                moves += 1
                # state at the beginning of step
                state = queue.pop()
                time_left, robots, resources, actions, score = state
                # print(f'handle queue item {state=}')

                if time_left <= 0:
                    if score > max_score:
                        max_score = score
                        best_path = actions
                    continue

                if robots[-1] == 0:
                    potential_g = (time_left - 1) * time_left // 2
                    if potential_g <= max_score:
                        continue

                if robots[2] == 0:
                    tg = math.ceil((1 + math.sqrt(8 * cost_list[3][2])) / 2)
                    potential_g = (time_left - tg - 1) * (time_left - tg) // 2
                    if potential_g <= max_score:
                        continue

                # do nothing
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
                    if time_left < init_time - 15 and i == 0:
                        continue

                    # no clays after 20th move
                    if time_left < init_time - 25 and i == 1:
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
                            actions + [(keys[i], init_time - (time_left - time_to_farm) + 1)],
                            new_resources[-1]
                        )
                    )
                    # print(f'append {queue[-1]}')

            print(bp, max_score, best_path)
            quantity_level *= max_score
        return quantity_level















    def _solve_one_prev(self):

        actions = ['ore', 'clay', 'obsidian', 'geode'][::-1]

        ql = []
        for ix, costs in enumerate(self.data['costs'][29:], start=1):
        # costs = self.data['costs'][1]
        # print(costs)

            queue = deque()
            queue.append(Step(0, '',
                              robots=dict(ore=1, clay=0, obsidian=0, geode=0),
                              resources=dict(ore=0, clay=0, obsidian=0, geode=0),
                              steps=set(), stepsr=''))

            geodes = set()
            gg = set()
            maxes = {k: max(v[k] for _, v in costs.items()) for k in ['ore', 'clay', 'obsidian']}
            # print(maxes)

            while queue:
                state: Step = queue.pop()

                if state.tick >= 24:
                    # if state.resources['geode'] == 9:
                    #     print(f'add geodes: {state.resources["geode"]}, {state.stepsr=}')
                    geodes.add(state.resources['geode'])
                    gg.add((state.resources['geode'], state.stepsr, state.robots.values(), state.resources.values()))

                    continue

                # возможные действия: стоим до конца, 2) строим робота через n тиков

                # stay
                ticks_left = 24 - state.tick
                new_res = {k: v + ticks_left * state.robots[k] for k, v in state.resources.items()}
                queue.append(
                    Step(tick=24, created_robot='', robots=state.robots, resources=new_res, steps=state.steps, stepsr=state.stepsr)
                )

                potential_geodes = state.robots['geode'] * ticks_left + (ticks_left - 1) * ticks_left // 2
                if potential_geodes <= (max(geodes) if geodes else 0):
                    continue

                exclude = ['ore', 'clay'] if state.tick > 25 else []
                for k in ['ore', 'clay', 'obsidian']:
                    if state.robots[k] >= maxes[k]:
                        exclude.append(k)

                # выбираем робота для постройки
                for next_robot in [a for a in actions if a not in exclude]:
                    # проверяем, есть ли робота для сбора ресурсов для постройки выбранного

                    # current robots
                    current_robots = [kr for kr, vr in state.robots.items() if vr > 0]
                    next_robots_costs = costs[next_robot]

                    if any(nk not in current_robots for nk, nv in next_robots_costs.items() if nv > 0):
                        continue

                    ticks_needed = max(
                        0 if state.resources[nk] >= nv else math.ceil((nv - state.resources[nk]) / state.robots[nk])
                        for nk, nv in next_robots_costs.items()
                        if nv > 0
                    )

                    # if state.tick + ticks_needed + 1 in state.steps:
                    #     continue

                    if state.tick + ticks_needed >= 23:
                        continue

                    new_resources = {
                        kr: vr + state.robots[kr] * (ticks_needed + 1) - next_robots_costs.get(kr, 0)
                        for kr, vr in state.resources.items()}

                    new_robots = {kr: vr + 1 if kr == next_robot else vr for kr, vr in state.robots.items()}

                    dd = {'ore': 'o', 'clay': 'c', 'obsidian': 'Ob', 'geode': 'g'}
                    new_steps = state.steps.copy()
                    new_steps.add(state.tick + ticks_needed + 1)
                    new_step = Step(
                        state.tick + ticks_needed + 1,
                        created_robot=next_robot,
                        robots=new_robots,
                        resources=new_resources,
                        steps=new_steps,
                        stepsr=state.stepsr + f' {state.tick + ticks_needed}{dd[next_robot]}')

                    # if next_robot == 'geode' and state.tick + ticks_needed == 18:
                    #     print(f'Tick {state.tick}, {ticks_needed=}, {state.resources=}, {next_robot=}, {new_step=}')
                    # if new_resources['geode'] > 3:
                    #     print(f'{state=}, {next_robot=}, {new_step=}')
                    queue.append(new_step)

                # print(f'{queue=}')
            max_geodes = max(geodes) if geodes else 0
            print(f'{ix=}, {max_geodes=}')
            ql.append(ix * max_geodes)

        print(ql)

        return sum(ql)


    def _as_str(self, d: dict):
        return '-'.join(str(v) for _, v in d.items())

    def _solve_two_prev(self):
        actions = ['ore', 'clay', 'obsidian', 'geode'][::-1]

        ql = []
        for ix, costs in enumerate(self.data['costs'][:3], start=1):
            # costs = self.data['costs'][1]
            # print(costs)

            queue = deque()
            queue.append(Step(0, '',
                              robots=dict(ore=1, clay=0, obsidian=0, geode=0),
                              resources=dict(ore=0, clay=0, obsidian=0, geode=0),
                              steps=set(), stepsr=''))

            geodes = set()
            gg = set()
            maxes = {k: max(v[k] for _, v in costs.items()) for k in ['ore', 'clay', 'obsidian']}
            # print(maxes)

            while queue:
                state: Step = queue.pop()

                if state.tick >= 32:
                    # if state.resources['geode'] == 9:
                    #     print(f'add geodes: {state.resources["geode"]}, {state.stepsr=}')
                    geodes.add(state.resources['geode'])
                    gg.add((state.resources['geode'], state.stepsr, state.robots.values(), state.resources.values()))

                    continue

                # возможные действия: стоим до конца, 2) строим робота через n тиков

                # stay
                ticks_left = 32 - state.tick
                new_res = {k: v + ticks_left * state.robots[k] for k, v in state.resources.items()}
                queue.append(
                    Step(tick=32, created_robot='', robots=state.robots, resources=new_res, steps=state.steps,
                         stepsr=state.stepsr)
                )

                potential_geodes = state.robots['geode'] * ticks_left + (ticks_left - 1) * ticks_left // 2
                if potential_geodes <= (max(geodes) if geodes else 0):
                    continue

                exclude = ['ore', 'clay'] if state.tick > 33 else []
                for k in ['ore', 'clay', 'obsidian']:
                    if state.robots[k] >= maxes[k]:
                        exclude.append(k)

                # выбираем робота для постройки
                for next_robot in [a for a in actions if a not in exclude]:
                    # проверяем, есть ли робота для сбора ресурсов для постройки выбранного

                    # current robots
                    current_robots = [kr for kr, vr in state.robots.items() if vr > 0]
                    next_robots_costs = costs[next_robot]

                    if any(nk not in current_robots for nk, nv in next_robots_costs.items() if nv > 0):
                        continue

                    ticks_needed = max(
                        0 if state.resources[nk] >= nv else math.ceil((nv - state.resources[nk]) / state.robots[nk])
                        for nk, nv in next_robots_costs.items()
                        if nv > 0
                    )

                    # if state.tick + ticks_needed + 1 in state.steps:
                    #     continue

                    if state.tick + ticks_needed >= 31:
                        continue

                    new_resources = {
                        kr: vr + state.robots[kr] * (ticks_needed + 1) - next_robots_costs.get(kr, 0)
                        for kr, vr in state.resources.items()}

                    new_robots = {kr: vr + 1 if kr == next_robot else vr for kr, vr in state.robots.items()}

                    dd = {'ore': 'o', 'clay': 'c', 'obsidian': 'Ob', 'geode': 'g'}
                    new_steps = state.steps.copy()
                    new_steps.add(state.tick + ticks_needed + 1)
                    new_step = Step(
                        state.tick + ticks_needed + 1,
                        created_robot=next_robot,
                        robots=new_robots,
                        resources=new_resources,
                        steps=new_steps,
                        stepsr=state.stepsr + f' {state.tick + ticks_needed}{dd[next_robot]}')

                    # if next_robot == 'geode' and state.tick + ticks_needed == 18:
                    #     print(f'Tick {state.tick}, {ticks_needed=}, {state.resources=}, {next_robot=}, {new_step=}')
                    # if new_resources['geode'] > 3:
                    #     print(f'{state=}, {next_robot=}, {new_step=}')
                    queue.append(new_step)

                # print(f'{queue=}')
            max_geodes = max(geodes) if geodes else 0
            print(f'{ix=}, {max_geodes=}')
            ql.append(max_geodes)

        print(ql)

        return ql[0] * ql[1] * ql[2]
