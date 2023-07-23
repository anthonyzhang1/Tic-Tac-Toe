"""Handles the graphics for the game, using tkinter."""

import tkinter as tk
from tkinter import font

BOARD_ROWS = 3  # The number of rows in the board
BOARD_COLUMNS = 3  # The number of columns in the board

class Graphics(tk.Tk):
    """
    Handles the display of the GUI window, and the label and board within.
    """
    
    def __init__(self):
        """
        Initializes the GUI window, the label, and the board.
        """
        super().__init__()
        self.title("Tic-tac-toe")  # Title of the window
        self._squares = {}
        self._create_display()
        self._create_board()
        
    def _create_display(self):
        """
        Creates the display frame and the label above the board.
        """
        display_frame = tk.Frame(master=self)
        display_frame.pack(fill=tk.X)

        # The label shown above the board
        self.display = tk.Label(
            master=display_frame,
            text="Make the first move!", # Initial text in the label
            font=font.Font(size=20, weight="bold"),
        )

        self.display.pack()

    def _create_board(self):
        """
        Creates the board using a grid of buttons.
        """
        board_frame = tk.Frame(master=self)
        board_frame.pack()

        for row in range(BOARD_ROWS):
            self.rowconfigure(row, weight=1, minsize=50)
            self.columnconfigure(row, weight=1, minsize=50)

            # Creates an empty button for every square in the board
            for column in range(BOARD_COLUMNS):
                button = tk.Button(
                    master=board_frame,
                    text="",
                    font=font.Font(size=40, weight="bold"),  # Determines the size of the squares
                    fg="black",
                    width=3,
                    height=2,
                    highlightbackground="lightblue",
                )

                self._squares[button] = (row, column)  # The buttons are now the squares in the board

                button.grid(
                    row=row,
                    column=column,
                    padx=5,
                    pady=5,
                    sticky="NSEW"
                )