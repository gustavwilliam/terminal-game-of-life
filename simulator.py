import time
from keyboard import KBHit
from models import Board, Cell

DIRECTION_MAP = {
    0: (0, -1),
    1: (1, 0),
    2: (0, 1),
    3: (-1, 0),
}


class Simulation:
    def __init__(
        self,
        board: Board,
        frame_time: float = 0.5,
        render_reference: Cell = (0, 0),
    ):
        """Initializes a new simulation."""
        self.board = board
        self.frame_time = frame_time
        self.render_reference = render_reference
        self.paused = False

    def render(self):
        """Returns a string representation of the simulation."""
        return "\n".join(self.board.render_list(self.render_reference))  # type: ignore

    def run(self):
        """Runs the simulation until it is stopped."""
        kb = KBHit()
        print("\033[?25l", end="")  # Hide cursor
        print(end="\033[H\033[m\033[2J", flush=True)  # Clear screen

        try:
            while True:
                print("\033[H", end=self.render(), flush=True)
                time.sleep(self.frame_time)

                while kb.kbhit():
                    key = kb.get_key()
                    if key in DIRECTION_MAP.keys():
                        direction = DIRECTION_MAP[key]  # type: ignore
                        self.render_reference = (
                            self.render_reference[0] + direction[0],
                            self.render_reference[1] + direction[1],
                        )
                    elif key == " ":
                        self.paused = not self.paused
                    elif key == "q":
                        exit()

                if not self.paused:
                    self.board.simulate_iteration()

        finally:
            kb.set_normal_term()
            print("\033[?25h", end="")  # Show cursor again
