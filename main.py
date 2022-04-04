from collections import defaultdict
from models import Board
from simulator import Simulation
import os
import json


def get_grid(filename: str) -> defaultdict:
    """Returns a defaultdict representing the grid of the board."""
    grid = defaultdict(bool)
    try:
        with open(filename) as f:
            board_config = json.load(f)
            for cell in board_config:
                # Split string into tuple
                cell = tuple(int(x) for x in cell.split(","))
                grid[cell] = True

    except FileNotFoundError:
        pass  # No config file found

    return grid


if __name__ == "__main__":
    width = os.get_terminal_size().columns
    height = os.get_terminal_size().lines
    grid = get_grid("board_config.json")

    board = Board(width, height, grid=grid)
    simulation = Simulation(board=board, frame_time=0.1)
    simulation.run()
