example_input = """vJrwpWtwJgWrhcsFMMfFFhFp
jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL
PmmdzqPrVvPwwTWBwg
wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn
ttgJtRGJQctTZtZT
CrZsJsPPZsGzwwsLwLmpwMDw"""


def main() -> None:
    with open("day3.txt") as fp:
        lines = fp.readlines()

    items = []
    priority_sum = 0

    for line in lines:
        limit = len(line) // 2
        for ch in line[: limit + 1]:
            if line.find(ch, limit) != -1:
                items.append(ch)
                priority_sum += get_priority(ch)
                break

    print(items, priority_sum, sep="\n")
    return


def get_priority(char: str) -> int:
    if len(char) != 1 or not char.isalpha():
        raise ValueError("Can only deal with single characters")

    if char.isupper():
        return ord(char) - 38  # A - 27 ... Z - 56

    return ord(char) - 96  # a - 1 ... z - 26


if __name__ == "__main__":
    main()
