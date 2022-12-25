import itertools as it
import functools as ft


def main() -> None:
    with open("day13.txt") as fp:
        file = fp.read()

    pairs = [
        [eval(list_desc) for list_desc in pair_string.splitlines()]
        for pair_string in file.split("\n\n")
    ]

    all_signals = [eval(packet.strip()) for packet in file.splitlines() if packet] + [
        [[2]],
        [[6]],
    ]

    good_indexes = [
        i for i, [l1, l2] in enumerate(pairs, 1) if new_compare_pair(l1, l2) == 1
    ]

    print(good_indexes)
    print(sum(good_indexes))

    all_signals.sort(key=ft.cmp_to_key(new_compare_pair))
    i1 = all_signals.index([[2]]) + 1
    i2 = all_signals.index([[6]]) + 1
    print(*all_signals, sep="\n")
    print(i1 * i2)
    return


def new_compare_pair(left, right) -> bool:
    if left is None:
        return -1
    elif right is None:
        return 1

    if type(left) == type(right) == int:
        if right < left:
            return 1
        elif left < right:
            return -1
        else:
            return 0

    left = left if type(left) == list else [left]
    right = right if type(right) == list else [right]

    for l, r in it.zip_longest(left, right):
        cmp = new_compare_pair(l, r)
        if cmp == 0:
            continue
        elif cmp == 1:
            return 1
        else:
            return -1
    return 0


if __name__ == "__main__":
    main()
