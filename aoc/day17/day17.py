import re
from pathlib import Path

input_data = []


def run_operations(program, reg_a, reg_b, reg_c) -> list[int]:
    ind = 0
    out = []
    while ind < len(program):
        instr = program[ind]
        operand = program[ind + 1]
        match operand:
            case 4:
                combo = reg_a
            case 5:
                combo = reg_b
            case 6:
                combo = reg_c
            case 7:
                raise ValueError("Invalid operand")
            case _:
                combo = operand

        match instr:
            case 0:
                reg_a = int(reg_a / 2**combo)
            case 1:
                reg_b = reg_b ^ operand
            case 2:
                reg_b = combo % 8
            case 3:
                if reg_a != 0:
                    ind = operand
                    continue
            case 4:
                reg_b = reg_b ^ reg_c
            case 5:
                out.append(combo % 8)
            case 6:
                reg_b = int(reg_a / 2**combo)
            case 7:
                reg_c = int(reg_a / 2**combo)
        ind += 2
    return out


def part_1(input_file: str):
    global input_data
    data_file = Path(__file__).with_name(input_file).read_text()
    input_data = data_file.split("\n\n")
    reg_a, reg_b, reg_c = input_data[0].split("\n")
    reg_a = int(reg_a.split()[-1])
    reg_b = int(reg_b.split()[-1])
    reg_c = int(reg_c.split()[-1])
    program = list(re.findall(r"\d+", input_data[1]))
    program = [int(x) for x in program]

    out = run_operations(program, reg_a, reg_b, reg_c)
    return ",".join(map(str, out))


def part_2(input_file: str):
    global input_data
    data_file = Path(__file__).with_name(input_file).read_text()
    input_data = data_file.split("\n\n")
    _, reg_b, reg_c = input_data[0].split("\n")
    reg_b = int(reg_b.split()[-1])
    reg_c = int(reg_c.split()[-1])
    program = list(re.findall(r"\d+", input_data[1]))
    program = [int(x) for x in program]

    reg_a = 8
    # get starting point
    while len(program) > len(run_operations(program, reg_a, reg_b, reg_c)):
        reg_a *= 8
    out = ""
    prev = 0
    reg_a = 35942313392565
    while out != program:
        reg_a += 206158430208
        try:
            out = run_operations(program, reg_a, reg_b, reg_c)
            until = 11
            if out[:until] == program[:until]:
                # if True:
                print(reg_a, out, reg_a - prev)
                prev = reg_a
        except ValueError:
            continue
        if len(out) > len(program):
            print("Too long")
            break
    return reg_a


if __name__ == "__main__":
    print("#" * 10 + " Part 1 " + "#" * 10)
    result_ex = part_1("input_ex.txt")
    print(result_ex)
    assert result_ex == "4,6,3,5,6,3,5,2,1,0"

    result = part_1("input.txt")
    print(result)

    # #### Part 2 ####
    print("#" * 10 + " Part 2 " + "#" * 10)
    # result = part_2("input_ex2.txt")
    # print(result)
    # assert result == 117440

    result = part_2("input.txt")
    print(result)
