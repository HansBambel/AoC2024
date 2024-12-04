from pathlib import Path


def check_direction(
    puzzle, to_find: str, pos: tuple[int, int], direction: tuple[int, int]
) -> bool:
    if to_find == "":
        return True
    if (
        (pos[0] < 0)
        or (pos[1] < 0)
        or (pos[0] >= len(puzzle))
        or (pos[1] >= len(puzzle[0]))
    ):
        return False
    if puzzle[pos[0]][pos[1]] == to_find[0]:
        new_pos = (pos[0] + direction[0], pos[1] + direction[1])
        return check_direction(puzzle, to_find[1:], new_pos, direction)
    return False


def is_xmas(puzzle, pos: tuple[int, int]) -> int:
    if (
        (pos[0] < 0)
        or (pos[1] < 0)
        or (pos[0] >= len(puzzle))
        or (pos[1] >= len(puzzle[0]))
    ):
        return 0
    to_find = "XMAS"
    found = 0
    for vert in range(-1, 2):
        for hori in range(-1, 2):
            if (vert == 0) and (hori == 0):
                continue
            found += check_direction(puzzle, to_find, (pos[0], pos[1]), (vert, hori))
    return found


def is_x_mas(puzzle, pos: tuple[int, int]) -> bool:
    if (
        (pos[0] - 1 < 0)
        or (pos[1] - 1 < 0)
        or (pos[0] + 1 >= len(puzzle))
        or (pos[1] + 1 >= len(puzzle[0]))
    ):
        return False
    top_left = puzzle[pos[0] - 1][pos[1] - 1]
    bottom_right = puzzle[pos[0] + 1][pos[1] + 1]
    top_right = puzzle[pos[0] - 1][pos[1] + 1]
    bottom_left = puzzle[pos[0] + 1][pos[1] - 1]
    return {"A", top_left, bottom_right} == set("MAS") and {
        "A",
        top_right,
        bottom_left,
    } == set("MAS")


def part_1(input_file: str):
    data_file = Path(__file__).with_name(input_file).read_text()
    puzzle = data_file.split("\n")

    total = 0
    for y, line in enumerate(puzzle):
        for x, char in enumerate(line):
            if char != "X":
                continue
            total += is_xmas(puzzle, (y, x))

    return total


def part_2(input_file: str):
    data_file = Path(__file__).with_name(input_file).read_text()
    puzzle = data_file.split("\n")

    total = 0
    for y, line in enumerate(puzzle):
        for x, char in enumerate(line):
            if char != "A":
                continue
            total += is_x_mas(puzzle, (y, x))

    return total


if __name__ == "__main__":
    print("#" * 10 + " Part 1 " + "#" * 10)
    result_ex = part_1("input_ex.txt")
    print(result_ex)
    assert result_ex == 18

    result = part_1("input.txt")
    print(result)

    # #### Part 2 ####
    print("#" * 10 + " Part 2 " + "#" * 10)
    result = part_2("input_ex.txt")
    print(result)
    assert result == 9

    result = part_2("input.txt")
    print(result)
