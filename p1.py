#!/bin/python


def main() -> None:
    master_list = []
    current_elf_total = 0

    with open("elves_list.txt") as fp:
        for line in fp.readlines():
            if line == "\n":
                master_list.append(current_elf_total)
                current_elf_total = 0
            else:
                current_elf_total += int(line.strip())

    # a
    # print(sum(possibly_faster_top_3(master_list)[0]))
    # b
    # print(sorted(master_list, reverse=True)[0:3])
    print(sum(possibly_faster_top_3(master_list)))
    return


def possibly_faster_top_3(lst: list[int]) -> list[int]:
    if len(lst) < 3:
        raise Exception("Bad Input")

    top = lst[0:3]
    for num in lst[3:]:
        for i in range(3):
            if num > top[i]:
                top.insert(i, num)
                top.pop()
                break
    return top


if __name__ == "__main__":
    main()
