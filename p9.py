from dataclasses import dataclass
import math


@dataclass
class Pos:
    x: int
    y: int


class Simulation:
    def __init__(self) -> None:
        self.origin = Pos(0, 0)
        self.head_pos = Pos(0, 0)
        self.tail_pos = Pos(0, 0)

        self.visited = set()
        return

    def simulate_command(self) -> None:
        return

    def _move_head_one_step(self, direction: str) -> None:
        return

    def _chase_with_tail(self) -> None:
        dx = self.head_pos.x - self.tail_pos.x
        dy = self.head_pos.y - self.tail_pos.y
        distance = math.sqrt(dx**2 + dy**2)

        if distance < math.sqrt(2):
            return
        return

    @staticmethod
    def parse_command(command: str) -> (str, int):
        direction, steps_str = command.split()
        return (direction, int(steps_str))


def main() -> None:

    return


def coords_after_move(pos: (int, int), command: str) -> None:
    direction, steps = parse_command(command)
    return


if __name__ == "__main__":
    main()
