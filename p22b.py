import re
import enum


def parse_cube(desc: str) -> list[list[str]]:
    lines = desc.splitlines()

    zone1 = [lines[i][50:100] for i in range(50)]
    zone2 = [lines[i][100:150] for i in range(50)]
    zone3 = [lines[i][50:100] for i in range(50, 100)]
    zone4 = [lines[i][0:50] for i in range(100, 150)]
    zone5 = [lines[i][50:100] for i in range(100, 150)]
    zone6 = [lines[i][0:50] for i in range(150, 200)]

    inst_iter = [
        (match.group(1), int(match.group(2)))
        for match in re.finditer(r"([LR]?)(\d+)", lines[-1])
    ]

    return (zone1, zone2, zone3, zone4, zone5, zone6), inst_iter


class Dir(enum.IntEnum):
    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3


WRAP = (
    ((5, Dir.RIGHT), (1, Dir.RIGHT), (2, Dir.DOWN), (3, Dir.RIGHT)),
    ((5, Dir.UP), (4, Dir.LEFT), (2, Dir.LEFT), (0, Dir.LEFT)),
    ((0, Dir.UP), (1, Dir.UP), (4, Dir.DOWN), (3, Dir.DOWN)),
    ((2, Dir.RIGHT), (4, Dir.RIGHT), (5, Dir.DOWN), (0, Dir.RIGHT)),
    ((2, Dir.UP), (1, Dir.LEFT), (5, Dir.LEFT), (3, Dir.LEFT)),
    ((3, Dir.UP), (4, Dir.UP), (1, Dir.DOWN), (0, Dir.DOWN)),
)

DENORMALIZATION = ((0, 50), (0, 100), (50, 50), (100, 0), (100, 50), (150, 0))


def main() -> None:
    with open("day22.txt") as fp:
        desc = fp.read()

    cube, instructions = parse_cube(desc)
    old_pos = None
    pos = (0, 0, 0)
    facing = Dir.RIGHT

    M = {
        (z, y, x)
        for z, zone in enumerate(cube)
        for y, row in enumerate(zone)
        for x, ch in enumerate(row)
        if ch == "#"
    }

    counter = 0
    for rot, steps in instructions:
        if rot:
            facing = Dir((facing + 1 if rot == "R" else facing - 1) % 4)

        for i in range(steps):
            old_pos = pos
            pos, facing = move(pos, facing, M)
            if old_pos == pos:
                break

    z, y, x = pos
    print(pos)

    dy, dx = DENORMALIZATION[z]
    col, row = (x + dx + 1, y + dy + 1)
    print(col, row)

    answer = 1000 * row + 4 * col + (facing - 1)
    print(f"answer: {answer}")
    return


def move(pos, facing, M):
    moves = ((0, -1, 0), (0, 0, 1), (0, 1, 0), (0, 0, -1))
    move = moves[facing]

    zone, y, x = tuple(val + d for val, d in zip(pos, move))
    new_facing = facing
    new_zone = zone
    if not (0 <= y < 50 and 0 <= x < 50):
        if facing == Dir.UP:
            y += 50
        elif facing == Dir.RIGHT:
            x -= 50
        elif facing == Dir.LEFT:
            x += 50
        elif facing == Dir.DOWN:
            y -= 50

        new_zone, new_facing = WRAP[zone][facing]
        if facing == new_facing:
            pass
        elif facing + new_facing in (2, 4):
            x, y = 49 - x, 49 - y
        elif (facing, new_facing) == 3:
            x, y = y, x
        elif (facing, new_facing) in [(Dir.LEFT, Dir.DOWN), (Dir.RIGHT, Dir.UP)]:
            x, y = y, 49 - x
        else:
            x, y = 49 - y, x

    new_pos = (new_zone, y, x)
    if new_pos in M:
        return pos, facing

    return new_pos, new_facing


if __name__ == "__main__":
    main()
