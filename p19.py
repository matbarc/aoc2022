import re
from dataclasses import dataclass
from copy import copy
import math

test_input = """Blueprint 1: Each ore robot costs 4 ore. Each clay robot costs 2 ore. Each obsidian robot costs 3 ore and 14 clay. Each geode robot costs 2 ore and 7 obsidian.
Blueprint 2: Each ore robot costs 2 ore. Each clay robot costs 3 ore. Each obsidian robot costs 3 ore and 8 clay. Each geode robot costs 3 ore and 12 obsidian."""


class Blueprint:
    def __init__(self, description: str) -> None:
        self._parse_input(description)
        return

    def _parse_input(self, description: str) -> None:
        pattern = re.compile(
            r"Blueprint (\d{1,2}):.+(\d{1,2}).+?(\d{1,2}).+(\d{1,2}).+?(\d{1,2}) clay.+(\d{1,2}).+?(\d{1,2})"
        )
        if match := re.search(pattern, description):
            (
                id,
                ore,
                clay,
                obsidian_ore,
                obsidian_clay,
                geode_ore,
                geode_obsidian,
            ) = match.groups()

        self.id = int(id)
        self.costs = (
            (int(ore), 0, 0, 0),
            (int(clay), 0, 0, 0),
            (int(obsidian_ore), int(obsidian_clay), 0, 0),
            (int(geode_ore), 0, int(geode_obsidian), 0),
        )
        return


@dataclass
class State:
    time_remaining: int
    balance: tuple[int, int, int, int]
    workers: tuple[int, int, int, int]

    def can_build(self, robot: int, bp: Blueprint, maxs) -> bool:
        maxed = self.workers[robot] >= maxs[robot]
        return not maxed and all(
            map(lambda x: x[0] >= x[1], zip(self.balance, bp.costs[robot]))
        )

    def build(self, robot: int, bp: Blueprint):
        self.balance = tuple(
            [val - mat_price for val, mat_price in zip(self.balance, bp.costs[robot])]
        )
        self.workers = [x if i != robot else x + 1 for i, x in enumerate(self.workers)]
        return

    def undo_build(self, robot: int, bp: Blueprint):
        self.balance = tuple(
            [val + mat_price for val, mat_price in zip(self.balance, bp.costs[robot])]
        )
        self.workers = [x if i != robot else x - 1 for i, x in enumerate(self.workers)]
        return


def main() -> None:
    with open("day19.txt") as fp:
        lines = fp.readlines()
    # lines = test_input.splitlines()

    bps = [Blueprint(desc) for desc in lines]

    balance = (0, 0, 0, 0)
    workers = (1, 0, 0, 0)
    state0 = State(24, balance, workers)
    maxs = [
        (bp.id, find_blueprint_max_recursive(state0, bp, get_bp_max_mats(bp), (), 0))
        for bp in bps
    ]
    print(maxs)
    print(f"answer: {sum([id * val for id, val in maxs])}")

    state0 = State(32, balance, workers)
    maxs2 = [
        find_blueprint_max_recursive(state0, bp, get_bp_max_mats(bp), (), 0)
        for bp in bps[:3]
    ]
    print(maxs2)
    print(f"answer 2: {math.prod(maxs2)}")
    return


def find_blueprint_max_recursive(
    state: State, bp: Blueprint, max_mats, prev_skipped, best_so_far
):
    if state.time_remaining == 1:
        return state.balance[3] + state.workers[3]

    # This branch sucks
    if material_upper_bound(state, 3) < best_so_far:
        return 0

        # Optimistic heuristic - can't build any more geode machines
    if material_upper_bound(state, 2) < max_mats[2]:
        return state.balance[3] + state.workers[3] * state.time_remaining

    next_state = copy(state)
    next_state.time_remaining -= 1
    next_state.balance = update_balance(next_state.balance, next_state.workers)

    # If you can build the damn machine go ahead
    if state.can_build(3, bp, max_mats):
        next_state.build(3, bp)
        return find_blueprint_max_recursive(next_state, bp, max_mats, (), best_so_far)

    robots_available = [i for i in range(3) if state.can_build(i, bp, max_mats)]
    # print(next_state, robots_available)
    best = best_so_far

    for robot in robots_available:
        # Very dumb branch
        if robot in prev_skipped:
            continue

        next_state.build(robot, bp)
        score = find_blueprint_max_recursive(next_state, bp, max_mats, (), best)
        best = max(score, best)
        next_state.undo_build(robot, bp)

    # Doing nothing is pretty bad, leave it last
    score = find_blueprint_max_recursive(
        next_state, bp, max_mats, tuple(robots_available), best
    )
    best = max(score, best)
    return best


def material_upper_bound(state: State, material: int) -> int:
    t = state.time_remaining
    return state.balance[material] + state.workers[material] * t + t * (t - 1) / 2


def get_bp_max_mats(bp: Blueprint):
    max_robots = tuple(
        [max(vals) if i < 3 else 100 for i, vals in enumerate(zip(*bp.costs))]
    )
    return max_robots


def update_balance(balance, workers):
    new_balance = tuple([bal + qty for bal, qty in zip(balance, workers)])
    return new_balance


if __name__ == "__main__":
    main()
