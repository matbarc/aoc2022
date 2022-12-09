from dataclasses import dataclass, replace
import math
from enum import Enum, auto


@dataclass(frozen=True, repr=True, eq=True)
class Pos:
    x: int
    y: int


class Direction(Enum):
    UP = auto()
    DOWN = auto()
    RIGHT = auto()
    LEFT = auto()


class Simulation:
    def __init__(self) -> None:
        self.origin = Pos(0, 0)
        self.head_pos = Pos(0, 0)
        self.tail_pos = Pos(0, 0)

        self.tail_visited = set()
        return

    def simulate_command(self, command: str) -> None:
        direction, steps = self.parse_command(command)

        while steps > 0:
            self._move_head_one_step(direction)
            steps -= 1
            print(self)

        return

    def _move_head_one_step(self, direction: Direction) -> None:
        if direction == Direction.DOWN:
            self.head_pos = replace(self.head_pos, y=self.head_pos.y - 1)
        elif direction == Direction.UP:
            self.head_pos = replace(self.head_pos, y=self.head_pos.y + 1)
        elif direction == Direction.LEFT:
            self.head_pos = replace(self.head_pos, x=self.head_pos.x - 1)
        elif direction == Direction.RIGHT:
            self.head_pos = replace(self.head_pos, x=self.head_pos.x + 1)
        return

    def _chase_with_tail(self) -> None:
        dx = self.head_pos.x - self.tail_pos.x
        dy = self.head_pos.y - self.tail_pos.y
        distance = math.sqrt(dx**2 + dy**2)

        if distance < math.sqrt(2):
            return

        raise NotImplementedError("Not implemented tail movement")
        return

    @staticmethod
    def parse_command(command: str) -> (str, int):
        direction_str, steps_str = command.split()

        direction_lookup = {
            "U": Direction.UP,
            "D": Direction.DOWN,
            "L": Direction.LEFT,
            "R": Direction.RIGHT,
        }

        return (direction_lookup[direction_str], int(steps_str))

    def __repr__(self) -> str:
        string = (
            "==========================="
            f"head: {self.head_pos}\n"
            + f"tail: {self.tail_pos}\n"
            + f"visited: {self.visited}\n"
            + "============================"
        )
        return string


test_input = """R 4
U 4
L 3
D 1
R 4
D 1
L 5
R 2"""


def main() -> None:
    lines = test_input.splitlines()

    sim = Simulation()
    for line in lines:
        sim.simulate_command(line)

    print(len(sim.visited))
    return


if __name__ == "__main__":
    main()
