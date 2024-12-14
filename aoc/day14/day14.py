import re
from functools import reduce
from pathlib import Path
from operator import mul

input_data = []


def get_robot_in_quadrants(positions, size: tuple[int, int]) -> list[int]:
    quadrants = [0, 0, 0, 0]
    for pos in positions:
        if pos[0] < size[0] // 2 and pos[1] < size[1] // 2:
            quadrants[0] += 1
        elif pos[0] > size[0] // 2 and pos[1] < size[1] // 2:
            quadrants[1] += 1
        elif pos[0] < size[0] // 2 and pos[1] > size[1] // 2:
            quadrants[2] += 1
        elif pos[0] > size[0] // 2 and pos[1] > size[1] // 2:
            quadrants[3] += 1

    return quadrants


def get_robots(input_data: list[str]):
    robots = []
    for line in input_data:
        pos, vel = line.split(" ")
        pos = list(map(int, re.findall(r"-?\d+", pos)))
        vel = list(map(int, re.findall(r"-?\d+", vel)))
        robots.append((pos, vel))
    return robots


def part_1(input_file: str, seconds=100, size=(11, 7)) -> int:
    global input_data
    data_file = Path(__file__).with_name(input_file).read_text()
    input_data = data_file.split("\n")

    robots = get_robots(input_data)
    endpos = []
    for pos, vel in robots:
        endpos.append(
            (
                (pos[0] + vel[0] * seconds) % size[0],
                (pos[1] + vel[1] * seconds) % size[1],
            )
        )

    in_quadrants = get_robot_in_quadrants(endpos, size)
    return reduce(mul, in_quadrants)


def part_2(input_file: str):
    global input_data
    data_file = Path(__file__).with_name(input_file).read_text()
    input_data = data_file.split("\n")


if __name__ == "__main__":
    print("#" * 10 + " Part 1 " + "#" * 10)
    result_ex = part_1("input_ex.txt", size=(11, 7))
    print(result_ex)
    assert result_ex == 12

    result = part_1("input.txt", size=(101, 103))
    print(result)

    # #### Part 2 ####
    print("#" * 10 + " Part 2 " + "#" * 10)
    result = part_2("input_ex.txt")
    print(result)
    assert result == 1337

    result = part_2("input.txt")
    print(result)
