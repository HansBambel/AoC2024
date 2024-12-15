from pathlib import Path

grid = [[]]
moves = ""
dirs = {"^": (-1, 0), "v": (1, 0), ">": (0, 1), "<": (0, -1)}

def get_start_pos(grid) -> tuple[int, int]:
    for y in range(len(grid)):
        for x in range(len(grid[0])):
            if grid[y][x] == "@":
                return y, x

def get_score(grid) -> int:
    score = 0
    for y in range(len(grid)):
        for x in range(len(grid[0])):
            if grid[y][x] in ["O", "["]:
                score += 100*y + x
    return score

def move_box(pos: tuple[int, int], dir: tuple[int, int]) -> bool:
    next_pos = (pos[0] + dir[0], pos[1] + dir[1])
    if grid[next_pos[0]][next_pos[1]] == "#":
        # can't move
        return False
    if grid[next_pos[0]][next_pos[1]] == ".":
        grid[next_pos[0]][next_pos[1]] = "O"
        grid[pos[0]][pos[1]] = "."
        return True
    if grid[next_pos[0]][next_pos[1]] == "O":
        # move the box
        if move_box(next_pos, dir):
            grid[next_pos[0]][next_pos[1]] = "O"
            grid[pos[0]][pos[1]] = "."
            return True
        else:
            return False


def move_robot(pos: tuple[int, int], dir: tuple[int, int]) -> tuple[int, int]:
    next_pos = (pos[0] + dir[0], pos[1] + dir[1])
    if grid[next_pos[0]][next_pos[1]] == "#":
        # can't move
        return pos
    if grid[next_pos[0]][next_pos[1]] == ".":
        grid[next_pos[0]][next_pos[1]] = "@"
        grid[pos[0]][pos[1]] = "."
        return next_pos
    if grid[next_pos[0]][next_pos[1]] in ["O", "[", "]"]:
        # move the box
        if move_box(next_pos, dir):
            grid[next_pos[0]][next_pos[1]] = "@"
            grid[pos[0]][pos[1]] = "."
            return next_pos
        else:
            return pos


def part_1(input_file: str):
    global grid
    global moves
    data_file = Path(__file__).with_name(input_file).read_text()
    input_data = data_file.split("\n\n")
    grid, moves = input_data[0].split("\n"), "".join(input_data[1].split("\n"))
    grid = [list(row) for row in grid]
    cur_pos = get_start_pos(grid)
    for move in moves:
        cur_pos = move_robot(cur_pos, dirs[move])

    return get_score(grid)


def resize_grid(grid) -> list[list[str]]:
    new_grid = []
    for y, row in enumerate(grid):
        new_row = []
        for x, char in enumerate(row):
            if char == "O":
                new_row.extend(["[", "]"])
            elif char == "@":
                new_row.extend(["@", "."])
            elif char == ".":
                new_row.extend([".", "."])
            elif char == "#":
                new_row.extend(["#", "#"])
        new_grid.append(new_row)
    return new_grid

def part_2(input_file: str):
    global grid
    global moves
    data_file = Path(__file__).with_name(input_file).read_text()
    input_data = data_file.split("\n\n")
    grid, moves = input_data[0].split("\n"), "".join(input_data[1].split("\n"))
    grid = [list(row) for row in grid]
    grid = resize_grid(grid)


if __name__ == "__main__":
    print("#" * 10 + " Part 1 " + "#" * 10)
    result_ex = part_1("input_ex.txt")
    print(result_ex)
    assert result_ex == 2028
    result_ex = part_1("input_ex2.txt")
    print(result_ex)
    assert result_ex == 10092

    result = part_1("input.txt")
    print(result)

    # #### Part 2 ####
    print("#" * 10 + " Part 2 " + "#" * 10)
    result = part_2("input_ex2.txt")
    print(result)
    assert result == 9021

    result = part_2("input.txt")
    print(result)
