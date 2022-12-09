import dataclasses
import re

test_input = """    [D]    
[N] [C]    
[Z] [M] [P]
 1   2   3

move 1 from 2 to 1
move 3 from 1 to 3
move 2 from 2 to 1
move 1 from 1 to 2"""


@dataclasses.dataclass
class MoveInstruction:
    number_of_blocks: int
    from_i: int
    to_i: int


def main() -> None:
    with open("day5.txt") as fp:
        lines = fp.read()
    stack_lines, instruction_lines = lines.split("\n\n")

    # translating to data-structures
    instructions = [parse_instruction(line) for line in instruction_lines.splitlines()]
    stacks = parse_stack(stack_lines.splitlines())

    for instruction in instructions:
        execute_in_place_9001(stacks, instruction)

    top_of_stacks = [stack.pop() for stack in stacks if len(stack) > 0]
    print("".join(top_of_stacks))
    return


def execute_in_place_9000(stacks: list[list[str]], inst: MoveInstruction) -> None:
    for _ in range(inst.number_of_blocks):
        block_being_moved = stacks[inst.from_i].pop()
        stacks[inst.to_i].append(block_being_moved)
    return


def execute_in_place_9001(stacks: list[list[str]], inst: MoveInstruction) -> None:
    # equivalent to popping however many blocks from list
    block_being_moved = stacks[inst.from_i][-inst.number_of_blocks :]
    del stacks[inst.from_i][-inst.number_of_blocks :]

    stacks[inst.to_i].extend(block_being_moved)
    return


def parse_stack(stack_lines: list[str]) -> list[list[str]]:
    stacks = [[] for i in range(9)]
    for line in stack_lines:
        for i, ch in enumerate(line):
            if ch.isalpha():
                stacks[i // 4].insert(0, ch)
    return stacks


def parse_instruction(instruction_line: str) -> MoveInstruction:
    re_pattern = re.compile(r"move (\d{1,2}) from (\d) to (\d)")
    res = re.search(re_pattern, instruction_line)
    if res is None:
        raise ValueError(f"Could not parse intruction: {instruction_line}")

    number_str, from_str, to_str = res.groups()
    return MoveInstruction(int(number_str), int(from_str) - 1, int(to_str) - 1)


if __name__ == "__main__":
    main()
