test_input = "mjqjpqmgbljsphdztnvjfqwrcgsmlb"


def main() -> None:
    with open("day6.txt") as fp:
        lines = fp.read()

    print(find_start_of_packet_marker(lines))
    print(find_start_of_message_market(lines))
    return


def find_start_of_packet_marker(message: str) -> int:
    window = message[0:4]
    if len(set(window)) == 4:
        return 4  # early return

    for i, ch in enumerate(message[4:], 5):
        window = window[1:] + ch
        if len(set(window)) == 4:
            return i
    return -1


def find_start_of_message_market(message: str) -> int:
    window = message[0:14]
    if len(set(window)) == 14:
        return 4  # early return

    for i, ch in enumerate(message[14:], 15):
        window = window[1:] + ch
        if len(set(window)) == 14:
            return i
    return -1


if __name__ == "__main__":
    main()
