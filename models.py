from collections import defaultdict

Cell = tuple[int, int]


class Board:
    def __init__(
        self,
        dimensions: tuple[int, int],
        cell_width: int = 2,
        grid: defaultdict | None = None,
    ):
        self.grid = grid or defaultdict(bool)
        self.dimensions = dimensions
        self.cell_width = cell_width

    def neighbours(self, cell: Cell) -> int:
        """Returns the number of alive neighbours of a cell."""
        return sum(
            [
                self.grid[(x, y)]
                for x in range(cell[0] - 1, cell[0] + 2)
                for y in range(cell[1] - 1, cell[1] + 2)
                if (x, y) != cell
            ]
        )

    def to_simulate(self) -> set[tuple[int, int]]:
        """
        Returns the set of cells that should be simulated next.

        All cells that are alive, or have neighbours that are alive should be simulated.

        XXXXXX
        XX██XXXX
        XX████XXXX
        XXXXXX██XX
            XXXXXX
        """
        cells = set()
        for cell, alive in self.grid.items():
            if alive:
                for x in range(cell[0] - 1, cell[0] + 2):
                    for y in range(cell[1] - 1, cell[1] + 2):
                        cells.add((x, y))
            else:
                cells.add(cell)

        return cells

    def cell_survives(self, cell: Cell):
        """
        Returns whether a cell survives or not.

        The following rules apply:
        - Any living cell with two or three neighbours survives
        - Any dead cell with exactly three live neighbours becomes alive
        - All other cells die or stay dead
        """
        if self.grid[cell]:  # Cell is alive
            return self.neighbours(cell) in [2, 3]
        return self.neighbours(cell) == 3

    def simulate_iteration(self):
        """Simulates the next iteration of the board and updates `self.grid`."""
        new_grid = defaultdict(bool)
        for cell in self.to_simulate():
            if self.cell_survives(cell):
                new_grid[cell] = True

        self.grid = new_grid

    def render_point(self, cell: Cell) -> str:
        if self.grid[cell]:
            return "█" * self.cell_width
        return " " * self.cell_width

    def render(self) -> str:
        """Returns a string representation of the board."""
        rows = []
        for y in range(self.dimensions[1]):
            rows.append(
                "".join([self.render_point((x, y)) for x in range(self.dimensions[0])])
            )

        return "\n".join(rows)
