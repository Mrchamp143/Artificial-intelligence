import tkinter as tk
from tkinter import messagebox

class JugProblemGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Jug Problem Solver")

        # Jug capacities
        self.max1, self.max2, self.max3, self.fill = 5, 7, 11, 4  # Set the fill amount as needed
        self.jug1, self.jug2, self.jug3 = 0, 0, 0
        self.visited = set()
        self.steps = []

        # Create UI components
        self.create_widgets()

    def create_widgets(self):
        # Jug 1
        self.jug1_label = tk.Label(self.root, text=f"Jug 1 ({self.max1} liters)")
        self.jug1_label.grid(row=0, column=0)

        self.jug1_var = tk.StringVar(value=f"{self.jug1} liters")
        self.jug1_display = tk.Label(self.root, textvariable=self.jug1_var, font=("Arial", 20))
        self.jug1_display.grid(row=1, column=0)

        # Jug 2
        self.jug2_label = tk.Label(self.root, text=f"Jug 2 ({self.max2} liters)")
        self.jug2_label.grid(row=0, column=1)

        self.jug2_var = tk.StringVar(value=f"{self.jug2} liters")
        self.jug2_display = tk.Label(self.root, textvariable=self.jug2_var, font=("Arial", 20))
        self.jug2_display.grid(row=1, column=1)

        # Jug 3
        self.jug3_label = tk.Label(self.root, text=f"Jug 3 ({self.max3} liters)")
        self.jug3_label.grid(row=0, column=2)

        self.jug3_var = tk.StringVar(value=f"{self.jug3} liters")
        self.jug3_display = tk.Label(self.root, textvariable=self.jug3_var, font=("Arial", 20))
        self.jug3_display.grid(row=1, column=2)

        # Action Buttons
        tk.Button(self.root, text="Fill Jug 1", command=lambda: self.perform_action(self.fill_jug1)).grid(row=2, column=0)
        tk.Button(self.root, text="Fill Jug 2", command=lambda: self.perform_action(self.fill_jug2)).grid(row=2, column=1)
        tk.Button(self.root, text="Fill Jug 3", command=lambda: self.perform_action(self.fill_jug3)).grid(row=2, column=2)
        tk.Button(self.root, text="Empty Jug 1", command=lambda: self.perform_action(self.empty_jug1)).grid(row=3, column=0)
        tk.Button(self.root, text="Empty Jug 2", command=lambda: self.perform_action(self.empty_jug2)).grid(row=3, column=1)
        tk.Button(self.root, text="Empty Jug 3", command=lambda: self.perform_action(self.empty_jug3)).grid(row=3, column=2)
        tk.Button(self.root, text="Pour Jug 1 to Jug 2", command=lambda: self.perform_action(self.pour_jug1_to_jug2)).grid(row=4, column=0, columnspan=3)
        tk.Button(self.root, text="Pour Jug 1 to Jug 3", command=lambda: self.perform_action(self.pour_jug1_to_jug3)).grid(row=5, column=0, columnspan=3)
        tk.Button(self.root, text="Pour Jug 2 to Jug 1", command=lambda: self.perform_action(self.pour_jug2_to_jug1)).grid(row=6, column=0, columnspan=3)
        tk.Button(self.root, text="Pour Jug 2 to Jug 3", command=lambda: self.perform_action(self.pour_jug2_to_jug3)).grid(row=7, column=0, columnspan=3)
        tk.Button(self.root, text="Pour Jug 3 to Jug 1", command=lambda: self.perform_action(self.pour_jug3_to_jug1)).grid(row=8, column=0, columnspan=3)
        tk.Button(self.root, text="Pour Jug 3 to Jug 2", command=lambda: self.perform_action(self.pour_jug3_to_jug2)).grid(row=9, column=0, columnspan=3)
        tk.Button(self.root, text="Solve", command=self.solve).grid(row=10, column=0, columnspan=3)

        # History
        self.history_label = tk.Label(self.root, text="History:")
        self.history_label.grid(row=11, column=0, columnspan=3)

        self.history_display = tk.Text(self.root, height=10, width=50)
        self.history_display.grid(row=12, column=0, columnspan=3)

    def perform_action(self, action):
        action()
        self.update_display()
        if (self.jug1, self.jug2, self.jug3) in self.visited:
            messagebox.showinfo("Jug Problem", "Already visited this state.")
            return
        self.visited.add((self.jug1, self.jug2, self.jug3))
        self.steps.append((self.jug1, self.jug2, self.jug3))
        self.update_history()

    def fill_jug1(self):
        self.jug1 = self.max1

    def fill_jug2(self):
        self.jug2 = self.max2

    def fill_jug3(self):
        self.jug3 = self.max3

    def empty_jug1(self):
        self.jug1 = 0

    def empty_jug2(self):
        self.jug2 = 0

    def empty_jug3(self):
        self.jug3 = 0

    def pour_jug1_to_jug2(self):
        transfer = min(self.jug1, self.max2 - self.jug2)
        self.jug1 -= transfer
        self.jug2 += transfer

    def pour_jug1_to_jug3(self):
        transfer = min(self.jug1, self.max3 - self.jug3)
        self.jug1 -= transfer
        self.jug3 += transfer

    def pour_jug2_to_jug1(self):
        transfer = min(self.jug2, self.max1 - self.jug1)
        self.jug2 -= transfer
        self.jug1 += transfer

    def pour_jug2_to_jug3(self):
        transfer = min(self.jug2, self.max3 - self.jug3)
        self.jug2 -= transfer
        self.jug3 += transfer

    def pour_jug3_to_jug1(self):
        transfer = min(self.jug3, self.max1 - self.jug1)
        self.jug3 -= transfer
        self.jug1 += transfer

    def pour_jug3_to_jug2(self):
        transfer = min(self.jug3, self.max2 - self.jug2)
        self.jug3 -= transfer
        self.jug2 += transfer

    def update_display(self):
        self.jug1_var.set(f"{self.jug1} liters")
        self.jug2_var.set(f"{self.jug2} liters")
        self.jug3_var.set(f"{self.jug3} liters")

    def update_history(self):
        self.history_display.delete(1.0, tk.END)
        for step in self.steps:
            self.history_display.insert(tk.END, f"Jug1: {step[0]}, Jug2: {step[1]}, Jug3: {step[2]}\n")

    def solve(self):
        self.visited.clear()
        self.steps.clear()
        self.jug1, self.jug2, self.jug3 = 0, 0, 0
        self.update_display()
        if not self.solve_helper():
            messagebox.showinfo("Jug Problem", "No solution found")
        else:
            self.update_history()

    def solve_helper(self):
        def pour(jug1, jug2, jug3):
            if jug1 == self.fill or jug2 == self.fill or jug3 == self.fill:
                return True

            if (jug1, jug2, jug3) in self.visited:
                return False

            self.visited.add((jug1, jug2, jug3))

            # Fill Jug1
            if pour(self.max1, jug2, jug3):
                return True
            # Fill Jug2
            if pour(jug1, self.max2, jug3):
                return True
            # Fill Jug3
            if pour(jug1, jug2, self.max3):
                return True
            # Empty Jug1
            if pour(0, jug2, jug3):
                return True
            # Empty Jug2
            if pour(jug1, 0, jug3):
                return True
            # Empty Jug3
            if pour(jug1, jug2, 0):
                return True
            # Pour Jug1 to Jug2
            if jug1 + jug2 <= self.max2:
                if pour(0, jug1 + jug2, jug3):
                    return True
            else:
                if pour(jug1 - (self.max2 - jug2), self.max2, jug3):
                    return True
            # Pour Jug1 to Jug3
            if jug1 + jug3 <= self.max3:
                if pour(0, jug2, jug1 + jug3):
                    return True
            else:
                if pour(jug1 - (self.max3 - jug3), jug2, self.max3):
                    return True
            # Pour Jug2 to Jug1
            if jug2 + jug1 <= self.max1:
                if pour(jug2 + jug1, 0, jug3):
                    return True
            else:
                if pour(self.max1, jug2 - (self.max1 - jug1), jug3):
                    return True
            # Pour Jug2 to Jug3
            if jug2 + jug3 <= self.max3:
                if pour(jug1, 0, jug2 + jug3):
                    return True
            else:
                if pour(jug1, jug2 - (self.max3 - jug3), self.max3):
                    return True
            # Pour Jug3 to Jug1
            if jug3 + jug1 <= self.max1:
                if pour(jug3 + jug1, jug2, 0):
                    return True
            else:
                if pour(self.max1, jug2, jug3 - (self.max1 - jug1)):
                    return True
            # Pour Jug3 to Jug2
            if jug3 + jug2 <= self.max2:
                if pour(jug1, jug3 + jug2, 0):
                    return True
            else:
                if pour(jug1, self.max2, jug3 - (self.max2 - jug2)):
                    return True

            return False

        return pour(self.jug1, self.jug2, self.jug3)

if __name__ == "__main__":
    root = tk.Tk()
    app = JugProblemGUI(root)
    root.mainloop()
