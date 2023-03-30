import itertools as it

test_input = """1=-0-2
12111
2=0=
21
2=01
111
20012
112
1=-1=
1-12
12
1=
122"""

#   Decimal          SNAFU                        Binary
#         1              1                             1
#         2              2                            10
#         3             1=                            11
#         4             1-                           100
#         5             10                           101
#         6             11                           110
#         7             12                           111
#         8             2=                          1000
#         9             2-                          1001
#        10             20                          1010
#        15            1=0                          1111
#        20            1-0                         10100
#      2022         1=11-2                   11111100110
#     12345        1-0---0                  100100101001
# 314159265  1121-1110-1=0 10010101110011011000010100001


def main() -> None:
    with open("day25.txt") as fp:
        lines = fp.readlines()
    # lines = test_input.splitlines()

    # numbers = [parse_snafu(line.strip()) for line in lines]
    # print(sum(numbers))

    snafu_nums = [line.strip() for line in lines]
    snafu_final = snafu_sum(snafu_nums)
    print(snafu_final, parse_snafu(snafu_final))
    return


def parse_snafu(num: str) -> int:
    base10 = 0
    for i, ch in enumerate(reversed(num)):
        value = {"1": 1, "2": 2, "-": -1, "=": -2, "0": 0}
        base10 += value[ch] * (5**i)
    return base10


def snafu_sum(nums) -> str:
    carry = 0
    final = ""
    value = {"1": 1, "2": 2, "-": -1, "=": -2, "0": 0}
    eulav = {1: "1", 2: "2", -1: "-", -2: "=", 0: "0"}

    for chars in it.zip_longest(*[reversed(num) for num in nums], fillvalue="0"):
        cur = carry
        carry = 0
        for ch in chars:
            cur += value[ch]

            if cur > 2:
                cur -= 5
                carry += 1
            elif cur < -2:
                cur += 5
                carry -= 1

        final += eulav[cur]
    return "".join(reversed(final))


def base10_to_snafu(num: int) -> str:
    return


if __name__ == "__main__":
    main()
