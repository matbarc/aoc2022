import enum
import re


class Direction(enum.IntEnum):
    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3


def main() -> None:
    with open("day22.txt") as fp:
        data = fp.read()

    map_desc, instructions = data.split("\n\n")
    M = map_desc.split("\n")

    pos = find_start(M)
    old = pos
    direc = Direction.RIGHT

    print(f"starting at: {pos}")
    for match in re.finditer(r"([LR]?)(\d+)", instructions):
        rotation, steps_str = match.groups()
        if rotation:
            direc = Direction((direc + 1 if rotation == "R" else direc - 1) % 4)
        print(f"moving {steps_str} to {direc.name} ({direc})")
        for i in range(int(steps_str)):
            old = pos
            pos = move(pos, direc, M)
            if old == pos:
                break

    row = pos[1] + 1
    col = pos[0] + 1
    facing = direc - 1

    print(f"ended at: {pos} / row: {row} col: {col} facing: {direc}")
    print(f"answer: {1000 * row + 4 * col + facing}")
    return


def find_start(M):
    for y, row in enumerate(M):
        for x, ch in enumerate(row):
            if ch == ".":
                return (x, y)


def move(cur_pos, direc, M):
    moves = ((0, -1), (1, 0), (0, 1), (-1, 0))
    move = moves[direc]
    x, y = (
        (cur_pos[0] + move[0]) % len(M[cur_pos[1]]),
        (cur_pos[1] + move[1]) % len(M),
    )
    print(cur_pos)

    if len(M[y]) <= x or M[y][x] == " ":
        if direc in (0, 2):
            universe = list(
                enumerate([M[j][x] if x < len(M[j]) else " " for j in range(0, len(M))])
            )
            if direc == 0:
                universe = reversed(universe)
            for j, ch in universe:
                if ch == "#":
                    break
                elif ch == ".":
                    return (x, j)
        else:
            universe = list(enumerate(M[y]))
            if direc == 3:
                universe = reversed(universe)
            for j, ch in universe:
                if ch == "#":
                    break
                elif ch == ".":
                    return (j, y)

    elif M[y][x] == ".":
        return (x, y)

    elif M[y][x] == "#":
        return cur_pos

    return cur_pos


if __name__ == "__main__":
    main()
