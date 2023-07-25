"""
Handles the game's logic.
TODO: Expand on this when more features are added.
"""

from graphics import BOARD_SIZE, Graphics
from itertools import cycle
from typing import NamedTuple

class Player(NamedTuple):
    """Represents the two players playing the game, and their respective pieces and colours."""
    piece: str
    """The player's piece, e.g. 'X' or 'O'."""
    colour: str
    """The colour of the player's piece."""

class Square(NamedTuple):
    """Represents a square in the board, and which piece is in it, if any."""
    row: int
    """The row of the square in the board."""
    column: int
    """The column of the square in the board."""
    piece: str = ""
    """The piece in the square. An empty string means the square is empty."""

PLAYERS = (
    Player(piece="X", colour="white"),
    Player(piece="O", colour="black"),
)
"""The players in the game, and their pieces and colours."""

class Game:
    """Handles the game's logic."""
    def __init__(self, players=PLAYERS, board_size=BOARD_SIZE):
        """Initializes the game."""
        self._players = cycle(players)  # iterates through `players` in a cycle
        self.board_size = board_size
        self.current_player = next(self._players)
        self.winner_combination = []
        """The combination of squares that defines the winner."""
        self._current_squares = []
        """A list with all of the squares in the game."""
        self._has_winner = False
        """Used to determine if the game has a winner."""
        self._winning_combinations = []
        """Contains the square combinations that define a win."""
        self._setup_board()
        self._winning_combinations = self._get_winning_combinations()

    def _setup_board(self):
        """Initialize all of the squares in the board as empty squares, in the form [row][column]."""
        self._current_squares = [
            [Square(row, column) for column in range(self.board_size)]
            for row in range(self.board_size)
        ]

    def _get_winning_combinations(self):
        """Returns a list of all of the winning square combinations, i.e. three-in-a-row in a row, column, or diagonal."""
        # A list with lists of rows in the board, e.g. [..., [(2, 0), (2, 1), (2, 2)], ...].
        # Each sublist represents a winning combination, i.e. three-in-a-row in a row.
        rows = [[(square.row, square.column) for square in row] for row in self._current_squares]

        # A list with lists of columns in the board, e.g. [..., [(0, 2), (1, 2), (2, 2)], ...].
        # Each sublist represents a winning combination, i.e. three-in-a-row in a column.
        columns = [list(column) for column in zip(*rows)]

        # A list with the squares from the top-left to bottom-right diagonal in the board, e.g. [(0, 0), (1, 1), (2, 2), ...].
        # The list represents a winning combination, i.e. three-in-a-row in a diagonal.
        down_right_diagonal = [row[i] for i, row in enumerate(rows)]

        # A list with the squares from the top-right to bottom-left diagonal in the board, e.g. [(0, 2), (1, 1), (2, 0), ...].
        # The list represents a winning combination, i.e. three-in-a-row in a diagonal.
        down_left_diagonal = [col[j] for j, col in enumerate(reversed(columns))]

        # Returns a list of all of the winning square combinations, i.e. three-in-a-row in a row, column, or diagonal.
        return rows + columns + [down_right_diagonal, down_left_diagonal]

def main():
    """Create the game's GUI and run its main loop."""
    GUI = Graphics()
    GUI.mainloop()

if __name__ == "__main__":
    main()