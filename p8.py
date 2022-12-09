test_input = """30373
25512
65332
33549
35390"""


def main() -> None:
    with open("day8.txt") as fp:
        lines = fp.readlines()

    # lines = test_input.splitlines()

    grid = [[int(ch) for ch in line.strip()] for line in lines]

    height = len(grid)
    width = len(grid[0])

    total = 0

    print(is_tree_visible(grid, 42, 97))

    big_string = ""
    for y in range(height):
        to_print = ""
        for x in range(width):
            is_visible = is_tree_visible(grid, x, y)
            if is_visible:
                total += 1
                to_print += str(grid[y][x])
            else:
                to_print += " "
        big_string += to_print + "\n"

    # with open("debug.txt", "w+") as fp:
    #     fp.write(big_string)
    print(total)
    return


def is_tree_visible(grid: list[list[int]], x: int, y: int) -> bool:
    height = len(grid)
    width = len(grid[0])

    tree_height = grid[y][x]

    if x in (0, width - 1) or y in (0, height - 1):
        return True  # edge

    tallest_right = max(grid[y][x + 1 :])
    tallest_left = max(grid[y][:x])
    tallest_up = max([grid[y_prime][x] for y_prime in range(y)])
    tallest_down = max([grid[y_prime][x] for y_prime in range(y + 1, height)])

    minimum_in_cross = min(tallest_down, tallest_left, tallest_right, tallest_up)
    if minimum_in_cross < tree_height:
        return True
    return False


if __name__ == "__main__":
    main()
