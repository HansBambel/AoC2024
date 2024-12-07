from pathlib import Path
from itertools import product


def is_solvable(total: int, numbers: list[int], part_2: bool = False) -> int:
    """Return the total when the numbers can be arranged with + and * (and concat for part 2) to reach the total. 0 Otherwise."""

    def plus(x, y):
        return x + y

    def mult(x, y):
        return x * y

    def concat(x, y):
        return int(str(x) + str(y))

    ops = [plus, mult]
    if part_2:
        ops.append(concat)
    all_ops = list(product(ops, repeat=len(numbers) - 1))
    for calcs in all_ops:
        temp = numbers[0]
        for i, op in enumerate(calcs):
            temp = op(temp, numbers[i + 1])
        if temp == total:
            return total
    return 0


def part_1(input_file: str):
    data_file = Path(__file__).with_name(input_file).read_text()
    input_data = data_file.split("\n")
    rules = list(line.split(":") for line in input_data)
    rules = [(int(total), list(map(int, numbers.split()))) for total, numbers in rules]

    total = sum(is_solvable(total, numbers) for total, numbers in rules)
    return total


def part_2(input_file: str):
    data_file = Path(__file__).with_name(input_file).read_text()
    input_data = data_file.split("\n")
    rules = list(line.split(":") for line in input_data)
    rules = [(int(total), list(map(int, numbers.split()))) for total, numbers in rules]

    total = sum(is_solvable(total, numbers, part_2=True) for total, numbers in rules)
    return total


if __name__ == "__main__":
    print("#" * 10 + " Part 1 " + "#" * 10)
    result_ex = part_1("input_ex.txt")
    print(result_ex)
    assert result_ex == 3749

    result = part_1("input.txt")
    print(result)

    # #### Part 2 ####
    print("#" * 10 + " Part 2 " + "#" * 10)
    result = part_2("input_ex.txt")
    print(result)
    assert result == 11387

    result = part_2("input.txt")
    print(result)
