from .p13 import new_compare_pair
import functools as ft

test_input = [
    [1, 1, 3, 1, 1],
    [1, 1, 5, 1, 1],
    [[1], [2, 3, 4]],
    [[1], 4],
    [9],
    [[8, 7, 6]],
    [[4, 4], 4, 4],
    [[4, 4], 4, 4, 4],
    [7, 7, 7, 7],
    [7, 7, 7],
    [],
    [3],
    [[[]]],
    [[]],
    [1, [2, [3, [4, [5, 6, 7]]]], 8, 9],
    [1, [2, [3, [4, [5, 6, 0]]]], 8, 9],
]

extra = [[[2]], [[6]]]


def test_1():
    left = [1, 1, 3, 1, 1]
    right = [1, 1, 5, 1, 1]

    assert new_compare_pair(left, right) == -1


def test_2():
    left = [7, 7, 7]
    right = [9]

    assert new_compare_pair(left, right) == -1
    assert new_compare_pair(right, left) == 1


def test_3():
    left = [[4, 4], 4, 4, 4]
    right = [[4, 4], 4, 4]

    assert new_compare_pair(left, right) == 1


def test_sort():
    expected = [
        [],
        [[]],
        [[[]]],
        [1, 1, 3, 1, 1],
        [1, 1, 5, 1, 1],
        [[1], [2, 3, 4]],
        [1, [2, [3, [4, [5, 6, 0]]]], 8, 9],
        [1, [2, [3, [4, [5, 6, 7]]]], 8, 9],
        [[1], 4],
        [[2]],
        [3],
        [[4, 4], 4, 4],
        [[4, 4], 4, 4, 4],
        [[6]],
        [7, 7, 7],
        [7, 7, 7, 7],
        [[8, 7, 6]],
        [9],
    ]

    assert sorted(test_input + extra, key=ft.cmp_to_key(new_compare_pair)) == expected


def test_good_indexes():
    pairs = [test_input[i * 2 : (i * 2) + 2] for i in range(len(test_input) // 2)]
    good_indexes = [
        i for i, [l1, l2] in enumerate(pairs, 1) if new_compare_pair(l1, l2) == -1
    ]

    assert sum(good_indexes) == 13
