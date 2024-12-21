import re
from itertools import permutations
from pathlib import Path
from queue import PriorityQueue

input_data = []
keypad_show = [
    ["7", "8", "9"],
    ["4", "5", "6"],
    ["3", "2", "1"],
    ["", "0", "A"],
]
keypad = {
    "7": (0, 0),
    "8": (0, 1),
    "9": (0, 2),
    "4": (1, 0),
    "5": (1, 1),
    "6": (1, 2),
    "3": (2, 0),
    "2": (2, 1),
    "1": (2, 2),
    "0": (3, 1),
    "A": (3, 2),
}
dirpad = {
    "^": (0, 1),
    "A": (0, 2),
    "<": (1, 0),
    "v": (1, 1),
    ">": (1, 2),
}

shortest_keypad = {}


def calc_complexity(codes: dict[str, str]) -> int:
    complexity = [
        len(sequence) * int(re.sub(r"[A-Z]", "", code))
        for code, sequence in codes.items()
    ]
    return sum(complexity)


def get_directional_inputs(code: str) -> list[str]:
    cur_pos = (3, 2)


def get_path(
    prev: dict[tuple[int, int], list[tuple[tuple[int, int], str]]],
    cur: tuple[int, int],
    start_pos: tuple[int, int],
) -> list[str]:
    path = []
    moves = prev[cur]
    for pos, move in moves:
        if pos != start_pos:
            next_paths = get_path(prev, pos, start_pos)
        else:
            next_paths = [""]
        path.extend([move + next_path for next_path in next_paths])
    return path


def get_paths(start: tuple[int, int], end: tuple[int, int]) -> list[str]:
    seen = set()
    prev = {}
    dist = {start: 0}
    queue = PriorityQueue()
    queue.put((0, start))
    while not queue.empty():
        _, next_move = queue.get()
        seen.add(next_move)
        y, x = next_move
        for (dy, dx), move in [
            ((-1, 0), "v"),
            ((1, 0), "^"),
            ((0, -1), ">"),
            ((0, 1), "<"),
        ]:
            new_pos = (y + dy, x + dx)
            new_score = dist[next_move] + 1
            if new_pos not in keypad.values():
                continue

            if new_score < dist.get(new_pos, 1e9):
                dist[new_pos] = new_score
                prev[new_pos] = [(next_move, move)]
                queue.put((new_score, new_pos))
            elif new_score == dist[new_pos]:
                prev[new_pos].append((next_move, move))

    # Concat the paths
    paths = get_path(prev, end, start)
    return paths


def part_1(input_file: str):
    global input_data
    global shortest_keypad
    data_file = Path(__file__).with_name(input_file).read_text()
    input_data = data_file.split("\n")

    for start, end in permutations(keypad.values(), 2):
        shortest_keypad[(start, end)] = get_paths(end, start)
    codes = {code: None for code in input_data}

    best_paths = {}
    for code in codes.keys():
        best_paths[code] = get_directional_inputs(code)

    # do X directional inputs
    for code in codes.keys():
        pass

    complexity = calc_complexity(codes)
    return complexity


def part_2(input_file: str):
    global input_data
    data_file = Path(__file__).with_name(input_file).read_text()
    input_data = data_file.split("\n")


if __name__ == "__main__":
    print("#" * 10 + " Part 1 " + "#" * 10)
    result_ex = part_1("input_ex.txt")
    print(result_ex)
    assert result_ex == 126384

    result = part_1("input.txt")
    print(result)

    # #### Part 2 ####
    print("#" * 10 + " Part 2 " + "#" * 10)
    result = part_2("input_ex.txt")
    print(result)
    assert result == 1337

    result = part_2("input.txt")
    print(result)
