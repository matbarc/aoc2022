test_input = """2-4,6-8
2-3,4-5
5-7,7-9
2-8,3-7
6-6,4-6
2-6,4-8"""


def main() -> None:
    with open("day4.txt") as fp:
        lines = fp.readlines()

    pairs = [
        [translate_range(range_code) for range_code in line.split(",")]
        for line in lines
    ]
    # pairs_with_full_overlap = [pair for pair in pairs if one_is_subset(*pair)]
    pairs_with_overlap = [pair for pair in pairs if not mutually_exclusive(*pair)]

    print(len(pairs_with_overlap), sep="\n")
    return


def translate_range(range_code: str) -> range:
    start, stop = range_code.split("-")
    return range(int(start), int(stop) + 1)


def one_is_subset(r1: range, r2: range) -> bool:
    return (r1.start in r2 and r1[-1] in r2) or (r2.start in r1 and r2[-1] in r1)


def mutually_exclusive(r1: range, r2: range) -> bool:
    return r1[-1] < r2.start or r2[-1] < r1.start


if __name__ == "__main__":
    main()
