import itertools as it

test_input = """30373
25512
65332
33549
35390"""


def main() -> None:
    with open("aoc2022/day8.txt") as fp:
        lines = fp.readlines()

    # lines = test_input.splitlines()

    grid = [[int(ch) for ch in line.strip()] for line in lines]

    height = len(grid)
    width = len(grid[0])

    big_string = ""
    max_score = 0
    for y in range(height):
        to_print = ""
        for x in range(width):
            score = get_scenic_score(grid, x, y)

            if score > max_score:
                max_score = score

            to_print += str(score)
        big_string += to_print + "\n"

    # with open("debug.txt", "w+") as fp:
    #     fp.write(big_string)
    print(max_score)
    return


def get_scenic_score(grid: list[list[int]], x: int, y: int) -> int:
    height = len(grid)
    width = len(grid[0])

    tree_height = grid[y][x]

    if x in (0, width - 1) or y in (0, height - 1):
        return 0  # edge

    right = grid[y][x + 1 :]
    left = list(reversed(grid[y][:x]))
    up = list(reversed([grid[y_prime][x] for y_prime in range(y)]))
    down = [grid[y_prime][x] for y_prime in range(y + 1, height)]

    res = 1
    for lst in right, left, up, down:
        visible = len(list(it.takewhile(lambda x: x < tree_height, lst)))
        if visible < len(lst) and lst[visible] == tree_height:
            visible += 1
        res *= visible

    return res


if __name__ == "__main__":
    main()
