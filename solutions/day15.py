"""

"""
import re
from dataclasses import dataclass

from common import BaseSolver


@dataclass
class Sensor:
    # sensor
    x: int
    y: int

    # nearest beacon
    xb: int
    yb: int

    @property
    def distance(self):
        return abs(self.x - self.xb) + abs(self.y - self.yb)

    def get_distance(self, xp: int, yp: int):
        return abs(self.x - xp) + abs(self.y - yp)

    def is_point_under_this(self, xp: int, yp: int):
        return self.get_distance(xp, yp) <= self.distance

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y


class Solver(BaseSolver):
    def _prepare(self):
        sensors = []
        for row in self.data['input']:
            rx = re.findall("""Sensor at x=(\-?\d+), y=(\-?\d+): closest beacon is at x=(\-?\d+), y=(\-?\d+)""", row)
            sensors.append(Sensor(*list(map(int, rx[0]))))
        self.data['sensors'] = sensors

    def _solve_one(self):
        checked = set()
        y_target = 10 if self.data['is_test'] else 2000000
        sensors = set((s.x, s.y) for s in self.data['sensors'])
        beacons = set((s.xb, s.yb) for s in self.data['sensors'])
        for s in self.data['sensors']:
            # === 85 374 373 171 856 iterations - so slow ===
            # for x in range(s.x - s.distance, s.x + s.distance + 1):
            #     for y in range(s.y - s.distance, s.y + s.distance + 1):
            #         if s.get_distance(x, y) <= s.distance:
            #             if (x, y) not in sensors and (x, y) not in beacons:
            #                 checked.add((x, y))

            if (y_target < s.y - s.distance) or (y_target > s.y + s.distance):
                continue
            dist_to_target = abs(s.y - y_target)
            dist_from_edge = s.distance - dist_to_target
            for x in range(s.x - dist_from_edge, s.x + dist_from_edge + 1):
                if (x, y_target) not in sensors and (x, y_target) not in beacons:
                    checked.add(x)

        return len(checked)

    def _solve_two(self):
        min_coord, max_coord = 0, 20 if self.data['is_test'] else 4000000
        x_min, x_max = min_coord, max_coord
        y_min, y_max = min_coord, max_coord
        for s in self.data['sensors']:
            for x in range(max(x_min, s.x - s.distance - 1), min(x_max, s.x + s.distance + 2)):
                dx = abs(s.x - x)
                dy = s.distance + 1 - dx
                for y in (s.y - dy, s.y + dy):
                    if (y_min <= y <= y_max) and not self._is_under_sensor(x, y, exclude_sensor=s):
                        return x*4000000 + y

    def _is_under_sensor(self, x: int, y: int, exclude_sensor: Sensor):
        return any(
            s.is_point_under_this(x, y) for s in self.data['sensors'] if s != exclude_sensor
        )
