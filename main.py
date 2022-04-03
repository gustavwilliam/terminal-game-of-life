from models import Board
from simulator import Simulation
import os


if __name__ == "__main__":
    width = os.get_terminal_size().columns
    height = os.get_terminal_size().lines
    board = Board(width, height)

    board.grid[(4, 3)] = True
    board.grid[(3, 4)] = True
    board.grid[(4, 4)] = True
    board.grid[(5, 4)] = True

    simulation = Simulation(board=board)
    simulation.run()
