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


def part_2(input_file: str):
    data_file = Path(__file__).with_name(input_file).read_text()
    input_data = data_file.split("\n")


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
    assert result == 1337

    result = part_2("input.txt")
    print(result)
