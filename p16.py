import re

test_input = """Valve AA has flow rate=0; tunnels lead to valves DD, II, BB
Valve BB has flow rate=13; tunnels lead to valves CC, AA
Valve CC has flow rate=2; tunnels lead to valves DD, BB
Valve DD has flow rate=20; tunnels lead to valves CC, AA, EE
Valve EE has flow rate=3; tunnels lead to valves FF, DD
Valve FF has flow rate=0; tunnels lead to valves EE, GG
Valve GG has flow rate=0; tunnels lead to valves FF, HH
Valve HH has flow rate=22; tunnel leads to valve GG
Valve II has flow rate=0; tunnels lead to valves AA, JJ
Valve JJ has flow rate=21; tunnel leads to valve II
"""


def from_github() -> None:
    with open("day16.txt") as fp:
        lines = fp.readlines()

    # lines = test_input.splitlines()
    parsed_lines = [parse_node(line) for line in lines]

    # pre-processing
    graph = {name: set(neighbors) for (name, _, neighbors) in parsed_lines}
    flows = {name: flow for (name, flow, _) in parsed_lines if flow != 0}
    indicator = {name: 1 << i for i, name in enumerate(flows)}

    # very mathy way to calculate biggest distance between nodes (testing all combos)
    dist = {x: {y: 1 if y in graph[x] else float("+inf") for y in graph} for x in graph}
    for k in dist:
        for i in dist:
            for j in dist:
                dist[i][j] = min(dist[i][j], dist[i][k] + dist[k][j])

    # state variable stores open valves as bits in a binary number
    # the if checks whether they have any bits in common (aka you're on an open valve)
    # and continues, otherwise it does bitwise or later to aggregate such bit
    # equivalent to opening the valve
    # (more complicated than I would like, but faster than an array for sure)

    def visit(source: str, budget: int, state: int, flow: int, answer: dict[str, int]):
        answer[state] = max(answer.get(state, 0), flow)
        for target in flows:
            newbudget = budget - dist[source][target] - 1
            if indicator[target] & state or newbudget <= 0:
                continue

            newstate = state | indicator[target]
            newflow = flow + newbudget * flows[target]
            visit(target, newbudget, newstate, newflow, answer)
        return answer

    total1 = max(visit("AA", 30, 0, 0, {}).values())
    visited2 = visit("AA", 26, 0, 0, {})

    for i in sorted(visited2):
        print(f"{i:b}", visited2[i])

    total2 = max(
        v1 + v2
        for k1, v1 in visited2.items()
        for k2, v2 in visited2.items()
        if not k1 & k2
    )
    print(total1, total2)


def main() -> None:
    from_github()
    return


def parse_node(line: str) -> (str, int, list[str]):
    pattern = re.compile(r"Valve (\w\w).+rate=(\d{1,2});.+? ([A-Z, ]+)")
    match = pattern.search(line)
    if not match:
        raise ValueError("bloa")
    name, flow_rate, neighbor_label_list = match.groups()
    neighbors = neighbor_label_list.split(", ")
    return name, int(flow_rate), neighbors


if __name__ == "__main__":
    main()
