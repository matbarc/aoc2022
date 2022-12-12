test_input = """addx 15
addx -11
addx 6
addx -3
addx 5
addx -1
addx -8
addx 13
addx 4
noop
addx -1
addx 5
addx -1
addx 5
addx -1
addx 5
addx -1
addx 5
addx -1
addx -35
addx 1
addx 24
addx -19
addx 1
addx 16
addx -11
noop
noop
addx 21
addx -15
noop
noop
addx -3
addx 9
addx 1
addx -3
addx 8
addx 1
addx 5
noop
noop
noop
noop
noop
addx -36
noop
addx 1
addx 7
noop
noop
noop
addx 2
addx 6
noop
noop
noop
noop
noop
addx 1
noop
noop
addx 7
addx 1
noop
addx -13
addx 13
addx 7
noop
addx 1
addx -33
noop
noop
noop
addx 2
noop
noop
noop
addx 8
noop
addx -1
addx 2
addx 1
noop
addx 17
addx -9
addx 1
addx 1
addx -3
addx 11
noop
noop
addx 1
noop
addx 1
noop
noop
addx -13
addx -19
addx 1
addx 3
addx 26
addx -30
addx 12
addx -1
addx 3
addx 1
noop
noop
noop
addx -9
addx 18
addx 1
addx 2
noop
noop
addx 9
noop
noop
noop
addx -1
addx 2
addx -37
addx 1
addx 3
noop
addx 15
addx -21
addx 22
addx -6
addx 1
noop
addx 2
addx 1
noop
addx -10
noop
noop
addx 20
addx 1
addx 2
addx 2
addx -6
addx -11
noop
noop
noop"""

small_program = """noop
addx 3
addx -5"""


class SimpleVM:
    def __init__(self, initial_val: int = 1) -> None:
        self.history = [initial_val]
        self.register = initial_val
        return

    def _pass_cycle(self) -> None:
        self.history.append(self.register)
        return

    def _update_register(self, value: int) -> None:
        self.register = value
        self._pass_cycle()
        return

    def run_command(self, command: str) -> None:
        if command == "noop":
            self._pass_cycle()
            return

        operation, operand = command.split()
        value_to_add = int(operand)
        self._pass_cycle()
        self._update_register(self.register + value_to_add)
        return

    def get_pixel(self, cycle: int) -> str:
        sprit_middle_loc = self.history[cycle]
        x_loc_currently_painting = cycle % 40

        if abs(x_loc_currently_painting - sprit_middle_loc) < 2:
            return "#"
        return "."


def main() -> None:
    # lines = test_input.splitlines()
    with open("day10.txt") as fp:
        lines = fp.readlines()

    vm = SimpleVM()

    for line in lines:
        vm.run_command(line.strip())

    # interesting_indexes = [19, 59, 99, 139, 179, 219]
    # register_snapshots = [vm.history[i] * (i + 1) for i in interesting_indexes]
    # print(register_snapshots, sum(register_snapshots))

    for i in range(6):
        start = i * 40
        end = (i + 1) * 40
        chars = [vm.get_pixel(cycle) for cycle in range(start, end + 1)]
        print("".join(chars))
    return


if __name__ == "__main__":
    main()
