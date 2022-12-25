from collections import deque

test_input = """#.######
#>>.<^<#
#.<..<<#
#>v.><>#
#<^v^^>#
######.#"""


def main() -> None:
    with open("day24.txt") as fp:
        lines = fp.readlines()
    # lines = test_input.splitlines()

    bliz = []
    width = 0
    height = 0

    for row, line in enumerate(lines[1:-1]):
        height += 1
        for col, ch in enumerate(line.strip()[1:-1]):
            if row == 0:
                width += 1
            if ch in "<>^v":
                bliz.append((ch, (row, col)))

    pos0 = (-1, 0)
    end = (height, width - 1)
    print(pos0, end)

    # bfs
    t1 = bfs(pos0, end, bliz, height, width, 0)
    print(t1)
    t2 = bfs(end, pos0, bliz, height, width, t1)
    print(t2)
    t3 = bfs(pos0, end, bliz, height, width, t2)
    print(t3)
    return


def neighbors(pos, height, width) -> list[(int, int)]:
    y, x = pos
    moves = {(0, 1), (0, 0), (1, 0), (-1, 0), (0, -1)}

    to_ret = {
        (y + dy, x + dx)
        for dy, dx in moves
        if (y + dy in range(height) and x + dx in range(width))
        or (y + dy, x + dx) in [(-1, 0), (height, width - 1)]
    }
    return to_ret


def bfs(start, end, blizs, height, width, time):
    q = deque([start])

    while q:
        next_queue = set()
        time += 1
        bliz = get_blizzard_at(blizs, time, height, width)

        for pos in q:
            possible_neighbors = neighbors(pos, height, width) - bliz

            if end in possible_neighbors:
                return time

            for n in possible_neighbors:
                next_queue.add(n)

        q = next_queue


blizzard_cache = {}


def get_blizzard_at(blizzards, time, height, width):
    res = blizzard_cache.get(time, None)
    if res:
        return res

    new_map = set()
    moves = {">": (0, 1), "<": (0, -1), "v": (1, 0), "^": (-1, 0)}
    for dir, (y, x) in blizzards:
        dy, dx = moves[dir]
        ny = (y + dy * time) % height
        nx = (x + dx * time) % width
        new_map.add((ny, nx))

    blizzard_cache[time] = new_map
    return new_map


def print_grid(height, width, poss):
    line = ""
    for y in range(height):
        for x in range(width):
            pos = (y, x)
            if pos in poss:
                line += "b"
            else:
                line += "."
        line += "\n"

    print(line)
    return


if __name__ == "__main__":
    main()
