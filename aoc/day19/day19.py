from pathlib import Path

input_data = []


def is_possible(towels: list[str], design: str) -> bool:
    if design == "":
        return True
    for towel in towels:
        if not design.startswith(towel):
            continue
        if is_possible(towels, design[len(towel) :]):
            return True
    return False


def part_1(input_file: str):
    global input_data
    data_file = Path(__file__).with_name(input_file).read_text()
    input_data = data_file.split("\n\n")
    towels = input_data[0].split(", ")
    designs = input_data[1].split("\n")

    check_possible = [is_possible(towels, design) for design in designs]
    return sum(check_possible)


def part_2(input_file: str):
    global input_data
    data_file = Path(__file__).with_name(input_file).read_text()
    input_data = data_file.split("\n")


if __name__ == "__main__":
    print("#" * 10 + " Part 1 " + "#" * 10)
    result_ex = part_1("input_ex.txt")
    print(result_ex)
    assert result_ex == 6

    result = part_1("input.txt")
    print(result)

    # #### Part 2 ####
    print("#" * 10 + " Part 2 " + "#" * 10)
    result = part_2("input_ex.txt")
    print(result)
    assert result == 16

    result = part_2("input.txt")
    print(result)
