import re
from itertools import permutations
from pathlib import Path
from queue import PriorityQueue

input_data = []

keypad = {
    "7": (0, 0),
    "8": (0, 1),
    "9": (0, 2),
    "4": (1, 0),
    "5": (1, 1),
    "6": (1, 2),
    "1": (2, 0),
    "2": (2, 1),
    "3": (2, 2),
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


def calc_complexity(codes: dict[str, str]) -> int:
    complexity = [
        len(sequence) * int(re.sub(r"[A-Z]", "", code))
        for code, sequence in codes.items()
    ]
    return sum(complexity)


keypad_show = [
    ["7", "8", "9"],
    ["4", "5", "6"],
    ["1", "2", "3"],
    ["", "0", "A"],
]
dirpad_show = [
    ["", "^", "A"],
    ["<", "v", ">"],
]

shortest_keypad = {}
shortest_dirpad = {}


def get_dir2keypad_inputs(code: str) -> list[str]:
    cur_pos = (3, 2)
    possible_paths = [""]
    for c in code:
        next_move = keypad[c]
        ways = shortest_keypad[(next_move, cur_pos)]
        possible_paths = [
            old_path + way + "A" for old_path in possible_paths for way in ways
        ]
        cur_pos = next_move
    return possible_paths


def get_dir2dirpad_inputs(code: str) -> list[str]:
    cur_pos = (0, 2)
    possible_paths = [""]
    for c in code:
        next_move = dirpad[c]
        if next_move == cur_pos:
            possible_paths = [old_path + "A" for old_path in possible_paths]
        else:
            ways = shortest_dirpad[(next_move, cur_pos)]
            possible_paths = [
                old_path + way + "A" for old_path in possible_paths for way in ways
            ]
        cur_pos = next_move
    return possible_paths


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


def get_paths(
    start: tuple[int, int], end: tuple[int, int], pad: dict[str, tuple[int, int]]
) -> list[str]:
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
            if new_pos not in pad.values():
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


def is_optimal(sequence: str) -> bool:
    for sub_seq in sequence.split("A"):
        for i, char in enumerate(sub_seq):
            other_char_between = False
            for next_char in sub_seq[i + 1 :]:
                if char != next_char:
                    other_char_between = True
                if char == next_char and other_char_between:
                    return False
    return True


def optimize_paths(paths: list[str]) -> list[str]:
    """Remove paths that are not optimal.
    Those that have the same directions together. Only keep those that have the shortest length.
    """
    path_len = [len(p) for p in paths]
    min_len = min(path_len)
    optimal_paths = [path for path, length in zip(paths, path_len) if length == min_len]

    # TODO remove those with the same directions not together
    optimal_paths = [p for p in optimal_paths if is_optimal(p)]
    return optimal_paths


def move(start_move: str, end_move: str, pad: dict[str, tuple[int, int]]) -> str:
    start_pos = pad[start_move]
    end_pos = pad[end_move]
    d_y = start_pos[0] - end_pos[0]
    d_x = start_pos[1] - end_pos[1]
    vert_move = "^" * d_y + "v" * -d_y
    hor_move = "<" * d_x + ">" * -d_x
    # When moving left: check if the tile that is moved over exists
    if "<" in hor_move and (start_pos[0], end_pos[1]) not in pad.values():
        moves = vert_move + hor_move
    # elif ">" in hor_move and start_pos[1] == 0:
    #     moves = hor_move + vert_move
    else:
        moves = hor_move + vert_move
    return moves + "A"


def enter_code(code: str, pad: dict[str, tuple[int, int]]) -> str:
    cur_char = "A"
    sequence = ""
    for next_char in code:
        sequence += move(cur_char, next_char, pad)
        cur_char = next_char
    return sequence


def part_1(input_file: str, dir_pads: int = 3):
    global input_data
    data_file = Path(__file__).with_name(input_file).read_text()
    input_data = data_file.split("\n")
    codes = {}

    for start, end in permutations(keypad.values(), 2):
        new_paths = get_paths(start, end, keypad)
        new_paths_optimized = optimize_paths(new_paths)
        shortest_keypad[(start, end)] = new_paths_optimized
        # TODO optimize here: prefer those that have the same directions together

    for start, end in permutations(dirpad.values(), 2):
        new_paths = get_paths(end, start, dirpad)
        new_paths_optimized = optimize_paths(new_paths)
        shortest_dirpad[(start, end)] = new_paths_optimized
    codes = {code: None for code in input_data}

    best_paths = {}
    for code in codes.keys():
        cur_codes = get_dir2keypad_inputs(code)

        for i in range(dir_pads):
            print(i, len(cur_codes))
            new_codes = []
            for j, c in enumerate(cur_codes):
                print(f"{j/len(cur_codes):.2%}", end="\r")
                new_codes.extend(get_dir2dirpad_inputs(c))
            cur_codes = optimize_paths(new_codes)
        best_paths[code] = cur_codes

    complexity = calc_complexity(codes)

    complexity = sum(code * length for code, length in codes.items())
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
    assert result < 192842

    # #### Part 2 ####
    print("#" * 10 + " Part 2 " + "#" * 10)
    result = part_2("input_ex.txt")
    print(result)
    assert result == 1337

    result = part_2("input.txt")
    print(result)
