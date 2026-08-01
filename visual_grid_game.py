# IT3012 - Practical 02
# Simple Reflex Agent vs Model-Based Agent

import random
import tkinter as tk


# =========================
# ENVIRONMENT
# =========================

class VisualGridHuntGame:

    def __init__(self, width=12, height=12):

        self.width = width
        self.height = height

        self.agent_pos = [0, 0]

        self.food_positions = {
            (2, 1),
            (5, 3),
            (10, 6),
            (7, 9)
        }

        self.walls = {
            (2, 2),
            (2, 3),
            (2, 4),
            (5, 5),
            (6, 5),
            (7, 5),
            (3, 8)
        }

        self.toxic_traps = {
            (4, 2),
            (8, 8),
            (10, 2)
        }

        self.score = 0
        self.steps = 0

    # =========================
    # PARTIAL OBSERVABILITY
    # =========================
    def get_percept(self):

        x, y = self.agent_pos

        percept = {
            "food_here": (x, y) in self.food_positions,
            "toxin_here": (x, y) in self.toxic_traps,

            "wall_up": (
                y + 1 >= self.height
                or (x, y + 1) in self.walls
            ),

            "wall_down": (
                y - 1 < 0
                or (x, y - 1) in self.walls
            ),

            "wall_left": (
                x - 1 < 0
                or (x - 1, y) in self.walls
            ),

            "wall_right": (
                x + 1 >= self.width
                or (x + 1, y) in self.walls
            )
        }

        return percept

    def execute_action(self, action):

        self.steps += 1

        x, y = self.agent_pos

        new_x = x
        new_y = y

        if action == "Up":
            new_y += 1

        elif action == "Down":
            new_y -= 1

        elif action == "Left":
            new_x -= 1

        elif action == "Right":
            new_x += 1

        if (
            0 <= new_x < self.width
            and 0 <= new_y < self.height
            and (new_x, new_y) not in self.walls
        ):
            self.agent_pos = [new_x, new_y]

        x, y = self.agent_pos
        pos = (x, y)

        if pos in self.food_positions:
            self.food_positions.remove(pos)
            self.score += 20

        if pos in self.toxic_traps:
            self.score -= 15

    def is_done(self):

        return (
            len(self.food_positions) == 0
            or self.steps >= 150
        )


# =========================
# SIMPLE REFLEX AGENT
# =========================

class SimpleReflexAgent:

    def sense_and_act(self, percept):

        # CONDITION-ACTION RULES

        if percept["food_here"]:
            return "Stay"

        if not percept["wall_right"]:
            return "Right"

        if not percept["wall_up"]:
            return "Up"

        if not percept["wall_left"]:
            return "Left"

        return "Down"


# =========================
# MODEL BASED AGENT
# =========================

class ModelBasedAgent:

    def __init__(self):

        self.visited_cells = set()

        self.internal_x = 0
        self.internal_y = 0

        self.last_action = None

    def update_state(self):

        self.visited_cells.add(
            (self.internal_x, self.internal_y)
        )

        if self.last_action == "Up":
            self.internal_y += 1

        elif self.last_action == "Down":
            self.internal_y -= 1

        elif self.last_action == "Left":
            self.internal_x -= 1

        elif self.last_action == "Right":
            self.internal_x += 1

    def sense_and_act(self, percept):

        self.update_state()

        possible_moves = []

        if not percept["wall_right"]:
            possible_moves.append(
                ("Right",
                 (self.internal_x + 1,
                  self.internal_y))
            )

        if not percept["wall_up"]:
            possible_moves.append(
                ("Up",
                 (self.internal_x,
                  self.internal_y + 1))
            )

        if not percept["wall_left"]:
            possible_moves.append(
                ("Left",
                 (self.internal_x - 1,
                  self.internal_y))
            )

        if not percept["wall_down"]:
            possible_moves.append(
                ("Down",
                 (self.internal_x,
                  self.internal_y - 1))
            )

        # Prefer unvisited locations
        for action, future_pos in possible_moves:

            if future_pos not in self.visited_cells:

                self.last_action = action
                return action

        # If all visited, choose random
        if possible_moves:

            action, _ = random.choice(possible_moves)

            self.last_action = action
            return action

        return "Stay"


# =========================
# GUI
# =========================

class GridGameGUI:

    def __init__(self, root, use_model_agent=True):

        self.root = root
        self.root.title("IT3012 Practical 02")

        self.env = VisualGridHuntGame()

        if use_model_agent:
            self.agent = ModelBasedAgent()
            title = "Model-Based Agent"
        else:
            self.agent = SimpleReflexAgent()
            title = "Simple Reflex Agent"

        self.label = tk.Label(
            root,
            text=title,
            font=("Arial", 14)
        )
        self.label.pack()

        self.cell_size = 45

        self.canvas = tk.Canvas(
            root,
            width=self.env.width * self.cell_size,
            height=self.env.height * self.cell_size
        )
        self.canvas.pack()

        self.draw()

        self.run_loop()

    def draw(self):

        self.canvas.delete("all")

        for x in range(self.env.width):
            for y in range(self.env.height):

                x1 = x * self.cell_size
                y1 = (self.env.height - 1 - y) * self.cell_size
                x2 = x1 + self.cell_size
                y2 = y1 + self.cell_size

                color = "white"

                if (x, y) in self.env.walls:
                    color = "gray"

                self.canvas.create_rectangle(
                    x1, y1, x2, y2,
                    fill=color
                )

        for fx, fy in self.env.food_positions:

            self.canvas.create_oval(
                fx * self.cell_size + 10,
                (self.env.height - 1 - fy) * self.cell_size + 10,
                fx * self.cell_size + 35,
                (self.env.height - 1 - fy) * self.cell_size + 35,
                fill="orange"
            )

        for tx, ty in self.env.toxic_traps:

            self.canvas.create_rectangle(
                tx * self.cell_size + 10,
                (self.env.height - 1 - ty) * self.cell_size + 10,
                tx * self.cell_size + 35,
                (self.env.height - 1 - ty) * self.cell_size + 35,
                fill="purple"
            )

        ax, ay = self.env.agent_pos

        self.canvas.create_oval(
            ax * self.cell_size + 5,
            (self.env.height - 1 - ay) * self.cell_size + 5,
            ax * self.cell_size + 40,
            (self.env.height - 1 - ay) * self.cell_size + 40,
            fill="blue"
        )

        self.label.config(
            text=f"Score: {self.env.score} | Steps: {self.env.steps}"
        )

    def run_loop(self):

        def step():

            if not self.env.is_done():

                percept = self.env.get_percept()

                action = self.agent.sense_and_act(percept)

                self.env.execute_action(action)

                self.draw()

                self.root.after(250, step)

            else:

                self.label.config(
                    text=f"Finished! Score = {self.env.score}"
                )

        step()


# =========================
# MAIN
# =========================

if __name__ == "__main__":

    root = tk.Tk()

    # False = Simple Reflex Agent
    # True  = Model-Based Agent

    app = GridGameGUI(
        root,
        use_model_agent=True
    )

    root.mainloop()