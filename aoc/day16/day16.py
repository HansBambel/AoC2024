from pathlib import Path
from queue import PriorityQueue
from typing import Literal

input_data = []
seen = {}


def get_pos(input_data: list[str], character: str = "S") -> tuple[int, int]:
    for y, row in enumerate(input_data):
        for x, col in enumerate(row):
            if col == character:
                return y, x


def walk(
    start_pos: tuple[int, int],
    facing: Literal["^", "v", "<", ">"],
    goal: tuple[int, int],
) -> tuple[int, dict, str]:
    global input_data
    seen = set()
    prev = {}
    dist = {(start_pos, facing): 0}
    queue = PriorityQueue()
    queue.put((0, start_pos, facing))
    while not queue.empty():
        _, next_move, facing = queue.get()
        seen.add((next_move, facing))
        y, x = next_move
        if next_move == goal:
            break
        options: list[tuple[tuple[int, int], Literal["^", "v", "<", ">"], int]] = []
        match facing:
            case "^":
                options = [((-1, 0), "^", 1), ((0, 0), ">", 1000), ((0, 0), "<", 1000)]
            case "v":
                options = [((1, 0), "v", 1), ((0, 0), ">", 1000), ((0, 0), "<", 1000)]
            case "<":
                options = [((0, -1), "<", 1), ((0, 0), "v", 1000), ((0, 0), "^", 1000)]
            case ">":
                options = [((0, 1), ">", 1), ((0, 0), "v", 1000), ((0, 0), "^", 1000)]
        for dir, face, score in options:
            new_pos = (y + dir[0], x + dir[1])
            new_score = dist[(next_move, facing)] + score
            if input_data[new_pos[0]][new_pos[1]] == "#":
                continue
            if (new_pos, face) in seen:
                continue
            if (
                new_pos[0] < 0
                or new_pos[1] < 0
                or new_pos[0] >= len(input_data)
                or new_pos[1] >= len(input_data[0])
            ):
                continue

            if dist.get((new_pos, face), 1e9) > new_score:
                dist[(new_pos, face)] = new_score
                prev[(new_pos, face)] = next_move, facing
                queue.put((new_score, new_pos, face))
    smallest = dist[(goal, facing)]
    return smallest, prev, facing


def part_1(input_file: str):
    global input_data
    data_file = Path(__file__).with_name(input_file).read_text()
    input_data = data_file.split("\n")
    cur_pos = get_pos(input_data, "S")
    goal = get_pos(input_data, "E")
    score, _, _ = walk(cur_pos, ">", goal)
    return score


def part_2(input_file: str):
    global input_data
    data_file = Path(__file__).with_name(input_file).read_text()
    input_data = data_file.split("\n")
    cur_pos = get_pos(input_data, "S")
    goal = get_pos(input_data, "E")
    _, prev, facing = walk(cur_pos, ">", goal)
    path = []
    cur = goal
    while cur != cur_pos:
        path.append(cur)
        cur, facing = prev[cur, facing]
    return len(list(set(path)))


if __name__ == "__main__":
    print("#" * 10 + " Part 1 " + "#" * 10)
    result_ex = part_1("input_ex.txt")
    print(result_ex)
    assert result_ex == 7036
    result_ex = part_1("input_ex2.txt")
    print(result_ex)
    assert result_ex == 11048
    result_ex = part_1("input_ex3.txt")
    print(result_ex)
    assert result_ex == 21148
    result_ex = part_1("input_ex4.txt")
    print(result_ex)
    assert result_ex == 5078
    result_ex = part_1("input_ex5.txt")
    print(result_ex)
    assert result_ex == 41210

    result = part_1("input.txt")
    print(result)
    assert result > 105483

    # #### Part 2 ####
    print("#" * 10 + " Part 2 " + "#" * 10)
    result = part_2("input_ex.txt")
    print(result)
    assert result == 45
    result_ex = part_2("input_ex2.txt")
    print(result_ex)
    assert result_ex == 64

    result = part_2("input.txt")
    print(result)