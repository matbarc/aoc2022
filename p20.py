test_input = """1
2
-3
3
-2
0
4"""


def main() -> None:
    key = 811589153
    mixings_n = 10

    with open("day20.txt") as fp:
        ns = [(i, int(line) * key) for i, line in enumerate(fp.readlines())]

    # ns = [(i, int(line)) for i, line in enumerate(test_input.splitlines())]
    d = ns.copy()

    for _ in range(mixings_n):
        for i, n in ns:
            idx = d.index((i, n))
            target = (idx + n) % (len(ns) - 1)
            d.insert(target, d.pop(idx))

    final = [val for _, val in d]
    mod = len(final)

    zero_i = final.index(0)
    coords = [final[(i + zero_i) % mod] for i in (1000, 2000, 3000)]
    print(f"answer: {sum(coords)}")

    return


if __name__ == "__main__":
    main()
