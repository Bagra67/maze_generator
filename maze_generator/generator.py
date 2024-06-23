import random

from config import read_config_generator


class Cell:

    def __init__(self, c, l, entry_col = 0, entry_line = 0):
        self.visited: bool = False
        self.wall_up: bool = True
        self.wall_down: bool = True
        self.wall_left: bool = True
        self.wall_right: bool = True

        self._c: int = c
        self._l: int = l

        self.entry = True if c == entry_col and l == entry_line else False
        self.exit = False

    def __str__(self) -> str:
        return "({}, {}: {}|{}|{}|{})".format(
            self._c,
            self._l,
            self.wall_up,
            self.wall_right,
            self.wall_down,
            self.wall_left,
        )

    def display(self):
        print("🟦", end="")

    def get_c(self):
        return self._c + 1

    def get_l(self):
        return self._l + 1


class Maze:
    # Quand on parcours un tableau et qu'on veut les cases autour d'une on créer un tableau de taille n+2
    # Grace à ça les contours ne sont pas à gérer de façon particulères

    def __init__(self, column, line, entry_col = 0, entry_line = 0) -> None:
        self._line: int = line
        self._column: int = column
        self.maze: list[list[Cell]] = [
            [Cell(y-1, x-1, entry_col, entry_line) for y in range(column + 2)] for x in range(line + 2)
        ]

        # All edges are already visited to avoid use in algorithm
        for i in range(line + 2):
            self.maze[i][0].visited = True
            self.maze[i][column + 1].visited = True

        for j in range(column + 2):
            self.maze[0][j].visited = True
            self.maze[line + 1][j].visited = True

    def __str__(self):
        result = ""
        for i in range(self._line + 2):
            for j in range(self._column + 2):
                result += "T" if self.maze[i][j].visited else "F"
            result += "\n"
        return result

    def get(self, col: int, line: int) -> Cell:
        # Du coup le vrai 0,0 du tableau et en 1,1
        return self.maze[line + 1][col + 1]

    def get_neighbors(self, cell: Cell):
        result: list[Cell] = []
        offset: list[int] = [-1, 0, 1]
        for offset_c in offset:
            for offset_l in offset:
                #Get only direct neighbors and not diagonal and itself
                if (offset_c != 0 or offset_l != 0) and (
                    abs(offset_c) != abs(offset_l)
                ):
                    tmp_cell: Cell = self.maze[cell.get_l() + offset_l][
                        cell.get_c() + offset_c
                    ]
                    result.append(tmp_cell)
        return result
    
    def get_unvisited_neighbour(self, cell: Cell) -> list[Cell]:
        result = self.get_neighbors(cell)
        return [cell for cell in result if not cell.visited ]

    def open(self, current_cell: Cell, neighbor: Cell) -> None:
        if current_cell.get_c() == neighbor.get_c():
            if current_cell.get_l() + 1 == neighbor.get_l():
                current_cell.wall_down = False
                neighbor.wall_up = False
            else:
                current_cell.wall_up = False
                neighbor.wall_down = False
        elif current_cell.get_l() == neighbor.get_l():
            if current_cell.get_c() + 1 == neighbor.get_c():
                current_cell.wall_right = False
                neighbor.wall_left = False
            else:
                current_cell.wall_left = False
                neighbor.wall_right = False
        neighbor.visited = True

    def find_exit(self):
        possible_exits: list[Cell] = []

        # Go only on edges
        for column in range(self._column):
            for line in range(self._line):
                if (
                    column == 0
                    or column == self._column - 1
                    or line == 0
                    or line == self._line - 1
                ):
                    cell: Cell = self.get(column, line)
                    if not cell.entry:
                        neighbour = self.get_connected_neighbour(cell)
                        if len(neighbour) == 1:
                            possible_exits.append(cell)

        if possible_exits:
            random_index = random.randint(0, len(possible_exits) - 1)
            possible_exits[random_index].exit = True

    def get_connected_neighbour(self, cell: Cell) -> list[Cell]:
        neighbors: list[Cell] = self.get_neighbors(cell)
        result: list[Cell] = []

        for n in neighbors:
            if cell.get_c() == n.get_c():
                if not cell.wall_up and not n.wall_down:
                    result.append(n)
                elif not cell.wall_down and not n.wall_up:
                    result.append(n)
            
            if cell.get_l() == n.get_l():
                if not cell.wall_left and not n.wall_right:
                        result.append(n)
                elif not cell.wall_right and not n.wall_left:
                    result.append(n)

        return result
    
    
    def display(self):
        # First row will always be a wall
        for _ in range(self._column * 2 + 1):
            print("⬜", end="")
        print("\n", end="")

        for l in range(self._line):
            for c in range(self._column):
                cell: Cell = self.get(c, l)

                if cell.wall_left or c == 0:
                    print("⬜", end="")
                else:
                    print("🟦", end="")

                # Current cell
                if cell.entry:
                    print("🟩", end="")
                elif cell.exit:
                    print("🟥", end="")
                else:
                    print("🟦", end="")
            # The last character will always be a wall
            print("⬜\n", end="")

            # To diplay wall down
            for c_2 in range(self._column):
                cell: Cell = self.get(c_2, l)
                print("⬜", end="")

                if cell.wall_down:
                    print("⬜", end="")
                else:
                    print("🟦", end="")
            print("⬜\n", end="")

    def transform_in_file(self):
        with open("./output.txt", "w", encoding="utf-8") as f:
            # First row will always be a wall
            for _ in range(self._column * 2 + 1):
                f.write("⬜")
            f.write("\n")

            for l in range(self._line):
                for c in range(self._column):
                    cell: Cell = self.get(c, l)

                    if cell.wall_left or c == 0:
                        f.write("⬜")
                    else:
                        f.write("🟦")

                    # Current cell
                    if cell.entry:
                        f.write("🟩")
                    elif cell.exit:
                        f.write("🟥")
                    else:
                        f.write("🟦")

                # The last character will always be a wall
                f.write("⬜\n")

                # To diplay wall down
                for c_2 in range(self._column):
                    cell: Cell = self.get(c_2, l)
                    f.write("⬜")

                    if cell.wall_down:
                        f.write("⬜")
                    else:
                        f.write("🟦")
                f.write("⬜\n")


def generate():
    line, column, entry_col, entry_line = read_config_generator()

    maze = Maze(line=line, column=column, entry_col=entry_col, entry_line=entry_line)

    # Default entry
    default_cell: Cell = maze.get(entry_col, entry_line)
    default_cell.visited = True

    stack = [default_cell]

    while stack:
        cell = stack[len(stack) - 1]
        unvisited_neighbors: list[Cell] = [
            neighbour
            for neighbour in maze.get_unvisited_neighbour(cell)
            if not neighbour.visited
        ]

        if unvisited_neighbors:
            random_index = random.randint(0, len(unvisited_neighbors) - 1)
            selected_neighbor = unvisited_neighbors[random_index]

            maze.open(cell, selected_neighbor)
            stack.append(selected_neighbor)
        else:
            stack.remove(cell)

    maze.find_exit()
    maze.transform_in_file()
