from typing import Literal

OPPONENT_CODE_TO_MOVE = {"A": "ROCK", "B": "PAPER", "C": "SCISSORS"}
MY_CODE_TO_RESULT = {"X": "LOSE", "Y": "DRAW", "Z": "WIN"}

WIN_AGAINST = {"ROCK": "PAPER", "PAPER": "SCISSORS", "SCISSORS": "ROCK"}
LOSE_TO = {"ROCK": "SCISSORS", "PAPER": "ROCK", "SCISSORS": "PAPER"}

POINTS_FOR_MOVE = {"ROCK": 1, "PAPER": 2, "SCISSORS": 3}

Shape = Literal["ROCK", "PAPER", "SCISSORS"]
Result = Literal["LOSE", "DRAW", "WIN"]

test_input = """A Y
B X
C Z"""


def main() -> None:
    with open("rps_input.txt") as fp:
        lines = fp.readlines()

    scores = [get_round_score(line) for line in lines]
    print(sum(scores))
    return


def translate_codes(round_line: str) -> (Shape, Result):
    their_play_code, result_code = round_line.split()
    return (OPPONENT_CODE_TO_MOVE[their_play_code], MY_CODE_TO_RESULT[result_code])


def calculate_my_move(theirs: Shape, intention: Result) -> Shape:
    if intention == "DRAW":
        return theirs
    elif intention == "WIN":
        return WIN_AGAINST[theirs]
    else:
        return LOSE_TO[theirs]


def get_round_score(round_line: str):
    points = 0
    their_move, my_intention = translate_codes(round_line)
    my_move = calculate_my_move(their_move, my_intention)

    points += POINTS_FOR_MOVE[my_move]
    if my_intention == "DRAW":
        points += 3
    else:
        points += 6 if my_intention == "WIN" else 0
    return points


if __name__ == "__main__":
    main()
