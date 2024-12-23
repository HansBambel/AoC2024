from pathlib import Path
import re


def get_sum(matches: list[tuple[str, str]]) -> int:
    return sum([int(x) * int(y) for x, y in matches])


def part_1(input_file: str):
    input_data = Path(__file__).with_name(input_file).read_text()

    pattern = re.findall(r"mul\((\d{1,3}),(\d{1,3})\)", input_data)
    return get_sum(pattern)


def part_2(input_file: str):
    input_data = Path(__file__).with_name(input_file).read_text()
    pattern = re.findall(r"mul\((\d{1,3}),(\d{1,3})\)|(don't\(\)|do\(\))", input_data)
    multiplications = []
    enabled = True
    for x, y, do in pattern:
        if do:
            enabled = do == "do()"
            continue
        if enabled:
            multiplications.append((x, y))
    total = get_sum(multiplications)
    return total


if __name__ == "__main__":
    print("#" * 10 + " Part 1 " + "#" * 10)
    result_ex = part_1("input_ex.txt")
    print(result_ex)
    assert result_ex == 161, result_ex

    result = part_1("input.txt")
    print(result)

    # #### Part 2 ####
    print("#" * 10 + " Part 2 " + "#" * 10)
    result_ex = part_2("input_ex2.txt")
    print(result_ex)
    assert result_ex == 48, result_ex

    result = part_2("input.txt")
    assert result > 6889594, result
    assert result != 79344189, result
    assert result != 118265503, result
    assert result != 68841592, result
    assert result != 69854524, result
    assert result != 36601983, result
    assert result != 18948047, result
    print(result)
