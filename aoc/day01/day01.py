def part1():
    with open("input.txt") as f:
        lines = f.readlines()
    list1 = [int(x.split()[0]) for x in lines]
    list2 = [int(x.split()[1]) for x in lines]

    list1 = sorted(list1)
    list2 = sorted(list2)

    diff = [abs(x - y) for x, y in zip(list1, list2)]
    return sum(diff)


def part2():
    with open("input.txt") as f:
        lines = f.readlines()
    list1 = [int(x.split()[0]) for x in lines]
    list2 = [int(x.split()[1]) for x in lines]

    sim_score = 0
    for num in list(set(list1)):
        sim_score += num * list2.count(num)

    return sim_score


if __name__ == "__main__":
    solution = part1()
    print(f"Part 1: {solution}")
    solution = part2()
    print(f"Part 2: {solution}")
