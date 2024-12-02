def is_safe(report: list[int]) -> bool:
    increase = None
    safe = True
    for i, num in enumerate(report[1:]):
        if (num - report[i] == 0) or (abs(num - report[i]) > 3):
            safe = False
            break

        current_inc = num > report[i]
        if increase is None:
            increase = current_inc
        else:
            if increase != current_inc:
                safe = False
                break
    return safe


def part1(file):
    with open(file) as f:
        lines = f.readlines()
    reports = [list(map(int, x.split())) for x in lines]

    total = 0
    for report in reports:
        if is_safe(report):
            total += 1

    return total


def part2(file):
    with open(file) as f:
        lines = f.readlines()
    reports = [list(map(int, x.split())) for x in lines]

    total = 0
    for report in reports:
        if is_safe(report):
            total += 1
        else:
            # Check if removing one element makes it safe
            for i in range(len(report)):
                if is_safe(report[:i] + report[i + 1 :]):
                    total += 1
                    break

    return total


if __name__ == "__main__":
    print(f"Example: {part1('input_ex.txt')}")
    solution = part1("input.txt")
    print(f"Part 1: {solution}")
    print(f"Example: {part2('input_ex.txt')}")
    solution = part2("input.txt")
    print(f"Part 2: {solution}")
