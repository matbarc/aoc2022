import re
from sympy.parsing import parse_expr
from sympy import solve
from sympy.abc import x

test_input = """root: pppw + sjmn
dbpl: 5
cczh: sllz + lgvd
zczc: 2
ptdq: humn - dvpt
dvpt: 3
lfqf: 4
humn: 5
ljgn: 2
sjmn: drzm * dbpl
sllz: 4
pppw: cczh / lfqf
lgvd: ljgn * ptdq
drzm: hmdt - zczc
hmdt: 32"""


def main() -> None:

    with open("day21.txt") as fp:
        lines = fp.readlines()

    monkeys = [parse_monkey(line) for line in lines]
    G = {name: params for name, params in monkeys}

    res = dfs(G, "root")
    print(res)
    return


def main2() -> None:
    with open("day21.txt") as fp:
        lines = fp.readlines()

    monkeys = [parse_monkey(line) for line in lines]
    G = {name: params if name != "humn" else 0 for name, params in monkeys}

    root_l, _, root_r = G["root"]

    left = dfs_parse(G, root_l)
    right = eval(dfs_parse(G, root_r))

    res = solve(parse_expr(f"{left} - {right}"), x)
    print(res)

    return


def dfs(G, name: str):
    node = G[name]

    if isinstance(node, int):
        return node

    l_name, op, r_name = node
    left = dfs(G, l_name)
    right = dfs(G, r_name)
    res = eval(f"{left} {op} {right}")
    return res


def dfs_parse(G, name: str):
    node = G[name]

    if name == "humn":
        return "x"

    if isinstance(node, int):
        return node

    l_name, op, r_name = node
    left = dfs_parse(G, l_name)
    right = dfs_parse(G, r_name)
    res = f"({left} {op} {right})"
    return res


def parse_monkey(desc: str):
    number_pat = re.compile(r"(\w+): (\d+)")
    if num_match := number_pat.search(desc):
        name, num_str = num_match.groups()
        return name, int(num_str)

    op_pat = re.compile(r"(\w+): (\w+) (.) (\w+)")
    if op_match := op_pat.search(desc):
        name, left, op, right = op_match.groups()
        return name, (left, op, right)

    raise ValueError("Invalid Input")


if __name__ == "__main__":
    main()
    main2()
