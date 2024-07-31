import tkinter as tk
from tkinter import messagebox

class GraphVisualization(tk.Tk):
    def __init__(self, graph):
        super().__init__()
        self.title("Depth First Search Visualization")
        self.canvas = tk.Canvas(self, width=800, height=600, bg="white")
        self.canvas.pack()
        self.graph = graph
        self.node_positions = {}
        self.visited = set()
        self.paths = []  
        self.goal_node = None

        # GUI components for DFS
        self.goal_label = tk.Label(self, text="Enter Goal Node:")
        self.goal_label.pack(pady=5)
        self.goal_entry = tk.Entry(self)
        self.goal_entry.pack(pady=5)
        self.start_button = tk.Button(self, text="Start DFS", command=self.start_dfs)
        self.start_button.pack(pady=5)

        self.setup_graph()

    def setup_graph(self):
        # Define positions for 7 nodes
        self.node_positions = {
            '1': (200, 100),
            '2': (400, 100),
            '3': (600, 100),
            '4': (150, 250),
            '5': (300, 250),
            '6': (500, 250),
            '7': (650, 250)
        }

        # Draw nodes
        for node, position in self.node_positions.items():
            x, y = position
            self.canvas.create_oval(x-20, y-20, x+20, y+20, fill="lavender", tags=node)
            self.canvas.create_text(x, y, text=node, font=("Arial", 12, "bold"))

        # Draw edges
        for node, neighbors in self.graph.items():
            x1, y1 = self.node_positions.get(node, (0, 0))
            for neighbor in neighbors:
                if node < neighbor:  # Avoid drawing duplicate edges
                    x2, y2 = self.node_positions.get(neighbor, (0, 0))
                    self.canvas.create_line(x1, y1, x2, y2, fill="lavender", width=1, tags=f"{node}-{neighbor}")

    def start_dfs(self):
        self.goal_node = self.goal_entry.get().strip()
        if self.goal_node not in self.node_positions:
            messagebox.showerror("Error", f"Goal node '{self.goal_node}' not found in graph!")
            return

        self.visited.clear()
        self.paths.clear()
        self.canvas.delete("highlight")
        self.canvas.delete("node_visited")
        self.canvas.delete("path")

        # Start DFS from node '1'
        self.dfs('1', [])

        if not self.paths:
            messagebox.showinfo("Result", f"No path found to goal node '{self.goal_node}'")
        else:
            paths_str = "\n".join([" -> ".join(path) for path in self.paths])
            messagebox.showinfo("Result", f"Paths to goal node '{self.goal_node}':\n{paths_str}")

    def dfs(self, node, path):
        if node not in self.visited:
            self.visited.add(node)
            path.append(node)
            x, y = self.node_positions[node]

            # Mark the current node as visited
            self.canvas.create_oval(x-20, y-20, x+20, y+20, fill="lightgreen", tags="node_visited")
            self.update()
            self.after(500)

            if node == self.goal_node:
                self.paths.append(path.copy())
                self.draw_path(path)
            else:
                for neighbor in self.graph[node]:
                    if neighbor not in self.visited:
                        x1, y1 = self.node_positions[node]
                        x2, y2 = self.node_positions[neighbor]
                        self.canvas.create_line(x1, y1, x2, y2, fill="red", width=2, tags="highlight")
                        self.update()
                        self.after(500)
                        self.dfs(neighbor, path)

            path.pop()
            self.visited.remove(node)

    def draw_path(self, path):
        # Draw the final path
        for i in range(len(path) - 1):
            x1, y1 = self.node_positions[path[i]]
            x2, y2 = self.node_positions[path[i+1]]
            self.canvas.create_line(x1, y1, x2, y2, fill="blue", width=3, tags="path")
        self.update()

if __name__ == "__main__":
    initial_graph = {
        '1': ['2', '3'],
        '2': ['1', '4', '5'],
        '3': ['1', '6', '7'],
        '4': ['2'],
        '5': ['2', '6'],
        '6': ['3', '5'],
        '7': ['3']
    }

    app = GraphVisualization(initial_graph)
    app.mainloop()
