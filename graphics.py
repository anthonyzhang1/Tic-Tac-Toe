"""Handles the game's graphics, using tkinter."""

from game import Game, Square
from tkinter import font
import tkinter as tk

BUTTON_FOREGROUND_COLOUR = "black"
"""The foreground colour for the buttons used for the board."""
BUTTON_HIGHLIGHT_BACKGROUND_COLOUR = "lightblue"
"""The highlight background colour for the buttons used for the board."""

class Graphics(tk.Tk):
    """Handles the display of the GUI window, and the label and board within."""
    def __init__(self, game: Game):
        """Initializes the game's graphics and logic."""
        super().__init__()
        self.title("Tic-tac-toe")  # Title of the window
        self._squares: dict[tk.Button] = {}
        self._game: Game = game
        self._create_menu()
        self._create_display()
        self._create_board()

    def _create_menu(self):
        """Creates a menu with options to start a new game or exit the game."""
        menu_bar = tk.Menu(master=self)
        self.config(menu=menu_bar)  # Sets `menu_bar` as the main menu

        file_menu = tk.Menu(master=menu_bar, tearoff="off")  # The "File" option in the menu
        file_menu.add_command(label="New Game", command=self.reset_board)  # Adds an option to start a new game
        file_menu.add_separator()
        file_menu.add_command(label="Quit", command=quit)  # Adds an option to quit the game

        menu_bar.add_cascade(label="File", menu=file_menu)  # Adds the "File" option to the menu bar

    def _create_display(self):
        """Creates the display frame and the label above the board."""
        display_frame = tk.Frame(master=self)
        display_frame.pack(fill=tk.X)

        # The label shown above the board
        self.display = tk.Label(
            master=display_frame,
            text=f"{self._game.current_player.piece}, make the first move!",
            font=font.Font(size=20, weight="bold"),
        )

        self.display.pack()

    def _create_board(self):
        """Creates the board using a grid of buttons."""
        board_frame = tk.Frame(master=self)
        board_frame.pack()

        for row in range(self._game.board_size):
            self.rowconfigure(row, weight=1, minsize=50)
            self.columnconfigure(row, weight=1, minsize=50)

            # Creates an empty button for every square in the board
            for column in range(self._game.board_size):
                button = tk.Button(
                    master=board_frame,
                    text="",
                    font=font.Font(size=40, weight="bold"),  # Determines the size of the squares
                    fg=BUTTON_FOREGROUND_COLOUR,
                    width=4,
                    height=2,
                    highlightbackground=BUTTON_HIGHLIGHT_BACKGROUND_COLOUR,
                )

                self._squares[button] = (row, column)  # The buttons are now the squares in the board
                button.bind("<ButtonPress-1>", self.play)  # Binds the click event of every button with play()

                button.grid(
                    row=row,
                    column=column,
                    sticky="NSEW"
                )

    def _display_piece(self, clicked_button: tk.Button):
        """Displays the current player's piece on the clicked button."""
        clicked_button.config(
            text=self._game.current_player.piece,  # Displays the piece
            fg=self._game.current_player.colour  # The colour of the piece
        )

    def _update_label(self, message, colour="black"):
        """Updates the label shown above the board with the given message and colour."""
        self.display.config(text=message, fg=colour)

    def _highlight_winning_squares(self):
        """Highlights the squares containing the winner's combination."""
        button: tk.Button
        for button, coordinates in self._squares.items():
            # Finds the winner's combination and highlights them with the winner's colour.
            if coordinates in self._game.winner_combination:
                button.config(
                    default="active",
                    highlightcolor=self._game.current_player.colour,
                    highlightthickness=2
                )

    def play(self, event: tk.Event):
        """Handles a player's move."""
        clicked_button = event.widget  # The button pressed on the board
        row, column = self._squares[clicked_button]  # The row and column of the clicked button
        move = Square(row, column, self._game.current_player.piece)  # Create a move from the button clicked

        # If the move is invalid, do not do anything
        if not self._game.is_valid_move(move):
            return

        # If the move is valid:
        self._display_piece(clicked_button)  # Display the current player's piece on the clicked button
        self._game.process_move(move)  # Processes the move and checks if there is a winner

        if self._game.is_tied():  # If the game is tied
            self._update_label(message="The game is a tie!", colour="green")

        elif self._game.has_winner():  # If the game has a winner
            self._highlight_winning_squares()  # Highlights the winning squares
            message = f"{self._game.current_player.piece} won!"
            message_colour = self._game.current_player.colour

            self._update_label(message, message_colour)

        else:  # If the game is not over yet
            self._game.switch_player()  # Ends the current player's turn
            message = f"{self._game.current_player.piece}'s turn."
            self._update_label(message)

    def reset_board(self):
        """Resets the game's board so a new game can be played."""
        self._game.reset_game()
        self._update_label(message=f"{self._game.current_player.piece}, make the first move!")

        # Resets all the buttons in the board to their initial state
        for button in self._squares.keys():
            button.config(
                default="normal",  # Resets the button highlighting from a won game
                fg=BUTTON_FOREGROUND_COLOUR,
                highlightbackground=BUTTON_HIGHLIGHT_BACKGROUND_COLOUR,
                text=""
            )

def main():
    """Runs the game."""
    game = Game()
    graphics = Graphics(game)
    graphics.mainloop()

if __name__ == "__main__":
    main()