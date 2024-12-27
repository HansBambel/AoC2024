import re
from functools import cache
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


def calc_complexity(codes: dict[str, list[str]]) -> int:
    complexity = [
        len(sequence[0]) * int(re.sub(r"[A-Z]", "", code))
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
        ways = shortest_keypad[(cur_pos, next_move)]
        possible_paths = [
            old_path + way + "A" for old_path in possible_paths for way in ways
        ]
        cur_pos = next_move
    return possible_paths


@cache
def get_dir2dirpad_inputs(code: str, depth: int) -> int:
    if depth == 0:
        return len(code)
    cur_pos = (0, 2)
    total_length = 0
    for sub_code in code.split("A"):
        for c in sub_code + "A":
            next_move = dirpad[c]
            if cur_pos == next_move:
                ways = [""]
            else:
                ways = shortest_dirpad[(next_move, cur_pos)]
            shortest = 1e128
            for way in ways:
                new_code = way + "A"
                shortest = min(shortest, get_dir2dirpad_inputs(new_code, depth - 1))
            total_length += shortest
            cur_pos = next_move
    return total_length - 1


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


@cache
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

    # remove those with the same directions not together
    optimal_paths = [p for p in optimal_paths if is_optimal(p)]
    return optimal_paths


def part_1(input_file: str, dir_pads: int = 3):
    global input_data
    data_file = Path(__file__).with_name(input_file).read_text()
    input_data = data_file.split("\n")

    for start, end in permutations(keypad.values(), 2):
        new_paths = get_paths(start, end, keypad)
        new_paths_optimized = optimize_paths(new_paths)
        shortest_keypad[(end, start)] = new_paths_optimized

    for start, end in permutations(dirpad.values(), 2):
        new_paths = get_paths(end, start, dirpad)
        new_paths_optimized = optimize_paths(new_paths)
        shortest_dirpad[(end, start)] = new_paths_optimized

    total_complexity = {}
    for code in input_data:
        cur_codes = get_dir2keypad_inputs(code)

        min_length = 1e128
        for cur_code in cur_codes:
            seq_len = get_dir2dirpad_inputs(cur_code, dir_pads - 1)
            min_length = min(min_length, seq_len)
        total_complexity[code] = int(re.sub(r"[A-Z]", "", code)) * min_length

    print(total_complexity)
    return sum(total_complexity.values())


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

    result = part_1("input.txt", dir_pads=26)
    print(result)
    assert result > 92477346276378
