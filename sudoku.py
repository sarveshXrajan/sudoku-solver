import tkinter as tk
from tkinter import Button, messagebox, simpledialog
import sys
from sudoku_solver import *


class SudokuBoardGUI:
    def __init__(self, master, board):
        self.master = master
        self.master.title("Sudoku Board")
        self.create_board()
        # make a copy of the original board
        self.original_board = [row[:] for row in board]
        self.set_values(board)

        self.disable_original_values()

    def create_board(self):
        # create a frame to hold the entry widgets
        self.frame = tk.Frame(
            self.master, highlightbackground="red", highlightthickness=3)
        self.frame.pack()

        # create a 9x9 grid of entry widgets
        self.entries = []
        solve_button = Button(self.frame, text="Solve",
                              command=self.solve_board)
        solve_button.grid(row=9, column=4, columnspan=1)
        check_button = Button(self.frame, text="Check",
                              command=self.check_solution)
        check_button.grid(row=9, column=2, columnspan=1)

        for i in range(9):
            row = []
            for j in range(9):
                validate_cmd = (self.master.register(
                    self.validate_input), '%P')
                entry = tk.Entry(self.frame, width=2, font=(
                    'Arial', 22, 'bold'), validate='key', validatecommand=validate_cmd)
                row.append(entry)
                entry.grid(row=i, column=j, padx=1, pady=1)
            self.entries.append(row)

        # add thick borders to separate 3x3 blocks
        for i in range(0, 9, 3):
            for j in range(0, 9, 3):
                for k in range(3):
                    for l in range(3):
                        self.entries[i+k][j+l].grid(padx=(3, 1), pady=(3, 1))
                self.entries[i][j].grid(padx=(3, 1), pady=(3, 1))

        reset_button = Button(self.frame, text="New", command=self.reset_board)
        reset_button.grid(row=9, column=6, columnspan=1)

    def reset_board(self):
        # destroy the existing frame and create a new one
        self.frame.destroy()
        self.create_board()

        # display a message box to prompt the user to enter a new Sudoku board as a string
        while True:
            new_board_string = simpledialog.askstring(
                "New Sudoku Board", "Enter a new Sudoku board as a string of 81 characters:")
            if new_board_string is None:
                sys.exit(0)
            elif len(new_board_string) != 81 or not new_board_string.isdigit():
                messagebox.showwarning(
                    title="Invalid Input", message="Invalid input. Please enter 81 digits.")
            else:
                break

        # update the board with the new values
        new_board_values = [[int(new_board_string[i*9 + j])
                             for j in range(9)] for i in range(9)]
        self.original_board = [row[:] for row in new_board_values]
        self.set_values(new_board_values)
        self.disable_original_values()  # disable original values again

    def validate_input(self, new_value):
        if new_value.isdigit() or new_value == '':
            return True
        else:
            return False

    def set_values(self, values):
        for i in range(9):
            for j in range(9):
                value = values[i][j]
                entry = self.entries[i][j]
                entry.delete(0, 'end')
                if value != 0:
                    entry.insert(0, str(value))
                # set the state of the Entry widget to "disabled" if the cell has a value in the original board
                if self.original_board[i][j] != 0:
                    entry.config(state="disabled")

    def disable_original_values(self):
        # disable the Entry widgets for cells that have a value in the original board
        for i in range(9):
            for j in range(9):
                if self.original_board[i][j] != 0:
                    entry = self.entries[i][j]
                    entry.config(state="disabled")

    def solve_board(self):
        # solve the original board instead of the user-modified board
        solution = solve_sudoku(self.original_board)
        if solution is not None:
            # update the original board with the solution
            self.original_board = solution
            # set the values of the entry widgets based on the updated original board
            self.set_values(self.original_board)
            # get the solve button widget by name
            solve_button = self.frame.nametowidget('!button')
            solve_button.config(state='disabled')  # disable the button
        else:
            print("No solution found.")

    def check_solution(self):
        # create a 2D list to hold the current board values
        current_board = []
        for i in range(9):
            row = []
            for j in range(9):
                entry = self.entries[i][j].get()
                if entry == "":
                    row.append(0)
                else:
                    row.append(int(entry))

            current_board.append(row)

        # get the solved board
        solved_board = solve_sudoku(self.original_board)

        # check if the current board is equal to the solved board
        if current_board == solved_board:
            messagebox.showinfo(title="Congratulations!",
                                message="You have solved the puzzle!")
        else:
            messagebox.showwarning(
                title="Oops!", message="Your solution is not correct. Please try again.")


if __name__ == '__main__':
    while True:
        # prompt the user to enter the Sudoku board as a string
        root = tk.Tk()
        root.withdraw()
        board_string = simpledialog.askstring(
            title="Sudoku Board",
            prompt="Enter the Sudoku board as a string of 81 characters:"
        )
        root.destroy()

        # check if the input string is valid
        if board_string is None:
            # the user clicked on "Cancel" or closed the message box
            sys.exit(0)
        elif len(board_string) != 81 or not board_string.isdigit():
            # the input string is invalid, show a warning message and loop again
            messagebox.showwarning(
                title="Invalid Input",
                message="Invalid input. Please enter 81 digits."
            )
        else:
            # the input string is valid, convert it to a 2D list of integers and break the loop
            board_values = [[int(board_string[i*9 + j])
                             for j in range(9)] for i in range(9)]
            break

    # create the GUI and display the board
    root = tk.Tk()
    app = SudokuBoardGUI(root, board_values)
    app.set_values(board_values)
    root.mainloop()


#  070000043040009610800634900094052000358460020000800530080070091902100005007040802
