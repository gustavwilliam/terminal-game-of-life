import atexit
import sys
import termios
from select import select

ARROW_CODES = [65, 67, 66, 68]


class KBHit:
    def __init__(self):
        # Save the terminal settings
        self.fd = sys.stdin.fileno()
        self.new_term = termios.tcgetattr(self.fd)
        self.old_term = termios.tcgetattr(self.fd)

        # New terminal setting unbuffered
        self.new_term[3] = self.new_term[3] & ~termios.ICANON & ~termios.ECHO
        termios.tcsetattr(self.fd, termios.TCSAFLUSH, self.new_term)

        # Support normal-terminal reset at exit
        atexit.register(self.set_normal_term)

    def set_normal_term(self):
        """Resets to normal terminal."""
        termios.tcsetattr(self.fd, termios.TCSAFLUSH, self.old_term)

    def get_key(self):
        """
        Returns a keyboard character after kbhit() has been called.

        If an arrow key was pressed, one of the following codes are returned:

        0: up
        1: right
        2: down
        3: left
        """
        key = sys.stdin.read(1)
        if key == "\033":  # Escape sequence
            type_, key = sys.stdin.read(2)
            if type_ == "[":  # Control sequence
                if ord(key) in ARROW_CODES:
                    return ARROW_CODES.index(ord(key))
        else:  # Regular character pressed
            return key

    def kbhit(self):
        """Returns True if keyboard character was hit, False otherwise."""
        dr, _, _ = select([sys.stdin], [], [], 0)
        return dr != []
