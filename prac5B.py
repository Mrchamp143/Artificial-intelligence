import tkinter as tk
from tkinter import messagebox
import random

class TicTacToe(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Tic Tac Toe")
        self.geometry("300x300")
        self.buttons = [[None for _ in range(3)] for _ in range(3)]
        self.current_player = "X"  # Player starts
        self.create_widgets()

    def create_widgets(self):
        # Change background color of the window
        self.configure(bg="lightblue")

        for row in range(3):
            for col in range(3):
                button = tk.Button(self, text="", font=("Arial", 24), width=5, height=2,
                                   command=lambda r=row, c=col: self.on_button_click(r, c),
                                   bg="white", fg="black")
                button.grid(row=row, column=col)
                self.buttons[row][col] = button

        # Create and style the reset button
        reset_button = tk.Button(self, text="Reset", command=self.reset_game, bg="lightgrey")
        reset_button.grid(row=3, column=0, columnspan=3, pady=10)

    def on_button_click(self, row, col):
        button = self.buttons[row][col]
        if button["text"] == "" and not self.check_winner():
            button["text"] = self.current_player
            if self.check_winner():
                messagebox.showinfo("Game Over", f"Player {self.current_player} wins!")
            elif all(self.buttons[r][c]["text"] != "" for r in range(3) for c in range(3)):
                messagebox.showinfo("Game Over", "It's a draw!")
            else:
                self.current_player = "O"  # Computer's turn
                self.after(500, self.computer_move)

    def computer_move(self):
        empty_buttons = [(r, c) for r in range(3) for c in range(3) if self.buttons[r][c]["text"] == ""]
        if empty_buttons:
            row, col = random.choice(empty_buttons)
            self.buttons[row][col]["text"] = "O"
            if self.check_winner():
                messagebox.showinfo("Game Over", "Computer wins!")
            elif all(self.buttons[r][c]["text"] != "" for r in range(3) for c in range(3)):
                messagebox.showinfo("Game Over", "It's a draw!")
            else:
                self.current_player = "X"  # Player's turn

    def check_winner(self):
        # Check rows
        for row in range(3):
            if self.buttons[row][0]["text"] == self.buttons[row][1]["text"] == self.buttons[row][2]["text"] != "":
                return True

        # Check columns
        for col in range(3):
            if self.buttons[0][col]["text"] == self.buttons[1][col]["text"] == self.buttons[2][col]["text"] != "":
                return True

        # Check diagonals
        if self.buttons[0][0]["text"] == self.buttons[1][1]["text"] == self.buttons[2][2]["text"] != "":
            return True
        if self.buttons[0][2]["text"] == self.buttons[1][1]["text"] == self.buttons[2][0]["text"] != "":
            return True

        return False

    def reset_game(self):
        for row in range(3):
            for col in range(3):
                self.buttons[row][col]["text"] = ""
        self.current_player = "X"  # Player starts

if __name__ == "__main__":
    app = TicTacToe()
    app.mainloop()
