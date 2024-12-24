from pathlib import Path
from operator import and_, or_, xor

input_data = []
connections = []


def part_1(input_file: str):
    global input_data, connections
    data_file = Path(__file__).with_name(input_file).read_text()
    input_data, connections = data_file.split("\n\n")
    input_data = input_data.split("\n")
    connections = connections.split("\n")
    operators = {"AND": and_, "OR": or_, "XOR": xor}

    gates = {
        name: bool(int(value))
        for name, value in (gate.split(": ") for gate in input_data)
    }
    connections = [connection.split(" ") for connection in connections]
    while len(connections) > 0:
        connection = connections.pop(0)
        if gates.get(connection[0]) is None or gates.get(connection[2]) is None:
            connections.append(connection)
            continue
        operator = operators[connection[1]]
        gates[connection[-1]] = operator(gates[connection[0]], gates[connection[2]])

    # Sort the gates by name and convert the binary number to decimal
    bin_number = {
        name: str(int(value)) for name, value in gates.items() if name.startswith("z")
    }
    bin_number = dict(sorted(bin_number.items(), key=lambda x: x[0]))
    return int("".join(bin_number.values())[::-1], 2)


def part_2(input_file: str):
    global input_data
    data_file = Path(__file__).with_name(input_file).read_text()
    input_data = data_file.split("\n")


if __name__ == "__main__":
    print("#" * 10 + " Part 1 " + "#" * 10)
    result_ex = part_1("input_ex.txt")
    print(result_ex)
    assert result_ex == 4
    result_ex = part_1("input_ex2.txt")
    print(result_ex)
    assert result_ex == 2024

    result = part_1("input.txt")
    print(result)

    # #### Part 2 ####
    print("#" * 10 + " Part 2 " + "#" * 10)
    result_ex = part_2("input_ex.txt")
    print(result_ex)
    assert result_ex == 1337

    result = part_2("input.txt")
    print(result)
