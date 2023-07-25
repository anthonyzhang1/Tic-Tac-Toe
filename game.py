"""Handles the game's logic."""

from graphics import BOARD_SIZE, Graphics
from itertools import cycle
from typing import NamedTuple

EMPTY_SQUARE = ""
"""Represents an empty square, i.e. a square with no piece in it."""

class Player(NamedTuple):
    """Represents the two players playing the game, and their respective pieces and colours."""
    piece: str
    """The player's piece, e.g. 'X' or 'O'."""
    colour: str
    """The colour of the player's piece."""

class Square(NamedTuple):
    """Represents a square in the board, and the piece in it, if any."""
    row: int
    """The row of the square in the board."""
    column: int
    """The column of the square in the board."""
    piece: str = EMPTY_SQUARE
    """The piece in the square. The value EMPTY_SQUARE means the square is empty."""

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
        """The players in the game."""
        self.board_size = board_size
        """The size of the playing board, i.e. the number of rows and columns it has."""
        self.current_player = next(self._players)
        """The player whose turn it is."""
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
        self._current_squares = [[Square(row, column) for column in range(self.board_size)] for row in range(self.board_size)]

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

        return rows + columns + [down_right_diagonal, down_left_diagonal]
    
    def is_valid_move(self, move):
        """
        A move is valid if the selected square is empty, and the game is not over.
        Returns True if the move is valid, and False otherwise.
        """
        square_is_empty = self._current_squares[move.row][move.column].piece == EMPTY_SQUARE
        game_is_not_over = not self._has_winner  # The game is not over if there is no winner

        return square_is_empty and game_is_not_over
    
    def process_move(self, move):
        """Process the move played and check if it is a win."""
        self._current_squares[move.row][move.column] = move  # Update the list of squares with the new move

        # A combination is a row, column, or diagonal.
        for combination in self._winning_combinations:
            # Retrieves all the pieces in the current combination.
            results = set(self._current_squares[n][m].piece for n, m in combination)

            # Checks if the current combination contains three-in-a-row of the same piece, e.g. X|X|X, and not X|X|O or X|_|X.
            is_win = (len(results) == 1) and (EMPTY_SQUARE not in results)

            if is_win:
                self._has_winner = True
                self.winner_combination = combination  # The winning combination
                break

    def has_winner(self):
        """Return True if the game has a winner, and False otherwise."""
        return self._has_winner
    
    def is_tied(self):
        """
        Checks if the game is tied, i.e. if there is no winner and the board is entirely filled with pieces.
        Return True if the game is tied, and False otherwise.
        """
        no_winner = not self._has_winner
        played_moves = (square.piece for row in self._current_squares for square in row)

        # `all(played_moves)` returns True if there are no empty squares.
        return no_winner and all(played_moves)
    
    def switch_player(self):
        """Switches the current player to the next player."""
        self.current_player = next(self._players)

def main():
    """Create the game's GUI and run its main loop."""
    GUI = Graphics()
    GUI.mainloop()

if __name__ == "__main__":
    main()