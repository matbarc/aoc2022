from collections import deque, defaultdict

test_input = """..............
..............
.......#......
.....###.#....
...#...#.#....
....#...##....
...#.###......
...##.#.##....
....#..#......
..............
..............
.............."""

small_input = """.....
..##.
..#..
.....
..##.
....."""


def sim(M: set[complex], turn_limit=None) -> None:
    dirs = deque(
        [
            (-1 - 1j, -1j, 1 - 1j),
            (-1 + 1j, 1j, 1 + 1j),
            (-1 - 1j, -1, -1 + 1j),
            (1 - 1j, 1, 1 + 1j),
        ]
    )
    turns = 0
    while not turn_limit or turns < turn_limit:
        turns += 1
        moves = defaultdict(list)

        for elf in M:
            elf_moves = []
            for left, move, right in dirs:
                if not {left + elf, move + elf, right + elf} & M:
                    elf_moves.append(elf + move)

            if elf_moves and len(elf_moves) < len(dirs):
                moves[elf_moves[0]].append(elf)

        if len(moves) == 0:
            return turns, M

        for move, elves in moves.items():
            if len(elves) == 1:
                M.remove(elves[0])
                M.add(move)

        dirs.rotate(-1)
    return turns, M


def main() -> None:
    with open("day23.txt") as fp:
        lines = fp.readlines()
    # lines = test_input.splitlines()

    elves = {
        x + y * 1j
        for y, line in enumerate(lines)
        for x, ch in enumerate(line)
        if ch == "#"
    }

    turns, final = sim(elves)

    (minx, miny, maxx, maxy) = find_bounds(final)
    answer1 = (maxx - minx + 1) * (maxy - miny + 1) - len(elves)
    print(f"answer1: {answer1}")
    print(f"answer2: {turns}")
    return


def find_bounds(coords: list[complex]):
    miny = int(min(c.imag for c in coords))
    maxy = int(max(c.imag for c in coords))
    minx = int(min(c.real for c in coords))
    maxx = int(max(c.real for c in coords))
    return (minx, miny, maxx, maxy)


def print_grid(coords: list[(int, int)], pad=1):
    ((minx, maxx), (miny, maxy)) = find_bounds(coords)

    final = ""
    for y in range(miny - pad, maxy + 1 + pad):
        for x in range(minx - pad, maxx + 1 + pad):
            final += "#" if (x, y) in coords else "."
        final += "\n"

    print(final)
    return


if __name__ == "__main__":
    main()
