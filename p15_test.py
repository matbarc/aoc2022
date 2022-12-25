from .p15 import agg_line_ranges, agg_ranges


def test_subset():
    input1, input2 = [(1, 10), (2, 4)]
    computed = agg_ranges(input1, input2)
    expected = [(1, 10)]
    assert computed == expected


def test_contiguous():
    input1, input2 = [(1, 10), (11, 30)]
    computed = agg_ranges(input1, input2)
    expected = [(1, 30)]
    assert computed == expected


def test_overlapping():
    input1, input2 = [(1, 10), (5, 30)]
    computed = agg_ranges(input1, input2)
    expected = [(1, 30)]
    assert computed == expected


def test_mutually_exclusive():
    input1, input2 = [(1, 10), (20, 30)]
    computed = agg_ranges(input1, input2)
    expected = [(1, 10), (20, 30)]
    assert computed == expected


def test_triplet():
    input_ = [(1, 10), (2, 4), (20, 30)]
    computed = agg_line_ranges(input_)
    expected = [(1, 10), (20, 30)]
    assert computed == expected
