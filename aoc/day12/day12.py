from pathlib import Path

input_data = [[]]
seen = set()


def count_size_and_edges_of_area(pos: tuple[int, int], letter: str) -> tuple[int, int]:
    global input_data
    global seen
    seen.add(pos)
    edges = 0
    size = 1
    for y, x in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        new_pos = (pos[0] + y, pos[1] + x)
        if (
            new_pos[0] < 0
            or new_pos[1] < 0
            or new_pos[0] >= len(input_data)
            or new_pos[1] >= len(input_data[0])
        ):
            edges += 1
            continue
        if input_data[new_pos[0]][new_pos[1]] == letter:
            if new_pos in seen:
                continue
            new_size, new_edges = count_size_and_edges_of_area(
                (new_pos[0], new_pos[1]), letter
            )
            edges += new_edges
            size += new_size
        else:
            edges += 1
    return size, edges


def count_size_and_sides_of_area(
    pos: tuple[int, int], letter: str
) -> tuple[int, set[tuple[int, int, str]]]:
    global input_data
    global seen
    seen.add(pos)
    sides = set()
    size = 1
    for y, x, dir in [(-1, 0, "^"), (1, 0, "v"), (0, -1, "<"), (0, 1, ">")]:
        new_pos = (pos[0] + y, pos[1] + x)
        if (
            new_pos[0] < 0
            or new_pos[1] < 0
            or new_pos[0] >= len(input_data)
            or new_pos[1] >= len(input_data[0])
        ):
            sides.add((pos[0], pos[1], dir))
            continue
        if input_data[new_pos[0]][new_pos[1]] == letter:
            if new_pos in seen:
                continue
            new_size, new_sides = count_size_and_sides_of_area(
                (new_pos[0], new_pos[1]), letter
            )
            sides = sides.union(new_sides)
            size += new_size
        else:
            sides.add((pos[0], pos[1], dir))
    return size, sides


def part_1(input_file: str):
    global input_data
    global seen
    seen = set()
    data_file = Path(__file__).with_name(input_file).read_text()
    input_data = data_file.split("\n")
    total = 0
    for y, line in enumerate(input_data):
        for x, letter in enumerate(line):
            if (y, x) not in seen:
                size, edges = count_size_and_edges_of_area((y, x), letter)
                total += size * edges
    return total


def discard_line(y, x, dir, sides: set[tuple[int, int, str]]):
    match dir:
        case "^" | "v":
            if (y, x + 1, dir) in sides:
                sides.remove((y, x + 1, dir))
                discard_line(y, x + 1, dir, sides)
            if (y, x - 1, dir) in sides:
                sides.remove((y, x - 1, dir))
                discard_line(y, x - 1, dir, sides)
        case "<" | ">":
            if (y + 1, x, dir) in sides:
                sides.remove((y + 1, x, dir))
                discard_line(y + 1, x, dir, sides)
            if (y - 1, x, dir) in sides:
                sides.remove((y - 1, x, dir))
                discard_line(y - 1, x, dir, sides)


def get_actual_sides(sides: set[tuple[int, int, str]]) -> int:
    actual_sides = 0
    while sides:
        y, x, dir = sides.pop()
        actual_sides += 1
        discard_line(y, x, dir, sides)

    return actual_sides


def part_2(input_file: str):
    global input_data
    global seen
    seen = set()
    data_file = Path(__file__).with_name(input_file).read_text()
    input_data = data_file.split("\n")
    total = 0
    for y, line in enumerate(input_data):
        for x, letter in enumerate(line):
            if (y, x) not in seen:
                size, sides = count_size_and_sides_of_area((y, x), letter)
                actual_sides = get_actual_sides(sides)
                total += size * actual_sides
    return total


if __name__ == "__main__":
    print("#" * 10 + " Part 1 " + "#" * 10)
    result_ex = part_1("input_ex.txt")
    print(result_ex)
    assert result_ex == 140
    result_ex = part_1("input_ex2.txt")
    print(result_ex)
    assert result_ex == 772
    result_ex = part_1("input_ex3.txt")
    print(result_ex)
    assert result_ex == 1930

    result = part_1("input.txt")
    print(result)

    # #### Part 2 ####
    print("#" * 10 + " Part 2 " + "#" * 10)
    result = part_2("input_ex.txt")
    print(result)
    assert result == 80
    result = part_2("input_ex2.txt")
    print(result)
    assert result == 436
    result = part_2("input_ex3.txt")
    print(result)
    assert result == 1206
    result = part_2("input_ex4.txt")
    print(result)
    assert result == 236

    result = part_2("input.txt")
    print(result)
