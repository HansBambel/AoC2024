import re
from pathlib import Path

machines = []


def calc_tokens(machine: list[str], part2) -> int:
    a = list(map(int, re.findall(r"\d+", machine[0])))
    b = list(map(int, re.findall(r"\d+", machine[1])))
    prize = list(map(int, re.findall(r"\d+", machine[2])))
    if part2:
        prize = [prize[0] + 10000000000000, prize[1] + 10000000000000]

    # prize[0] = a[0]*a_pressed+b[0]*b_pressed
    # prize[1] = a[1]*a_pressed+b[1]*b_pressed

    # p0 - b[0]*b_pressed = a[0]*a_pressed
    # (p0 - b[0]*b_pressed) / a[0] = a_pressed

    # p1 - a[1]*a_pressed = b[1]*b_pressed
    # (p1 - a[1]*a_pressed) / b[1] = b_pressed

    # (p1 - a[1]*((p0 - b[0]*b_pressed) / a[0])) / b[1] = b_pressed
    # and so on

    b_pressed = (prize[1] * a[0] - a[1] * prize[0]) / (a[0] * b[1] - a[1] * b[0])
    a_pressed = (prize[0] - b[0] * b_pressed) / a[0]
    if b_pressed.is_integer() and a_pressed.is_integer():
        return int(a_pressed * 3 + b_pressed * 1)
    else:
        return 0


def part_1(input_file: str, part2=False):
    global machines
    data_file = Path(__file__).with_name(input_file).read_text()
    machines = data_file.split("\n\n")
    machines = [machine.split("\n") for machine in machines]
    tokens = 0
    for machine in machines:
        tokens += calc_tokens(machine, part2=part2)

    return tokens


def part_2(input_file: str):
    global machines
    data_file = Path(__file__).with_name(input_file).read_text()
    machines = data_file.split("\n\n")


if __name__ == "__main__":
    print("#" * 10 + " Part 1 " + "#" * 10)
    result_ex = part_1("input_ex.txt")
    print(result_ex)
    assert result_ex == 480

    result = part_1("input.txt")
    print(result)

    # #### Part 2 ####
    print("#" * 10 + " Part 2 " + "#" * 10)
    result = part_1("input.txt", part2=True)
    print(result)
