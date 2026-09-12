import tkinter as tk
import random
import time

# ========================================
# DIFFILCUTIES
# ========================================

DIFFICULTIES = {
    "CADET": 7,
    "RECRUIT": 11,
    "OFFICER": 15,

    "AGENT": 19,
    "OPERATIVE": 23,
    "SPECIALIST": 27,

    "COMMANDER": 31,
    "SHADOW": 37,
    "PHANTOM": 43
}

# ========================================
# COLOR
# ========================================

BG = "#071412"
GREEN = "#39ff88"
LIGHT_GREEN = "#baffd0"
YELLOW = "#ffe45c"
RED = "#ff6666"
DARK_GREEN = "#123c2b"

# ========================================
# MAIN APPLICATION
# ========================================

class MazeEscape:

    def __init__(self, root):
        self.root = root

        self.root.title("Maze Escape Game")
        self.root.geometry("900x850")
        self.root.configure(bg=BG)

        self.maze = []
        self.player_row = 1
        self.player_col = 1

        self.start_time = None
        self.moves = 0
        self.running = False

        self.showmenu

# ========================================
# MENU SCREEN
# ========================================

def show_menu(self):

    self.running = False

    for widget in self.root.winfo.children():
        widget.destroy()

        title = tk.Label(
            self.root,
            text="Maze\nEscape",
            font=("Consolas", 42, "bold"),
            fg=LIGHT_GREEN
            bg=BG
            justify="center"
        )

        title.pack(pady=(55, 10))

        subtitle = tk.Label(
            self.root,
            text="FIND THE EXIT. ESCAPE THE MAZE!"
            font=("Consolas", 15),
            bg=BG
        )

        subtitle.pack(pady=(55, 10))

        box = tk.Frame(
            self.root
            bg=BG
            highlightbackground=GREEN
            highlightthickness=1
        )

        box.pack(padx=80, fill="both")

        self.create_difficulty_section(
            box,
            "MEDIUM",
            ["CADET", "RECRUIT", "OFFICER"],
            GREEN
        )

        self.create_difficulty_section(
            box,
            "MEDIUM",
            ["AGENT", "OPERATIVE", "SPECIALIST"],
            YELLOW
        )

        self.create_difficulty_section(
            box,
            "MEDIUM",
            ["COMMANDER", "SHADOW", "PHANTOM"],
            RED
        )

        instruction = tk.Label(
            self.root,
            text="WASD/ ARROW KEYS TO NAVIGATE\nrREACH [] TO ESCAPE",
            font=("Consolar", 13),
            fg=GREEN
            bg=BG
            justify="center"
        )

        instruction.pack(pady=30)

# ========================================
# DIFFICULTY BUTTONS
# ========================================

def create_difficulty_section(
        self,
        parent,
        section_name,
        difficulties,
        color
)

    label = tk.Label(
        parent,
        text="---- {section_name} ----",
        font=("Consolas", 14, "bold"),
        fg=color
        bg=BG
    )

    label.pack(pady=(15, 8))

    for difficulty in difficulties:
        size = DIFFICULTIES[difficulty]

        button = tk.Button(
            parent,
            text=f"{difficulty:<12}{size}x{size}",
            font=("Consolas", 13, "bold"),
            fg=color,
            bg=BG
            activeforeground=BG
            activebackground=color,
            relief="flat",
            bd=0,
            highlightbackground=color
            highlightthickness=1,
            width=25,
            command=lambda d=difficulty: self.start_game(d)
        )

        button.pack(pady=5)

# ========================================
# START GAME
# ========================================

def start_game(self, difficulty):

    self.difficulty_name = difficulty
    self.size = DIFFICULTIES[difficulty]

    self.moves = 0
    self.start_time = time.time()
    self.running = True

    self.generate_maze()

    self.show_game()

    self.root.boot("<KeyPress>", self.key_pressed)

    self.update_timer()

# ========================================
# MAZE GENERATOR
# ========================================

def generate_maze(self):

    size = self.size

    # Make everything a wall first
    self.maze = [
        [1 for in range(size)]
        for in range(size)
    ]

    # Start
    self.maze[1][1] = 0

    stack = [(1, 1)]

    directions = [
        (-2, 0)
        (2, 0)
        (0, -2)
        (0, 2)
    ]

    while stack:

        current = stack[-1]

        row, col = current

        random.shuffle(directions)

        found = False

        for dr, dc in directions:

            nr = row + dr
            nc = col + dc

            if (
                nr > 0 and
                nr < size - 1 and
                nc > 0 and
                nc < size - 1 and
                self.maze[nr][nc] == 1
            ):

                # Remove wall between cells
                self.maze[row + dr // 2][col + dc // 2] = 0

                # Open new cell
                self.maze[nr][nc] = 0

                stack.append((nr, nc))

                found = True
                break

            if not found
            stack.pop()

            # Exit
            self.maze[size - 2][size - 2] = 0

            self.player_row = 1
            self.player_col = 1

# ========================================
# GAME SCREEN
# ========================================

def show_game(self):

    for widget in self.root.winfo.children():
        widget()

    # ------------- HEADER -------------
    header = tk.Frame(
        self.root,
        bg=BG
    )

    header.pack(fill="x", padx=30, pady=15)

    self.difficulty_label = tk.Label(
        header,
        text=f"HARD{self.difficulty_name}",
        font=("Consolas", 15, "bold"),
        fg=RED if self.diffilcuty_name in ["COMMANDER", "SHADOW", "PHANTOM"]
        else GREEN,
        bg=BG
    )

    self.difficulty_label.pack(side="left")

        self.time_label = tk.Label(
            header
        )