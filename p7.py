test_input = """$ cd /
$ ls
dir a
14848514 b.txt
8504156 c.dat
dir d
$ cd a
$ ls
dir e
29116 f
2557 g
62596 h.lst
$ cd e
$ ls
584 i
$ cd ..
$ cd ..
$ cd d
$ ls
4060174 j
8033020 d.log
5626152 d.ext
7214296 k"""


class Directory:
    def __init__(self, name: str, parent: "Directory" = None) -> None:
        self.name = name
        self.contents = []
        self.parent = parent
        return

    @property
    def size(self) -> int:
        return sum([file.size for file in self.contents])

    def __repr__(self) -> str:
        return f"/{self.name} ({self.size:,})"


class File:
    def __init__(self, name: str, size: int) -> None:
        self.name = name
        self.size = size
        return


def main() -> None:
    with open("day7.txt") as fp:
        lines = fp.read()

    blocks = [block.strip().splitlines() for block in lines.split("$") if block]

    root_dir = Directory("/")
    current_directory = None

    for block in blocks:
        cmd, *output = block

        if cmd == "ls":
            contents = parse_ls_output(output, current_directory)
            current_directory.contents = contents
        elif cmd == "cd ..":
            current_directory = current_directory.parent
        elif cmd == "cd /":
            current_directory = root_dir
        elif cmd.startswith("cd "):
            dir_name = cmd[3:]
            for file in current_directory.contents:
                if type(file) == Directory and file.name == dir_name:
                    current_directory = file

    total_size = 70_000_000
    root_size = root_dir.size
    update_size = 30_000_000
    space_to_free = update_size - (total_size - root_size)

    print(sum([dir.size for dir in find_small_directories(root_dir, 100_000)]))
    # print(find_big_enough_directories(root_dir, space_to_free))
    print(
        min(
            find_big_enough_directories(root_dir, space_to_free), key=lambda x: x.size
        ).size
    )
    return


def pretty_print(filelike, indent: int = 0) -> str:
    if type(filelike) == File:
        return f"{'  ' * indent}- {filelike.name} (file, size={filelike.size})"

    return "\n".join(
        [
            f"{'  ' * indent}- {filelike.name} (dir)",
            *[pretty_print(file, indent=indent + 1) for file in filelike.contents],
        ]
    )


def parse_ls_output(output: list[str], current_directory: Directory):
    files = []

    for line in output:
        if line.startswith("dir"):
            files.append(Directory(line[4:], current_directory))
            continue

        size_str, name = line.split()
        files.append(File(name, int(size_str)))
    return files


def find_small_directories(root_dir: Directory, threshold: int) -> list[Directory]:
    found = [root_dir] if root_dir.size <= threshold else []
    for filelike in root_dir.contents:
        if not isinstance(filelike, Directory):
            continue

        found.extend(find_small_directories(filelike, threshold))
    return found


def find_big_enough_directories(root_dir: Directory, threshold: int) -> list[Directory]:
    found = [root_dir] if root_dir.size >= threshold else []
    for filelike in root_dir.contents:
        if not isinstance(filelike, Directory):
            continue

        found.extend(find_big_enough_directories(filelike, threshold))
    return found


if __name__ == "__main__":
    main()
