from pathlib import Path
from queue import PriorityQueue

input_data = []


def find_path(start_pos, end_pos):
    options: list[tuple[int, int]] = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    seen = set()
    prev = {}
    dist = {start_pos: 0}
    queue = PriorityQueue()
    queue.put((0, start_pos))

    while not queue.empty():
        _, next_move = queue.get()
        seen.add(next_move)
        x, y = next_move
        if next_move == end_pos:
            break

        for dir in options:
            new_pos = (x + dir[0], y + dir[1])
            new_score = dist[next_move] + 1
            if new_pos in seen:
                continue
            if (
                new_pos[0] < 0
                or new_pos[1] < 0
                or new_pos[0] >= len(input_data)
                or new_pos[1] >= len(input_data[0])
                or input_data[new_pos[0]][new_pos[1]] == "#"
            ):
                continue

            if dist.get(new_pos, 1e9) > new_score:
                dist[new_pos] = new_score
                prev[new_pos] = next_move
                queue.put((new_score, new_pos))
            # elif new_score == dist[new_pos]:
            #     prev[new_pos].append(next_move)
    return dist, prev


def get_pos(input_data: list[list[str]], character: str = "S") -> tuple[int, int]:
    for y, row in enumerate(input_data):
        for x, col in enumerate(row):
            if col == character:
                return y, x


def part_1(input_file: str, threshold: int = 100):
    global input_data
    data_file = Path(__file__).with_name(input_file).read_text()
    input_data = data_file.split("\n")
    input_data = [[c for c in row] for row in input_data]

    start_pos = get_pos(input_data, "S")
    end_pos = get_pos(input_data, "E")
    dist_base, _ = find_path(start_pos, end_pos)
    base_line = dist_base[end_pos]

    best_cases = []
    for y, row in enumerate(input_data[1:-1], 1):
        for x, col in enumerate(row[1:-1], 1):
            if col != "#":
                continue
            input_data[y][x] = "."
            dist, _ = find_path(start_pos, end_pos)
            if base_line > dist[end_pos]:
                best_cases.append(base_line - dist[end_pos])
            input_data[y][x] = "#"

    return sum(1 for case in best_cases if case >= threshold)


def part_2(input_file: str):
    global input_data
    data_file = Path(__file__).with_name(input_file).read_text()
    input_data = data_file.split("\n")


if __name__ == "__main__":
    print("#" * 10 + " Part 1 " + "#" * 10)
    result_ex = part_1("input_ex.txt", 12)
    print(result_ex)
    assert result_ex == 8

    result = part_1("input.txt")
    print(result)

    # #### Part 2 ####
    print("#" * 10 + " Part 2 " + "#" * 10)
    result = part_2("input_ex.txt")
    print(result)
    assert result == 1337

    result = part_2("input.txt")
    print(result)
