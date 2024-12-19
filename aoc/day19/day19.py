from functools import cache
from pathlib import Path

towels = []


def is_possible(design: str) -> bool:
    global towels
    if design == "":
        return True
    for towel in towels:
        if not design.startswith(towel):
            continue
        if is_possible(design[len(towel) :]):
            return True
    return False


@cache
def get_designs(design: str) -> int:
    global towels
    if design == "":
        return 1
    count = 0
    for towel in towels:
        if not design.startswith(towel):
            continue
        count += get_designs(design[len(towel) :])
    return count


def part_1(input_file: str):
    global towels
    data_file = Path(__file__).with_name(input_file).read_text()
    input_data = data_file.split("\n\n")
    towels = input_data[0].split(", ")
    designs = input_data[1].split("\n")

    check_possible = [is_possible(design) for design in designs]
    return sum(check_possible)


def part_2(input_file: str):
    global towels
    data_file = Path(__file__).with_name(input_file).read_text()
    input_data = data_file.split("\n\n")
    towels = input_data[0].split(", ")
    designs = input_data[1].split("\n")

    check_possible = [get_designs(design) for design in designs]
    return sum(check_possible)


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

    get_designs.cache_clear()
    result = part_2("input.txt")
    print(result)
    assert result < 719644217597148
