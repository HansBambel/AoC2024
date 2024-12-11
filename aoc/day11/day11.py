from pathlib import Path
from functools import lru_cache

lru_cache(maxsize=None)


def split_stone(stone: str) -> list[str]:
    if stone == "0":
        return ["1"]
    if len(stone) % 2 == 0:
        return [stone[: len(stone) // 2], str(int(stone[len(stone) // 2 :]))]
    return [str(int(stone) * 2024)]


def part_1(input_file: str, blinks=25):
    data_file = Path(__file__).with_name(input_file).read_text()
    stones = data_file.split(" ")
    for i in range(blinks):
        new_stones = []
        for stone in stones:
            new_stones.extend(split_stone(stone))
        stones = new_stones

    return len(stones)


if __name__ == "__main__":
    print("#" * 10 + " Part 1 " + "#" * 10)
    result_ex = part_1("input_ex.txt", blinks=6)
    print(result_ex)
    assert result_ex == 22
    result_ex = part_1("input_ex.txt", blinks=25)
    assert result_ex == 55312

    result = part_1("input.txt", blinks=25)
    print(result)

    # #### Part 2 ####
    print("#" * 10 + " Part 2 " + "#" * 10)
    result = part_1("input.txt", blinks=75)
    print(result)
