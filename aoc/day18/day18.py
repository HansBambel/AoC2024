from pathlib import Path
from queue import PriorityQueue

input_data = []


def find_path(start_pos, end_pos, blocked):
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
        options: list[tuple[int, int]] = [(0, 1), (0, -1), (1, 0), (-1, 0)]

        for dir in options:
            new_pos = (x + dir[0], y + dir[1])
            new_score = dist[next_move] + 1
            if new_pos in blocked:
                continue
            if new_pos in seen:
                continue
            if (
                new_pos[0] < 0
                or new_pos[1] < 0
                or new_pos[0] >= end_pos[0] + 1
                or new_pos[1] >= end_pos[1] + 1
            ):
                continue

            if dist.get(new_pos, 1e9) > new_score:
                dist[new_pos] = new_score
                prev[new_pos] = next_move
                queue.put((new_score, new_pos))
            # elif new_score == dist[new_pos]:
            #     prev[new_pos].append(next_move)
    return dist, prev


def get_path(prev, end_pos):
    path = []
    while end_pos in prev:
        path.append(end_pos)
        end_pos = prev[end_pos]
    return path


def print_path(prev, blocked, end_pos):
    path = get_path(prev, end_pos)
    for y in range(end_pos[1] + 1):
        for x in range(end_pos[0] + 1):
            if (x, y) in path:
                print("O", end="")
            elif (x, y) in blocked:
                print("#", end="")
            else:
                print(".", end="")
        print()


def part_1(input_file: str, end_pos=(6, 6), start_after=1024):
    global input_data
    data_file = Path(__file__).with_name(input_file).read_text()
    input_data = data_file.split("\n")
    input_data = [list(map(int, row.split(","))) for row in input_data]
    start_pos = (0, 0)
    blocked = [tuple(pos) for pos in input_data[:start_after]]
    dist, prev = find_path(start_pos, end_pos, blocked)

    # print_path(prev, blocked, end_pos)
    return dist[end_pos]


def part_2(input_file: str, end_pos=(6, 6), start_after=1024):
    global input_data
    data_file = Path(__file__).with_name(input_file).read_text()
    input_data = data_file.split("\n")
    input_data = [list(map(int, row.split(","))) for row in input_data]
    start_pos = (0, 0)

    last_ind = len(input_data) - 1
    begin_ind = start_after
    middle = begin_ind + (last_ind - begin_ind) // 2
    old = -1
    while begin_ind <= last_ind:
        middle = begin_ind + (last_ind - begin_ind) // 2
        blocked = [tuple(pos) for pos in input_data[:middle]]
        dist, prev = find_path(start_pos, end_pos, blocked)
        if end_pos in prev:
            begin_ind = middle
        else:
            last_ind = middle
        if old == middle:
            break
        old = middle
    return str(input_data[middle][0]) + "," + str(input_data[middle][1])


if __name__ == "__main__":
    print("#" * 10 + " Part 1 " + "#" * 10)
    result_ex = part_1("input_ex.txt", end_pos=(6, 6), start_after=12)
    print(result_ex)
    assert result_ex == 22

    result = part_1("input.txt", end_pos=(70, 70), start_after=1024)
    print(result)

    # #### Part 2 ####
    print("#" * 10 + " Part 2 " + "#" * 10)
    result_ex = part_2("input_ex.txt", end_pos=(6, 6), start_after=12)
    print(result_ex)
    assert result_ex == "6,1"

    # Takes about 5min to run
    result = part_2("input.txt", end_pos=(70, 70), start_after=1024)
    print(result)
