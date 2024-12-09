from collections import OrderedDict
from pathlib import Path


def get_string(disk: dict[int, list[str]]) -> str:
    return "".join(disk.values())


def create_initial_state(input_data: str) -> OrderedDict[int, list[str]]:
    disk = OrderedDict()
    for i, num in enumerate(input_data):
        disk[i] = [str(i // 2)] * int(num) if i % 2 == 0 else ["."] * int(num)
    return disk


def calculate_checksum(sorted_disk: dict[int, list[str]]) -> int:
    checksum = 0
    ind = -1
    for entry in sorted_disk.values():
        for num in entry:
            ind += 1
            if num == ".":
                continue
            checksum += ind * int(num)
    return checksum


def sort_disk(disk: OrderedDict[int, list[str]]) -> dict[int, list[str]]:
    free_index = 0
    sort_index = len(disk) - 1
    while free_index < sort_index:
        if "." not in disk[free_index]:
            free_index += 1
            continue
        if len(disk[sort_index]) == 0:
            sort_index -= 1
            continue
        # Find first "." in the free_index
        dot_ind = next(i for i, c in enumerate(disk[free_index]) if c == ".")
        disk[free_index][dot_ind] = disk[sort_index][-1]
        disk[sort_index] = disk[sort_index][:-1]
        # print(get_string(disk))
    return disk


def part_1(input_file: str):
    data_file = Path(__file__).with_name(input_file).read_text()
    disk = create_initial_state(data_file)

    sorted_disk = sort_disk(disk)
    checksum = calculate_checksum(sorted_disk)
    return checksum


def part_2(input_file: str):
    data_file = Path(__file__).with_name(input_file).read_text()
    disk = create_initial_state(data_file)

    sorted_disk = sort_disk(disk)
    checksum = calculate_checksum(sorted_disk)
    return checksum


if __name__ == "__main__":
    print("#" * 10 + " Part 1 " + "#" * 10)
    result_ex = part_1("input_ex.txt")
    print(result_ex)
    assert result_ex == 1928

    result = part_1("input.txt")
    assert result > 92092395920
    print(result)

    # #### Part 2 ####
    print("#" * 10 + " Part 2 " + "#" * 10)
    result = part_2("input_ex.txt")
    print(result)
    assert result == 2858

    result = part_2("input.txt")
    print(result)
