# Enhanced Water Jug Problem AI with Animation & Output Controls

import tkinter as tk
from tkinter import messagebox
from collections import deque

# AI Logic for Water Jug Problem (BFS)
def water_jug_bfs(jug1, jug2, target, condition='either', require_empty=False):
    visited = set()
    queue = deque()
    queue.append((0, 0, []))

    while queue:
        a, b, path = queue.popleft()

        if (a, b) in visited:
            continue
        visited.add((a, b))

        path = path + [(a, b)]

        # Check condition
        if ((condition == 'jug1' and a == target) or
            (condition == 'jug2' and b == target) or
            (condition == 'either' and (a == target or b == target))):

            if require_empty:
                if (a == target and b == 0) or (b == target and a == 0):
                    return path
            else:
                return path

        next_states = [
            (jug1, b),       # Fill Jug1
            (a, jug2),       # Fill Jug2
            (0, b),          # Empty Jug1
            (a, 0),          # Empty Jug2
            (min(a + b, jug1), max(0, b - (jug1 - a))),  # Pour Jug2 -> Jug1
            (max(0, a - (jug2 - b)), min(a + b, jug2)),  # Pour Jug1 -> Jug2
        ]

        for state in next_states:
            if state not in visited:
                queue.append((state[0], state[1], path))

    return None

# GUI Code
class WaterJugGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("AI Water Jug Problem - Animated")

        self.create_widgets()

    def create_widgets(self):
        tk.Label(self.root, text="Jug1 Capacity (Max 10):").grid(row=0, column=0)
        tk.Label(self.root, text="Jug2 Capacity (Max 10):").grid(row=1, column=0)
        tk.Label(self.root, text="Target Amount:").grid(row=2, column=0)

        self.jug1_entry = tk.Entry(self.root)
        self.jug2_entry = tk.Entry(self.root)
        self.target_entry = tk.Entry(self.root)

        self.jug1_entry.grid(row=0, column=1)
        self.jug2_entry.grid(row=1, column=1)
        self.target_entry.grid(row=2, column=1)

        # Output type controls
        tk.Label(self.root, text="Target in:").grid(row=3, column=0)
        self.target_var = tk.StringVar(value='either')
        tk.OptionMenu(self.root, self.target_var, 'either', 'jug1', 'jug2').grid(row=3, column=1)

        self.empty_check = tk.IntVar()
        tk.Checkbutton(self.root, text="Other jug must be empty", variable=self.empty_check).grid(row=4, column=0, columnspan=2)

        self.solve_button = tk.Button(self.root, text="Solve", command=self.solve)
        self.solve_button.grid(row=5, column=0, columnspan=2)

        self.canvas = tk.Canvas(self.root, width=300, height=300, bg="white")
        self.canvas.grid(row=6, column=0, columnspan=2, pady=10)

        self.step_text = tk.StringVar()
        self.step_label = tk.Label(self.root, textvariable=self.step_text, wraplength=280, justify='left')
        self.step_label.grid(row=7, column=0, columnspan=2)

    def draw_jugs(self, a, b, jug1_cap, jug2_cap):
        self.canvas.delete("all")
        self.canvas.create_rectangle(50, 50, 110, 250, outline="black", width=2)
        self.canvas.create_rectangle(190, 50, 250, 250, outline="black", width=2)

        jug1_height = 200 * a // jug1_cap if jug1_cap else 0
        jug2_height = 200 * b // jug2_cap if jug2_cap else 0

        self.canvas.create_rectangle(50, 250 - jug1_height, 110, 250, fill="skyblue")
        self.canvas.create_rectangle(190, 250 - jug2_height, 250, 250, fill="skyblue")

        self.canvas.create_text(80, 30, text=f"Jug1: {a}/{jug1_cap}", font=('Arial', 12))
        self.canvas.create_text(220, 30, text=f"Jug2: {b}/{jug2_cap}", font=('Arial', 12))

    def solve(self):
        try:
            jug1 = int(self.jug1_entry.get())
            jug2 = int(self.jug2_entry.get())
            target = int(self.target_entry.get())

            if jug1 > 10 or jug2 > 10:
                messagebox.showerror("Invalid Input", "Max jug capacity allowed is 10.")
                return

        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter valid integers.")
            return

        steps = water_jug_bfs(jug1, jug2, target,
                              condition=self.target_var.get(),
                              require_empty=bool(self.empty_check.get()))

        if not steps:
            messagebox.showinfo("No Solution", "No solution found.")
            return

        self.animate_steps(steps, jug1, jug2)

    def animate_steps(self, steps, jug1_cap, jug2_cap):
        delay = 1000
        for i, (a, b) in enumerate(steps):
            self.root.after(i * delay, lambda a=a, b=b, j1=jug1_cap, j2=jug2_cap: self.draw_jugs(a, b, j1, j2))
        final_msg = "\n".join([f"Step {i+1}: Jug1 = {a}, Jug2 = {b}" for i, (a, b) in enumerate(steps)])
        self.root.after(len(steps) * delay, lambda: self.step_text.set(final_msg))

if __name__ == '__main__':
    root = tk.Tk()
    app = WaterJugGUI(root)
    root.mainloop()
