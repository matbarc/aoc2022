import time
import os
from colorama import Fore, init

init()
test_input = """498,4 -> 498,6 -> 496,6
503,4 -> 502,4 -> 502,9 -> 494,9"""

SAND_CHAR = "o"
AIR_CHAR = " "
WALL_CHAR = "#"


def main() -> None:
    with open("day14.txt") as fp:
        real_input = fp.read()

    sim = Simulation(real_input)

    while sim.tick():
        pass

    sim.print_grid()
    print(f"total resting particles: {sim.resting_particles}")
    return


Coord = tuple[int, int]


class Simulation:
    def __init__(self, wall_description: str) -> None:
        paths = [self._parse_nodes(desc) for desc in wall_description.splitlines()]
        filled_walls = [coord for nodes in paths for coord in self._filled_paths(nodes)]
        self.sand_source = (500, 0)

        grid, width = self._make_grid(filled_walls)
        self.grid = grid
        self.width = width
        self.length = len(grid) // width

        self.active_sand = None
        self.resting_particles = 0
        return

    def tick(self) -> None:
        if self.active_sand is None:
            if not self.spawn_particle():
                return False
        elif (move_code := self.move_active_particle()) != 1:
            if move_code == -1:
                return False
            self.active_sand = None
        return True

    def spawn_particle(self) -> bool:
        x0, y0 = self.sand_source

        if not self.is_blocked(x0, y0):
            self.active_sand = self.sand_source
            self.grid[self.coord_to_idx(x0, y0)] = SAND_CHAR
            return True
        return False

    def move_active_particle(self) -> int:
        x0, y0 = self.active_sand
        sorted_potential_moves = [(x0, y0 + 1), (x0 - 1, y0 + 1), (x0 + 1, y0 + 1)]
        for x, y in sorted_potential_moves:

            if self.is_oob(x, y):
                self.grid[self.coord_to_idx(x0, y0)] = AIR_CHAR
                self.active_sand = None
                return -1  # terminate

            if not self.is_blocked(x, y):
                if self.active_sand == (619, 170):
                    print(self.active_sand, x, y, self.coord_to_idx(x, y))
                self.grid[self.coord_to_idx(x, y)] = SAND_CHAR
                self.grid[self.coord_to_idx(x0, y0)] = AIR_CHAR
                self.active_sand = (x, y)
                return 1  # regular
        self.resting_particles += 1
        return 0  # new spawn

    def coord_to_idx(self, x: int, y: int) -> int:
        return y * self.width + (x - self.x_baseline)

    def is_blocked(self, x: int, y: int) -> bool:
        oob = self.is_oob(x, y)
        index = self.coord_to_idx(x, y)
        try:
            return not oob and not self.grid[index] == AIR_CHAR
        except IndexError as e:
            print(e)
            raise ValueError(f"{x,y,oob, index, len(self.grid)}")

    def is_oob(self, x: int, y: int) -> bool:
        if x % self.x_baseline >= self.width:
            return True

        return self.coord_to_idx(x, y) >= len(self.grid)

    def print_grid(self) -> None:
        def colored(ch: str) -> str:
            return ch if ch != "o" else f"{Fore.YELLOW}{ch}{Fore.RESET}"

        final = ""
        for i in range(self.length):
            start = self.width * i
            end = start + self.width
            final += f"{i:03} {''.join([colored(ch) for ch in self.grid[start:end]])}\n"

        print(final)
        return

    def add_floor(self) -> None:
        return

    @staticmethod
    def _parse_nodes(nodes_description: str) -> list[tuple[int, int]]:
        path = [
            tuple(int(coord) for coord in coord_description.split(","))
            for coord_description in nodes_description.split(" -> ")
        ]
        return path

    @staticmethod
    def _filled_paths(nodes: list[tuple[int, int]]) -> list[tuple[int, int]]:
        nodes_copy = nodes[:]
        filled_path = [nodes_copy[0]]
        for i in range(len(nodes_copy) - 1):
            x0, y0 = nodes_copy[i]
            x1, y1 = nodes_copy[i + 1]

            dx = x1 - x0
            dy = y1 - y0

            if dx == 0:
                step = 1 if dy > 0 else -1
                sub_path = [(x0, y) for y in range(y0 + step, y1 + step, step)]
            elif dy == 0:
                step = 1 if dx > 0 else -1
                sub_path = [(x, y0) for x in range(x0 + step, x1 + step, step)]
            else:
                raise ValueError(f"Invalid nodes: {nodes_copy[i:i+2]}")
            filled_path.extend(sub_path)
        return filled_path

    def _make_grid(self, wall_coords: list[tuple[int, int]]) -> (list[str], int):
        coords = wall_coords + [self.sand_source]

        max_y = max(coords, key=lambda c: c[1])[1]
        min_y = min(coords, key=lambda c: c[1])[1]
        max_x = max(coords, key=lambda c: c[0])[0]
        min_x = min(coords, key=lambda c: c[0])[0]
        self.x_baseline = min_x

        def get_char(coord: tuple[int, int]) -> str:
            if coord in wall_coords:
                ch = WALL_CHAR
            else:
                ch = AIR_CHAR
            return ch

        grid = [
            get_char((x, y))
            for y in range(min_y, max_y + 1)
            for x in range(min_x, max_x + 1)
        ]

        # adding floor for part 2
        # grid += [AIR_CHAR for i in range(min_x, max_x + 1)]
        # grid += [WALL_CHAR for i in range(min_x, max_x + 1)]

        width = max_x - min_x + 1
        assert len(grid) % width == 0
        print(width)
        return (grid, width)


if __name__ == "__main__":
    main()
