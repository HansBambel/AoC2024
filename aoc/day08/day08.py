from pathlib import Path
from itertools import combinations


def get_antinodes_of_antennas(
    antenna_1, antenna_2, grid_lengths: tuple[int, int] | None = None
) -> set:
    diff = (antenna_1[0] - antenna_2[0], antenna_1[1] - antenna_2[1])
    max_repetitions = 1 if grid_lengths is None else max(grid_lengths)
    antinodes = set()
    for y, x in (antenna_1, antenna_2):
        for i in range(1, max_repetitions + 1):
            antinodes.add((y + i * diff[0], x + i * diff[1]))
            antinodes.add((y - i * diff[0], x - i * diff[1]))
    # Unsure why this difference is not needed for part 2
    # I am assuming at once the antennas would need to be removed
    if grid_lengths is None:
        return antinodes.difference({antenna_1, antenna_2})
    return antinodes


def get_antinodes_of_frequencies(
    input_data, frequency, grid_lengths: tuple[int, int] = None
) -> set:
    antennas = []
    antinodes = set()
    for y, line in enumerate(input_data):
        for x, c in enumerate(line):
            if c == frequency:
                antennas.append((y, x))

    # make pairs of antennas
    for ant_1, ant_2 in combinations(antennas, 2):
        antinodes = antinodes.union(
            get_antinodes_of_antennas(ant_1, ant_2, grid_lengths=grid_lengths)
        )

    return antinodes


def print_antinodes(input_data, antinodes):
    for y, row in enumerate(input_data):
        line = "".join("#" if (y, x) in antinodes else c for x, c in enumerate(row))
        print(line)


def part_1(input_file: str):
    data_file = Path(__file__).with_name(input_file).read_text()
    input_data = data_file.split("\n")
    # Find the same letters, get pairs, get their locations,
    antinodes = set()
    frequencies_to_handle = set(data_file).difference({"\n", "."})

    for frequency in frequencies_to_handle:
        new_antinodes = get_antinodes_of_frequencies(input_data, frequency)
        antinodes = antinodes.union(new_antinodes)

    # Remove those outside the grid
    antinodes = {
        antinode
        for antinode in antinodes
        if 0 <= antinode[0] < len(input_data) and 0 <= antinode[1] < len(input_data[0])
    }
    # print_antinodes(input_data, antinodes)
    return len(antinodes)


def part_2(input_file: str):
    data_file = Path(__file__).with_name(input_file).read_text()
    input_data = data_file.split("\n")
    # Find the same letters, get pairs, get their locations,
    antinodes = set()
    frequencies_to_handle = set(data_file).difference({"\n", "."})

    for frequency in frequencies_to_handle:
        new_antinodes = get_antinodes_of_frequencies(
            input_data, frequency, grid_lengths=(len(input_data), len(input_data[0]))
        )
        antinodes = antinodes.union(new_antinodes)

    # Remove those outside the grid
    antinodes = {
        antinode
        for antinode in antinodes
        if 0 <= antinode[0] < len(input_data) and 0 <= antinode[1] < len(input_data[0])
    }
    # print_antinodes(input_data, antinodes)
    return len(antinodes)


if __name__ == "__main__":
    print("#" * 10 + " Part 1 " + "#" * 10)
    result_ex = part_1("input_ex.txt")
    print(result_ex)
    assert result_ex == 14

    result = part_1("input.txt")
    print(result)

    # #### Part 2 ####
    print("#" * 10 + " Part 2 " + "#" * 10)
    result = part_2("input_ex.txt")
    print(result)
    assert result == 34

    result = part_2("input.txt")
    print(result)
