from pathlib import Path

input_data = []


def get_keys_locks(input_data) -> tuple[list, list]:
    keys = []
    locks = []
    for i, grid in enumerate(input_data):
        grid = grid.split("\n")
        pins = [0 for _ in range(len(grid[0]))]
        for j, row in enumerate(grid):
            for k, cell in enumerate(row):
                if cell == "#":
                    pins[k] += 1

        pins = [x - 1 for x in pins]
        to_add = locks if set(grid[0]) == {"#"} else keys
        to_add.append(pins)

    return keys, locks


def match_lock_and_keys(keys, locks) -> int:
    matching = 0
    for lock in locks:
        for key in keys:
            matching += all(lock[i] + key[i] <= 5 for i in range(len(lock)))
    return matching


def part_1(input_file: str):
    global input_data
    data_file = Path(__file__).with_name(input_file).read_text()
    input_data = data_file.split("\n\n")
    keys, locks = get_keys_locks(input_data)

    matching_locks = match_lock_and_keys(keys, locks)

    return matching_locks


def part_2(input_file: str):
    global input_data
    data_file = Path(__file__).with_name(input_file).read_text()
    input_data = data_file.split("\n")


if __name__ == "__main__":
    print("#" * 10 + " Part 1 " + "#" * 10)
    result_ex = part_1("input_ex.txt")
    print(result_ex)
    assert result_ex == 3

    result = part_1("input.txt")
    print(result)
