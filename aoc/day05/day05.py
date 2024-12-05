from collections import defaultdict
from pathlib import Path


def make_rules(raw_rules: list[list[str]]) -> dict[str : list[str]]:
    rules = defaultdict(list)
    for before, after in raw_rules:
        rules[before].append(after)
    return rules


def is_correct_order(row: list[str], rules: dict[str, list[str]]) -> bool:
    for i, number in enumerate(row):
        if number in rules:
            must_be_after = rules[number]
            if any(after in row[:i] for after in must_be_after):
                return False
    return True


def part_1(input_file: str):
    data_file = Path(__file__).with_name(input_file).read_text()
    rules, updates = data_file.split("\n\n")
    rules = rules.split("\n")
    raw_rules = [rule.split("|") for rule in rules]
    rules = make_rules(raw_rules)
    updates = updates.split("\n")

    middle_values = []
    for row in updates:
        row = row.split(",")
        in_order = is_correct_order(row, rules)
        if in_order:
            middle_values.append(int(row[len(row) // 2]))
    return sum(middle_values)


def sort_row(row: list[str], rules: dict[str, list[str]]) -> list[str]:
    new_row = []
    for number in row:
        if number in rules:
            must_be_following = rules[number]
            first_match = next(
                (after for after in must_be_following if after in new_row), None
            )
            if first_match:
                new_row.insert(new_row.index(first_match), number)
            else:
                new_row.append(number)
        else:
            new_row.append(number)
    if not is_correct_order(new_row, rules):
        new_row = sort_row(new_row, rules)
    return new_row


def part_2(input_file: str):
    data_file = Path(__file__).with_name(input_file).read_text()
    input_rules, updates = data_file.split("\n\n")
    input_rules = input_rules.split("\n")
    raw_rules = [rule.split("|") for rule in input_rules]
    rules = make_rules(raw_rules)
    updates = updates.split("\n")

    incorrect = []
    for row in updates:
        row = row.split(",")
        if not is_correct_order(row, rules):
            incorrect.append(row)

    corrected = []
    for row in incorrect:
        corrected_row = sort_row(row, rules)
        corrected.append(corrected_row)

    for row in corrected:
        if not is_correct_order(row, rules):
            print(row)

    assert all(is_correct_order(row, rules) for row in corrected)

    middle_values = [int(row[len(row) // 2]) for row in corrected]
    return sum(middle_values)


if __name__ == "__main__":
    print("#" * 10 + " Part 1 " + "#" * 10)
    result_ex = part_1("input_ex.txt")
    print(result_ex)
    assert result_ex == 143

    result = part_1("input.txt")
    print(result)

    # #### Part 2 ####
    print("#" * 10 + " Part 2 " + "#" * 10)
    result = part_2("input_ex.txt")
    print(result)
    assert result == 123

    result = part_2("input.txt")
    assert result > 6972, result
    print(result)
