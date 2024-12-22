from collections import defaultdict
from pathlib import Path

input_data = []


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


def part_2(input_file: str):
    global input_data
    data_file = Path(__file__).with_name(input_file).read_text()
    input_data = data_file.split("\n")
    input_data = [int(x) for x in input_data]
    secret_numbers = []
    changes = []
    bananas_gained = {}
    for n_i, number in enumerate(input_data):
        new_secret_numbers = [number % 10]
        changes_number = []
        for i in range(2000):
            number = (number ^ number * 64) % 16777216
            number = (number ^ number // 32) % 16777216
            number = (number ^ number * 2048) % 16777216
            new_secret_numbers.append(number % 10)
            changes_number.append(new_secret_numbers[-1] - new_secret_numbers[-2])
            if i > 3:
                sequence = (
                    changes_number[i - 3],
                    changes_number[i - 2],
                    changes_number[i - 1],
                    changes_number[i],
                )
                bananas = number % 10
                if (input_data[n_i], sequence) not in bananas_gained:
                    bananas_gained[(input_data[n_i], sequence)] = bananas
        secret_numbers.append(new_secret_numbers)
        changes.append(changes_number)

    best_price_per_pattern = defaultdict(int)
    for n_i, number in enumerate(input_data):
        seen = set()
        for i in range(len(changes[n_i]) - 4):
            sequence = tuple(changes[n_i][i : i + 4])

            if sequence not in seen:
                best_price_per_pattern[sequence] += secret_numbers[n_i][i + 4]
                seen.add(sequence)
    best_price = max(best_price_per_pattern.values())

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
