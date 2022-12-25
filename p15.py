import re
import time

test_input = """Sensor at x=2, y=18: closest beacon is at x=-2, y=15
Sensor at x=9, y=16: closest beacon is at x=10, y=16
Sensor at x=13, y=2: closest beacon is at x=15, y=3
Sensor at x=12, y=14: closest beacon is at x=10, y=16
Sensor at x=10, y=20: closest beacon is at x=10, y=16
Sensor at x=14, y=17: closest beacon is at x=10, y=16
Sensor at x=8, y=7: closest beacon is at x=2, y=10
Sensor at x=2, y=0: closest beacon is at x=2, y=10
Sensor at x=0, y=11: closest beacon is at x=2, y=10
Sensor at x=20, y=14: closest beacon is at x=25, y=17
Sensor at x=17, y=20: closest beacon is at x=21, y=22
Sensor at x=16, y=7: closest beacon is at x=15, y=3
Sensor at x=14, y=3: closest beacon is at x=15, y=3
Sensor at x=20, y=1: closest beacon is at x=15, y=3"""


def manhattan_dist(p1: (int, int), p2: (int, int)) -> int:
    dx = abs(p1[0] - p2[0])
    dy = abs(p1[1] - p2[1])
    return dx + dy


class Sensor:
    def __init__(self, pos: (int, int), closest_beacon: (int, int)):
        self.pos = pos
        self.closest_beacon = closest_beacon
        return

    def __repr__(self) -> str:
        return f"sensor: {self.pos} / beacon: {self.closest_beacon}"


def main() -> None:
    with open("day15.txt") as fp:
        lines = fp.readlines()

    # lines = test_input.splitlines()

    LIMIT = 4_000_000

    sensors = sorted([parse_sensor(line) for line in lines], key=lambda x: x.pos[0])
    # sensors_pos = [s.pos for s in sensors]
    beacons = set(sensor.closest_beacon for sensor in sensors)
    dz_by_line = [[] for i in range(LIMIT + 1)]

    for sensor in sensors:
        limit = manhattan_dist(sensor.pos, sensor.closest_beacon)
        for dy in range(-limit, limit + 1):
            dx = limit - abs(dy)
            dz_range = (max(sensor.pos[0] - dx, 0), min(sensor.pos[0] + dx, LIMIT))
            if 0 <= (y := sensor.pos[1] + dy) <= LIMIT:
                dz_by_line[y].append(dz_range)

    for (x, y) in beacons:
        if 0 <= x <= LIMIT and 0 <= y <= LIMIT:
            dz_by_line[y].append((x, x))

    for y, line in enumerate(dz_by_line):
        line.sort()
        line = agg_line_ranges(line)
        if len(line) > 1:
            r1, r2 = line
            x = r2[0] + 1
            print(f"frequency: {x * 4_000_000 + y}")
    return


def agg_line_ranges(line: list[(int, int)]) -> list[(int, int)]:
    if len(line) < 2:
        return line

    r1, r2, *rest = line
    agg = agg_ranges(r1, r2)
    if len(agg) == 1:
        return agg_line_ranges([*agg, *rest])
    return [agg[0], *agg_line_ranges([agg[1], *rest])]


def agg_ranges(r1: list[(int, int)], r2: list[(int, int)]) -> list[(int, int)]:
    lower, higher = sorted([r1, r2])
    min1, max1 = lower
    min2, max2 = higher

    if min2 >= min1 and max2 <= max1:
        return [lower]

    elif min2 <= max1 + 1:
        return [(min1, max2)]

    return [lower, higher]


def parse_sensor(line: str) -> Sensor:
    pattern = re.compile(r"Sensor at x=([-\d]+), y=([-\d]+): .+ x=([-\d]+), y=([-\d]+)")
    match = pattern.search(line)
    if match:
        x, y, bx, by = [int(val) for val in match.groups()]
        return Sensor((x, y), (bx, by))
    raise ValueError(f"Invalid input: {line}")


def print_grid(sensors, beacons, deadzone) -> None:
    def get_char(coord: (int, int)) -> str:
        if coord in [s.pos for s in sensors]:
            return "S"
        elif coord in beacons:
            return "B"
        elif coord in deadzone:
            return "#"
        return "."

    final = ""
    for i in range(-2, 23):
        final += f"{i:>2} {''.join([get_char((j,i)) for j in range(-3, 23)])}\n"

    print(final)
    return


if __name__ == "__main__":
    main()
