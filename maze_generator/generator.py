import random

from config import read_config_generator


class Cell:

    def __init__(self, c, l, entry_col=0, entry_line=0):
        self.visited: bool = False
        self.is_wall: bool = True

        self._c: int = c
        self._l: int = l

        self.entry = True if c == entry_col and l == entry_line else False
        self.exit = False

    def __str__(self) -> str:
        return "({}, {}: {})".format(
            self._c,
            self._l,
            self.is_wall,
        )

    def display(self):
        if self.is_wall:
            print("⬜", end="")
        elif self.entry:
            print("🟩", end="")
        elif self.exit:
            print("🟥", end="")
        else:
            print("🟦", end="")

    def get_c(self):
        return self._c

    def get_l(self):
        return self._l


class Maze:
    # Quand on parcours un tableau et qu'on veut les cases autour
    # d'une on créé un tableau de taille n+2
    # Grace à ça les contours ne sont pas à gérer de façon particulères

    def __init__(self, column, line, entry_col=0, entry_line=0) -> None:
        self._line: int = line
        self._column: int = column
        self.maze: list[list[Cell]] = [
            [Cell(y - 1, x - 1, entry_col, entry_line) for y in range(column + 2)]
            for x in range(line + 2)
        ]

        # All edges are already visited to avoid use in algorithm
        for i in range(line + 2):
            self.maze[i][0].visited = True
            self.maze[i][0].is_wall = True
            self.maze[i][column + 1].visited = True
            self.maze[i][column + 1].is_wall = True

        for j in range(column + 2):
            self.maze[0][j].visited = True
            self.maze[0][j].is_wall = True
            self.maze[line + 1][j].visited = True
            self.maze[line + 1][j].is_wall = True

    def get(self, col: int, line: int) -> Cell:
        # Du coup le vrai 0,0 du tableau et en 1,1
        return self.maze[line + 1][col + 1]

    def get_neighbours(self, cell: Cell):
        result: list[Cell] = []
        offset: list[int] = [-1, 0, 1]
        for offset_c in offset:
            for offset_l in offset:
                # Get only direct neighbors and not diagonal and itself
                if (offset_c != 0 or offset_l != 0) and (
                    abs(offset_c) != abs(offset_l)
                ):
                    c = cell.get_c() + offset_c
                    l = cell.get_l() + offset_l
                    neighbour: Cell = self.get(c, l)
                    result.append(neighbour)
        return result

    def get_unvisited_neighbour(self, cell: Cell) -> list[Cell]:
        neighbours = self.get_neighbours(cell)
        return [cell for cell in neighbours if not cell.visited]

    def open(self, current_cell: Cell, neighbor: Cell) -> None:
        neighbor.is_wall = False
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
        neighbors: list[Cell] = self.get_neighbours(cell)
        result: list[Cell] = []

        for n in neighbors:
            if not n.is_wall:
                result.append(n)
        return result

    def display(self):
        for line in self.maze:
            for cell in line:
                cell.display()
            print("\n", end="")

    def transform_in_file(self):
        # TODO
        pass


def generate():
    line, column, entry_col, entry_line = read_config_generator()

    maze = Maze(line=line, column=column, entry_col=entry_col, entry_line=entry_line)

    # Default entry
    default_cell: Cell = maze.get(entry_col, entry_line)
    default_cell.visited = True
    default_cell.is_wall = False

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
    maze.display()
