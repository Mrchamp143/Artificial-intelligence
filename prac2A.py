import tkinter as tk
from tkinter import messagebox

class NQueensGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("N-Queens Problem")

        # Board size
        self.size = 8
        self.board = [[0] * self.size for _ in range(self.size)]

        # Create UI components
        self.create_widgets()
        self.create_board()

    def create_widgets(self):
        # Size Input
        tk.Label(self.root, text="Board Size:").grid(row=0, column=0)
        self.size_entry = tk.Entry(self.root, width=5)
        self.size_entry.grid(row=0, column=1)
        self.size_entry.insert(0, str(self.size))

        # Buttons
        tk.Button(self.root, text="Set Size", command=self.set_size).grid(row=0, column=2)
        tk.Button(self.root, text="Check Validity", command=self.check_validity).grid(row=0, column=3)
        tk.Button(self.root, text="Reset", command=self.reset).grid(row=0, column=4)
        tk.Button(self.root, text="Find Solution", command=self.find_solution).grid(row=0, column=5)

        # Board Canvas
        self.canvas = tk.Canvas(self.root, width=400, height=400, bg="white")
        self.canvas.grid(row=1, column=0, columnspan=6)
        self.create_board()

    def create_board(self):
        self.canvas.delete("all")
        self.cell_size = 400 // self.size
        for i in range(self.size):
            for j in range(self.size):
                color = "white" if (i + j) % 2 == 0 else "gray"
                self.canvas.create_rectangle(j * self.cell_size, i * self.cell_size,
                                             (j + 1) * self.cell_size, (i + 1) * self.cell_size,
                                             fill=color, outline="black")
                if self.board[i][j] == 1:
                    self.canvas.create_oval(j * self.cell_size + self.cell_size / 4,
                                            i * self.cell_size + self.cell_size / 4,
                                            (j + 1) * self.cell_size - self.cell_size / 4,
                                            (i + 1) * self.cell_size - self.cell_size / 4,
                                            fill="red")
        self.canvas.bind("<Button-1>", self.on_canvas_click)
  
        
    def on_canvas_click(self, event):
        x = event.x // self.cell_size
        y = event.y // self.cell_size
        if self.board[y][x] == 1:
            self.board[y][x] = 0
        else:
            self.board[y][x] = 1
        self.create_board()

    def set_size(self):
        try:
            new_size = int(self.size_entry.get())
            if new_size < 4:
                raise ValueError("Size must be at least 4.")
            self.size = new_size
            self.board = [[0] * self.size for _ in range(self.size)]
            self.create_board()
        except ValueError as e:
            messagebox.showerror("Invalid Input", f"Please enter a valid board size (integer >= 4).\n{e}")

    def reset(self):
        self.board = [[0] * self.size for _ in range(self.size)]
        self.create_board()

    def check_validity(self):
        if self.is_valid_solution():
            messagebox.showinfo("Validity Check", "The current board is a valid N-Queens solution. Congratulations!")
        else:
            messagebox.showinfo("Validity Check", "The current board is not a valid N-Queens solution.")

    def is_valid_solution(self):
        # Gather positions of all queens
        queens = [(r, c) for r in range(self.size) for c in range(self.size) if self.board[r][c] == 1]

        # Check if we have exactly one queen per row
        if len(queens) != self.size:
            return False

        # Check column constraints
        columns = set()
        for r, c in queens:
            if c in columns:
                return False
            columns.add(c)
        
        # Check diagonal constraints
        diag1 = set()  # r - c
        diag2 = set()  # r + c
        for r, c in queens:
            if (r - c) in diag1 or (r + c) in diag2:
                return False
            diag1.add(r - c)
            diag2.add(r + c)
        
        return True

    def find_solution(self):
        solution = self.solve_n_queens(self.size)
        if solution:
            self.board = [[0] * self.size for _ in range(self.size)]
            for r, c in solution:
                self.board[r][c] = 1
            self.create_board()
            messagebox.showinfo("Solution Found", "A solution has been found and displayed on the board.")
        else:
            messagebox.showinfo("Solution Not Found", "No solution exists for the current board size.")

    def solve_n_queens(self, n):
        def is_safe(board, row, col):
            for i in range(col):
                if board[row][i] == 1:
                    return False
            for i, j in zip(range(row, -1, -1), range(col, -1, -1)):
                if board[i][j] == 1:
                    return False
            for i, j in zip(range(row, n, 1), range(col, -1, -1)):
                if board[i][j] == 1:
                    return False
            return True

        def solve(board, col):
            if col >= n:
                return True
            for i in range(n):
                if is_safe(board, i, col):
                    board[i][col] = 1
                    if solve(board, col + 1):
                        return True
                    board[i][col] = 0
            return False

        board = [[0] * n for _ in range(n)]
        if solve(board, 0):
            return [(r, c) for r in range(n) for c in range(n) if board[r][c] == 1]
        else:
            return None

if __name__ == "__main__":
    root = tk.Tk()
    app = NQueensGUI(root)
    root.mainloop()
