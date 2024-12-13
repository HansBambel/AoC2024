import re
from pathlib import Path

machines = []


def calc_tokens(machine: list[str]) -> int:
    solutions = []
    a = list(map(int, re.findall(r"\d+", machine[0])))
    b = list(map(int, re.findall(r"\d+", machine[1])))
    prize = list(map(int, re.findall(r"\d+", machine[2])))
    for i in range(101):
        for j in range(101):
            if a[0] * i + b[0] * j == prize[0] and a[1] * i + b[1] * j == prize[1]:
                solutions.append(i * 3 + j * 1)
    return max(solutions) if solutions else 0


def part_1(input_file: str):
    global machines
    data_file = Path(__file__).with_name(input_file).read_text()
    machines = data_file.split("\n\n")
    machines = [machine.split("\n") for machine in machines]
    tokens = 0
    for machine in machines:
        tokens += calc_tokens(machine)

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
    result = part_2("input_ex.txt")
    print(result)
    assert result == 1337

    result = part_2("input.txt")
    print(result)
