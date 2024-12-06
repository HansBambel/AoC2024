from pathlib import Path


order = {"^": ">", ">": "v", "v": "<", "<": "^"}
directions = {">": (0, 1), "v": (1, 0), "<": (0, -1), "^": (-1, 0)}


def get_start_pos(data: list[str]) -> tuple[int, int]:
    for y, row in enumerate(data):
        for x, pos in enumerate(row):
            if pos in order.keys():
                return (y, x)
    raise ValueError("no start found")


def part_1(input_file: str):
    data_file = Path(__file__).with_name(input_file).read_text()
    input_data = data_file.split("\n")
    cur_pos = get_start_pos(input_data)
    visited = {cur_pos}
    facing = input_data[cur_pos[0]][cur_pos[1]]
    direction = directions[facing]
    while (
        cur_pos[0] + direction[0] >= 0
        and cur_pos[0] + direction[0] < len(input_data)
        and cur_pos[1] + direction[1] >= 0
        and cur_pos[1] + direction[1] < len(input_data[0])
    ):
        y_new, x_new = cur_pos[0] + direction[0], cur_pos[1] + direction[1]
        if input_data[y_new][x_new] == "#":
            facing = order[facing]
            direction = directions[facing]
            continue

        cur_pos = (y_new, x_new)
        visited.add(cur_pos)

    return len(visited)


def is_loop(input_data, facing, cur_pos) -> bool:
    visited = {(facing, cur_pos)}
    direction = directions[facing]

    while (
        cur_pos[0] + direction[0] >= 0
        and cur_pos[0] + direction[0] < len(input_data)
        and cur_pos[1] + direction[1] >= 0
        and cur_pos[1] + direction[1] < len(input_data[0])
    ):
        y_new, x_new = cur_pos[0] + direction[0], cur_pos[1] + direction[1]
        if input_data[y_new][x_new] == "#":
            facing = order[facing]
            direction = directions[facing]
            continue

        cur_pos = (y_new, x_new)
        if (facing, cur_pos) in visited:
            return True
        visited.add((facing, cur_pos))
    return False


def part_2(input_file: str):
    data_file = Path(__file__).with_name(input_file).read_text()
    input_data = data_file.split("\n")
    cur_pos = get_start_pos(input_data)
    facing = input_data[cur_pos[0]][cur_pos[1]]
    loops = 0
    for y, row in enumerate(input_data):
        for x, item in enumerate(row):
            if item == "#":
                continue
            input_data[y] = row[:x] + "#" + row[x + 1 :]
            loops += is_loop(input_data, facing, cur_pos)
            input_data[y] = row[:x] + "." + row[x + 1 :]

    return loops


if __name__ == "__main__":
    print("#" * 10 + " Part 1 " + "#" * 10)
    result_ex = part_1("input_ex.txt")
    print(result_ex)
    assert result_ex == 41

    result = part_1("input.txt")
    print(result)

    # #### Part 2 ####
    print("#" * 10 + " Part 2 " + "#" * 10)
    result = part_2("input_ex.txt")
    print(result)
    assert result == 6

    result = part_2("input.txt")
    assert result > 1573
    print(result)
