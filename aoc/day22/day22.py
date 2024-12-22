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


if __name__ == "__main__":
    print("#" * 10 + " Part 1 " + "#" * 10)
    result_ex = part_1("input_ex.txt")
    print(result_ex)
    assert result_ex == 37327623

    result = part_1("input.txt")
    print(result)

    # #### Part 2 ####
    print("#" * 10 + " Part 2 " + "#" * 10)
    result = part_2("input_ex.txt")
    print(result)
    assert result == 1337

    result = part_2("input.txt")
    print(result)
