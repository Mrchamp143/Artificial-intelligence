import tkinter as tk

class TowerOfHanoiGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Tower of Hanoi")

        self.canvas = tk.Canvas(root, width=600, height=400, bg='white')
        self.canvas.pack()

        self.poles = {'A': (150, 300), 'B': (300, 300), 'C': (450, 300)}
        self.disk_colors = ['red', 'green', 'blue', 'yellow', 'purple']
        self.disks = {'A': [], 'B': [], 'C': []}  # Dictionary to track disks on each pole

        self.create_poles()
        self.create_disks(3)  # Initialize with 3 disks

        self.step_button = tk.Button(root, text="Step", command=self.step)
        self.step_button.pack(side='left')

        self.reset_button = tk.Button(root, text="Reset", command=self.reset)
        self.reset_button.pack(side='left')

        self.instructions = tk.Label(root, text="Instructions:\nClick 'Step' to move disks.\nClick 'Reset' to start over.")
        self.instructions.pack(side='bottom')

        self.moves = []
        self.current_move = 0

        # Variables for manual dragging
        self.selected_disk = None
        self.disk_start_pos = None
        self.drag_start_x = None
        self.drag_start_y = None

        self.canvas.bind("<Button-1>", self.on_click)
        self.canvas.bind("<B1-Motion>", self.on_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_drop)

    def create_poles(self):
        for pole, (x, y) in self.poles.items():
            self.canvas.create_line(x, y-150, x, y, width=5, fill='black')
            self.canvas.create_text(x, y+20, text=pole, font=('Arial', 16))

    def create_disks(self, num_disks):
        self.disks = {'A': [], 'B': [], 'C': []}
        for i in range(num_disks):
            disk_width = 100 - i * 20
            disk_color = self.disk_colors[i % len(self.disk_colors)]
            disk = self.canvas.create_rectangle(0, 0, disk_width, 20, fill=disk_color, outline='black')
            self.disks['A'].append(disk)
            self.canvas.coords(disk, self.poles['A'][0] - disk_width / 2, self.poles['A'][1] - 20 * (i+1), self.poles['A'][0] + disk_width / 2, self.poles['A'][1] - 20 * i)

    def reset(self):
        self.canvas.delete('all')
        self.create_poles()
        self.create_disks(3)
        self.moves = []
        self.current_move = 0
        self.instructions.config(text="Instructions:\nClick 'Step' to move disks.\nClick 'Reset' to start over.")

    def step(self):
        if self.current_move >= len(self.moves):
            self.instructions.config(text="No more moves.")
            return
        
        move = self.moves[self.current_move]
        self.perform_move(move)
        self.current_move += 1

    def perform_move(self, move):
        from_pole, to_pole = move
        disk = self.get_top_disk(from_pole)
        if disk:
            disk_width = self.canvas.coords(disk)[2] - self.canvas.coords(disk)[0]
            self.canvas.move(disk, self.poles[to_pole][0] - self.poles[from_pole][0], self.poles[to_pole][1] - self.poles[from_pole][1])
            self.update_disk_stack(from_pole, to_pole, disk)

    def get_top_disk(self, pole):
        if not self.disks[pole]:
            return None
        return self.disks[pole][-1]

    def update_disk_stack(self, from_pole, to_pole, disk):
        self.disks[from_pole].remove(disk)
        self.disks[to_pole].append(disk)

    def moveTower(self, height, fromPole, toPole, withPole):
        if height >= 1:
            self.moveTower(height - 1, fromPole, withPole, toPole)
            self.moves.append((fromPole, toPole))
            self.moveTower(height - 1, withPole, toPole, fromPole)

    def on_click(self, event):
        if self.selected_disk is not None:
            return

        for pole, (x, y) in self.poles.items():
            if x - 100 <= event.x <= x + 100 and y - 200 <= event.y <= y:
                disk = self.get_top_disk(pole)
                if disk and self.canvas.coords(disk)[1] <= event.y <= self.canvas.coords(disk)[3]:
                    self.selected_disk = disk
                    self.disk_start_pos = pole
                    self.drag_start_x = event.x
                    self.drag_start_y = event.y
                    return

    def on_drag(self, event):
        if self.selected_disk is None:
            return

        dx = event.x - self.drag_start_x
        dy = event.y - self.drag_start_y
        self.canvas.move(self.selected_disk, dx, dy)
        self.drag_start_x = event.x
        self.drag_start_y = event.y

    def on_drop(self, event):
        if self.selected_disk is None:
            return

        disk_coords = self.canvas.coords(self.selected_disk)
        drop_pole = None
        for pole, (x, y) in self.poles.items():
            if x - 100 <= event.x <= x + 100 and y - 200 <= event.y <= y:
                drop_pole = pole
                break

        if drop_pole:
            # Update position
            disk_width = disk_coords[2] - disk_coords[0]
            new_x = self.poles[drop_pole][0] - disk_width / 2
            new_y = self.poles[drop_pole][1] - 20 * (len(self.disks[drop_pole]) + 1)
            self.canvas.coords(self.selected_disk, new_x, new_y, new_x + disk_width, new_y + 20)
            self.update_disk_stack(self.disk_start_pos, drop_pole, self.selected_disk)

        # Reset the dragging state
        self.selected_disk = None
        self.disk_start_pos = None
        self.drag_start_x = None
        self.drag_start_y = None

# Main application
root = tk.Tk()
app = TowerOfHanoiGUI(root)
app.moveTower(3, 'A', 'C', 'B')  # Start solving the Tower of Hanoi with 3 disks
root.mainloop()
