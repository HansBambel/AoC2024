import re
from pathlib import Path

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

    for code in input_data:
        cur_code = enter_code(code, keypad)
        for _ in range(dir_pads - 1):
            cur_code = enter_code(cur_code, dirpad)
        codes[int(code[:-1])] = len(cur_code)

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
