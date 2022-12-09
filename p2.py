from typing import Literal

OPPONENT_CODE_TO_MOVE = {"A": "ROCK", "B": "PAPER", "C": "SCISSORS"}

MY_CODE_TO_MOVE = {"X": "ROCK", "Y": "PAPER", "Z": "SCISSORS"}
POINTS_FOR_MOVE = {"ROCK": 1, "PAPER": 2, "SCISSORS": 3}

Shape = Literal["ROCK", "PAPER", "SCISSORS"]

test_input = """A Y
B X
C Z"""


def main() -> None:
    with open("aoc2022/rps_input.txt") as fp:
        lines = fp.readlines()

    scores = [get_round_score(line) for line in lines]
    print(sum(scores))
    return


def translate_code_to_shape(round_line: str) -> (Shape, Shape):
    their_play_code, my_play_code = round_line.split()
    return (OPPONENT_CODE_TO_MOVE[their_play_code], MY_CODE_TO_MOVE[my_play_code])


def did_i_win(theirs: Shape, mine: Shape) -> bool:
    if (theirs, mine) in [
        ("ROCK", "SCISSORS"),
        ("PAPER", "ROCK"),
        ("SCISSORS", "PAPER"),
    ]:
        return False
    return True


def get_round_score(round_line: str):
    points = 0
    their_move, my_move = translate_code_to_shape(round_line)

    points += POINTS_FOR_MOVE[my_move]
    if their_move == my_move:
        points += 3
    else:
        points += 6 if did_i_win(their_move, my_move) else 0

    return points


if __name__ == "__main__":
    main()
