import time
from models import Board


class Simulation:
    def __init__(
        self,
        board: Board,
        frame_time: float = 0.5,
    ):
        """Initializes a new simulation."""
        self.board = board
        self.frame_time = frame_time

    def render(self):
        """Returns a string representation of the simulation."""
        return "\n".join(self.board.render_list())

    def run(self):
        """Runs the simulation until it is stopped."""
        print("\033[?25l", end="")  # Hide cursor
        print(end="\033[H\033[m\033[2J", flush=True)  # Clear screen

        try:
            while True:
                print("\033[H", end=self.render(), flush=True)
                self.board.simulate_iteration()
                time.sleep(self.frame_time)

        finally:
            print("\033[?25h", end="")  # Show cursor again
            print(flush=True)  # Send out newline
