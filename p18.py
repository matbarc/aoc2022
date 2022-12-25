test_lines = """2,2,2
1,2,2
3,2,2
2,1,2
2,3,2
2,2,1
2,2,3
2,2,4
2,2,6
1,2,5
3,2,5
2,1,5
2,3,5"""


def main() -> None:
    with open("day18.txt") as fp:
        lines = fp.readlines()

    cubes = [eval(line.strip()) for line in lines]

    face_count = 0

    for c1 in cubes:
        face_count += 6
        for c2 in cubes:
            if c1 == c2:
                continue

            if cubes_adjacent(c1, c2):
                face_count -= 1

    answer = face_count
    print(f"answer: {answer}")

    maxs = (0, 0, 0)
    mins = (0, 0, 0)
    for c in cubes:
        maxs = tuple(map(max, zip(c, maxs)))
        mins = tuple(map(min, zip(c, mins)))

    ranges = [range(low - 1, high + 2) for low, high in zip(mins, maxs)]

    q = [mins]
    seen = set(mins)
    answer2 = 0
    while q:
        coords = q.pop()
        for neighbor in neighbours(coords):
            if neighbor in seen or is_oob(neighbor, ranges):
                continue
            if neighbor in cubes:
                answer2 += 1
            else:
                q.append(neighbor)
                seen.add(neighbor)

    print(answer2)
    return


def is_oob(c: (int, int, int), ranges) -> bool:
    for coord, _range in zip(c, ranges):
        if coord not in _range:
            return True
    return False


def neighbours(coords):
    x, y, z = coords
    for dx, dy, dz in (
        (1, 0, 0),
        (-1, 0, 0),
        (0, 1, 0),
        (0, -1, 0),
        (0, 0, 1),
        (0, 0, -1),
    ):
        yield x + dx, y + dy, z + dz


def cubes_adjacent(c1, c2) -> bool:
    x1, y1, z1 = c1
    x2, y2, z2 = c2
    return (
        (x1 == x2 and y1 == y2 and abs(z1 - z2) == 1)
        or (z1 == z2 and y1 == y2 and abs(x1 - x2) == 1)
        or (x1 == x2 and z1 == z2 and abs(y1 - y2) == 1)
    )


if __name__ == "__main__":
    main()
