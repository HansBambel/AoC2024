from collections import defaultdict
from pathlib import Path

input_data = []


def part_1(input_file: str):
    global input_data
    data_file = Path(__file__).with_name(input_file).read_text()
    input_data = data_file.split("\n")
    connections = [tuple(connection.split("-")) for connection in input_data]
    triple_connections = set()
    computer_connected = defaultdict(set)
    for comp1, comp2 in connections:
        computer_connected[comp1].add(comp2)
        computer_connected[comp2].add(comp1)

    for comp1, connected in computer_connected.items():
        for comp2 in connected:
            for comp3, connected2 in computer_connected.items():
                if (comp2 in connected2) and (comp1 in connected2):
                    triple_connections.add(tuple(sorted({comp1, comp2, comp3})))

    # The computer that starts with t needs to be in the connections
    filtered = []
    for triplets in triple_connections:
        if any(triplet for triplet in triplets if triplet.startswith("t")):
            filtered.append(triplets)

    return len(filtered)


def part_2(input_file: str):
    global input_data
    data_file = Path(__file__).with_name(input_file).read_text()
    input_data = data_file.split("\n")
    connections = [tuple(connection.split("-")) for connection in input_data]
    computer_connected = defaultdict(set)
    for comp1, comp2 in connections:
        computer_connected[comp1].add(comp2)
        computer_connected[comp2].add(comp1)

    connected = [{comp} for comp in computer_connected.keys()]
    for sub_con in connected:
        for comp, connected_comps in computer_connected.items():
            if all(other_comp in connected_comps for other_comp in sub_con):
                sub_con.add(comp)

    # get largest sub_network
    largest_network = max(connected, key=len)
    return ",".join(sorted(largest_network))


if __name__ == "__main__":
    print("#" * 10 + " Part 1 " + "#" * 10)
    result_ex = part_1("input_ex.txt")
    print(result_ex)
    assert result_ex == 7

    result = part_1("input.txt")
    print(result)

    # #### Part 2 ####
    print("#" * 10 + " Part 2 " + "#" * 10)
    result_ex = part_2("input_ex.txt")
    print(result_ex)
    assert result_ex == "co,de,ka,ta"

    result = part_2("input.txt")
    print(result)
