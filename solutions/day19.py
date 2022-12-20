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
            costs['ore'] = dict(ore=int(ore[0]), clay=0, obsidian=0)
            clay = re.findall(re_clay, line)
            costs['clay'] = dict(ore=int(clay[0]), clay=0, obsidian=0)
            ob_ore, ob_clay = re.findall(re_obsidian, line)[0]
            costs['obsidian'] = dict(ore=int(ob_ore), clay=int(ob_clay), obsidian=0)
            g_ore, g_obs = re.findall(re_geode, line)[0]
            costs['geode'] = dict(ore=int(g_ore), clay=0, obsidian=int(g_obs))

            all_costs.append(costs)

        self.data['costs'] = all_costs

    def _solve_one(self):

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

    def _solve_two(self):
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
