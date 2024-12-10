from pathlib import Path

input_data: list[list[int]] = [[]]
can_reach = {}


def get_trailheads(visited: list[tuple[int, int]], distinct_paths: bool = False) -> int:
    pos = visited[-1]
    if input_data[pos[0]][pos[1]] == 9:
        if distinct_paths:
            return 1
        start = visited[0]
        if pos in can_reach.get(start, []):
            return 0
        else:
            can_reach[start] = can_reach.get(start, []) + [pos]
            return 1

    trailheads = 0
    current = input_data[pos[0]][pos[1]]
    for y, x in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        if (
            pos[0] + y < 0
            or pos[1] + x < 0
            or pos[0] + y >= len(input_data)
            or pos[1] + x >= len(input_data[0])
        ):
            continue
        if input_data[pos[0] + y][pos[1] + x] == current + 1:
            trailheads += get_trailheads(
                visited + [(pos[0] + y, pos[1] + x)], distinct_paths=distinct_paths
            )
    return trailheads


def part_1(input_file: str, part2: bool = False) -> int:
    global input_data
    data_file = Path(__file__).with_name(input_file).read_text()
    input_data = [[int(c) for c in line] for line in data_file.split("\n")]
    starts = []
    for y, line in enumerate(input_data):
        for x, start in enumerate(line):
            if input_data[y][x] == 0:
                starts.append((y, x))
    trailheads = []
    for start in starts:
        trailheads.append(get_trailheads([start], distinct_paths=part2))
    return sum(trailheads)


def part_2(input_file: str):
    return part_1(input_file, part2=True)


if __name__ == "__main__":
    print("#" * 10 + " Part 1 " + "#" * 10)
    result_ex = part_1("input_ex2.txt")
    print(result_ex)
    assert result_ex == 1
    result_ex = part_1("input_ex.txt")
    print(result_ex)
    assert result_ex == 36

    result = part_1("input.txt")
    print(result)

    # #### Part 2 ####
    can_reach = {}
    print("#" * 10 + " Part 2 " + "#" * 10)
    result = part_2("input_ex.txt")
    print(result)
    assert result == 81

    result = part_2("input.txt")
    print(result)
