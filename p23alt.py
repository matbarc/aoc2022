#!/usr/bin/env python3

import pathlib
import sys

from collections import deque, defaultdict
from typing import Generator


def read_positions(file: pathlib.Path) -> set[complex]:
    map = {
        x + y * 1j
        for y, line in enumerate(file.readlines())
        for x in range(len(line))
        if line[x] == "#"
    }
    return map


def simulation(map: set[complex]) -> Generator[set[complex], None, None]:
    dirs = deque(
        [
            (-1 - 1j, -1j, 1 - 1j),
            (-1 + 1j, 1j, 1 + 1j),
            (-1 - 1j, -1, -1 + 1j),
            (1 - 1j, 1, 1 + 1j),
        ]
    )

    while True:
        moves = defaultdict(list)

        for elf in map:
            elf_moves = []
            for left, move, right in dirs:
                if not {elf + left, elf + move, elf + right} & map:
                    elf_moves.append(elf + move)

            if elf_moves and len(elf_moves) < len(dirs):
                moves[elf_moves[0]].append(elf)

        if len(moves) == 0:
            yield map
            return

        for move, elves in moves.items():
            if len(elves) == 1:
                map.remove(elves[0])
                map.add(move)

        yield map

        dirs.rotate(-1)


def bounds(map: set[complex]) -> tuple[int, int, int, int]:
    min_x = int(min(elf.real for elf in map))
    min_y = int(min(elf.imag for elf in map))
    max_x = int(max(elf.real for elf in map))
    max_y = int(max(elf.imag for elf in map))

    return min_x, min_y, max_x, max_y


def display(map: set[complex]) -> str:
    min_x, min_y, max_x, max_y = bounds(map)

    return "\n".join(
        "".join("#" if x + y * 1j in map else "." for x in range(min_x, max_x + 1))
        for y in range(min_y, max_y + 1)
    )


def empty_area(map: set[complex]) -> int:
    min_x, min_y, max_x, max_y = bounds(map)
    return (max_x - min_x + 1) * (max_y - min_y + 1) - len(map)


def run() -> None:
    with open("day23.txt") as fp:
        map = read_positions(fp)

    sim = simulation(map)
    for _ in range(10):
        map = next(sim)

    print(f"Empty area: {empty_area(map)}")

    round = 10 + sum(1 for _ in sim)
    print(f"Final round: {round}")


if __name__ == "__main__":
    run()
    sys.exit(0)
