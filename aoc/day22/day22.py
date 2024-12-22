from functools import cache
from pathlib import Path

input_data = []
changes = []
secret_numbers = []


def part_1(input_file: str):
    global input_data
    data_file = Path(__file__).with_name(input_file).read_text()
    input_data = data_file.split("\n")
    input_data = [int(x) for x in input_data]
    secret_numbers = []
    for number in input_data:
        for _ in range(2000):
            number = (number ^ number * 64) % 16777216
            number = (number ^ number // 32) % 16777216
            number = (number ^ number * 2048) % 16777216
        secret_numbers.append(number)

    return sum(secret_numbers)


@cache
def find_prices_with_sequence(sequence: tuple[int, int, int, int]) -> int:
    total = 0
    # go through all changes of all secret numbers
    for s_i, secret_changes in enumerate(changes):
        # Get the occurrence
        for i in range(4, len(secret_changes)):
            if tuple(secret_changes[i - 4 : i]) == sequence:
                total += secret_numbers[s_i][i]
                break
    return total


def part_2(input_file: str):
    global input_data
    global changes
    global secret_numbers
    data_file = Path(__file__).with_name(input_file).read_text()
    input_data = data_file.split("\n")
    input_data = [int(x) for x in input_data]
    secret_numbers = []
    changes = []
    for number in input_data:
        new_secret_numbers = [number % 10]
        changes_number = []
        for i in range(2000):
            number = (number ^ number * 64) % 16777216
            number = (number ^ number // 32) % 16777216
            number = (number ^ number * 2048) % 16777216
            new_secret_numbers.append(number % 10)
            changes_number.append(new_secret_numbers[-1] - new_secret_numbers[-2])
        secret_numbers.append(new_secret_numbers)
        changes.append(changes_number)

    # go through the
    best_price = 0
    for s_i, changes_secret in enumerate(changes):
        print(f"{s_i/len(changes)*100:.2f}%")
        for i in range(4, 2000):
            sequence = (
                changes_secret[i - 4],
                changes_secret[i - 3],
                changes_secret[i - 2],
                changes_secret[i - 1],
            )
            price = find_prices_with_sequence(sequence)
            if price > best_price:
                best_price = price

    return best_price


if __name__ == "__main__":
    print("#" * 10 + " Part 1 " + "#" * 10)
    result_ex = part_1("input_ex.txt")
    print(result_ex)
    assert result_ex == 37327623

    result = part_1("input.txt")
    print(result)

    # #### Part 2 ####
    print("#" * 10 + " Part 2 " + "#" * 10)
    _ = part_2("input_ex3.txt")
    result_ex = part_2("input_ex2.txt")
    print(result_ex)
    assert result_ex == 23

    result = part_2("input.txt")
    print(result)
