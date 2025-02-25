from collections import Counter
from itertools import combinations
from pathlib import Path
from queue import PriorityQueue
from time import time

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


def part_1(input_file: str, threshold: int = 100, cheat_size=2):
    global input_data
    data_file = Path(__file__).with_name(input_file).read_text()
    input_data = data_file.split("\n")
    input_data = [[c for c in row] for row in input_data]

    start_pos = get_pos(input_data, "S")
    end_pos = get_pos(input_data, "E")
    dist_base, prev = find_path(start_pos, end_pos)
    path = get_path(prev, end_pos)
    path.append(start_pos)

    useful_cheats = Counter()
    for new_pos, pos in combinations(path, 2):
        # Manhattan distance
        size = abs(pos[0] - new_pos[0]) + abs(pos[1] - new_pos[1])
        if size > cheat_size:
            continue
        better_steps = dist_base[new_pos] - (dist_base[pos] + size)
        if better_steps >= threshold:
            useful_cheats.update([better_steps])

    # print(useful_cheats)
    return useful_cheats.total()


def get_path(prev, end_pos):
    path = []
    while end_pos in prev:
        path.append(end_pos)
        end_pos = prev[end_pos]
    return path


if __name__ == "__main__":
    print("#" * 10 + " Part 1 " + "#" * 10)
    start_time = time()
    result_ex = part_1("input_ex.txt", threshold=12)
    print(result_ex)
    assert result_ex == 8

    result = part_1("input.txt", threshold=100)
    print(result)
    print(f"Part 1 took: {time() - start_time:.2f} seconds")

    # #### Part 2 ####
    start_time = time()
    print("#" * 10 + " Part 2 " + "#" * 10)
    result = part_1("input_ex.txt", threshold=70, cheat_size=20)
    print(result)
    assert result == 41

    result = part_1("input.txt", threshold=100, cheat_size=20)
    print(result)
    print(f"Part 2 took: {time() - start_time:.2f} seconds")
