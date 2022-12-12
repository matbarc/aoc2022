from typing import Callable
import math


class Monkey:
    def __init__(
        self,
        name: str,
        inventory: list[int],
        operation: Callable[int, int],
        test_num: int,
        throw_on_fail: int,
        throw_on_success: int,
    ) -> None:
        self.name = name
        self.inventory = inventory
        self.operation = operation
        self.test_num = test_num
        self.throw_on_fail = throw_on_fail
        self.throw_on_success = throw_on_success
        self.inspections = 0
        return

    def test(self, item: int) -> bool:
        return item % self.test_num == 0


def main_monkeys() -> list[Monkey]:
    m0 = Monkey("Monkey 0", [50, 70, 54, 83, 52, 78], lambda x: x * 3, 11, 7, 2)
    m1 = Monkey("Monkey 1", [71, 52, 58, 60, 71], lambda x: x * x, 7, 2, 0)
    m2 = Monkey("Monkey 2", [66, 56, 56, 94, 60, 86, 73], lambda x: x + 1, 3, 5, 7)
    m3 = Monkey("Monkey 3", [83, 99], lambda x: x + 8, 5, 4, 6)
    m4 = Monkey("Monkey 4", [98, 98, 79], lambda x: x + 3, 17, 0, 1)
    m5 = Monkey("Monkey 5", [76], lambda x: x + 4, 13, 3, 6)
    m6 = Monkey("Monkey 6", [52, 51, 84, 54], lambda x: x * 17, 19, 1, 4)
    m7 = Monkey("Monkey 7", [82, 86, 91, 79, 94, 92, 59, 94], lambda x: x + 7, 2, 3, 5)

    monkeys = [m0, m1, m2, m3, m4, m5, m6, m7]
    return monkeys


def test_monkeys() -> list[Monkey]:
    m0 = Monkey("Monkey 0", [79, 98], lambda x: x * 19, 23, 3, 2)
    m1 = Monkey("Monkey 1", [54, 65, 75, 74], lambda x: x + 6, 19, 0, 2)
    m2 = Monkey("Monkey 2", [79, 60, 97], lambda x: x * x, 13, 3, 1)
    m3 = Monkey("Monkey 3", [74], lambda x: x + 3, 17, 1, 0)

    monkeys = [m0, m1, m2, m3]
    return monkeys


def main() -> None:
    monkeys = main_monkeys()
    LIMIT = math.prod([m.test_num for m in monkeys])

    for i in range(1, 10_000 + 1):
        for monkey in monkeys:
            for item in monkey.inventory[:]:
                # item = monkey.operation(item) // 3
                new_val = monkey.operation(item)
                item = new_val if new_val < LIMIT else new_val % LIMIT
                monkey.inspections += 1
                throw_index = (
                    monkey.throw_on_success
                    if monkey.test(item)
                    else monkey.throw_on_fail
                )
                monkeys[throw_index].inventory.append(item)
                monkey.inventory.pop(0)

        if i % 1000 == 0:
            print(f"------ round {i} --------")
            print(*[m.inspections for m in monkeys], sep="\n")

    inspections = [m.inspections for m in monkeys]
    maxi = max(inspections)
    inspections.remove(maxi)
    maxi2 = max(inspections)

    print(maxi * maxi2)
    return


if __name__ == "__main__":
    main()
