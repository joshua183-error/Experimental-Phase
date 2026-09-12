import tkinter as tk
import random
import time


# ============================================================
# DIFFICULTIES
# ============================================================

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


# ============================================================
# COLORS
# ============================================================

BG = "#071412"
GREEN = "#39ff88"
LIGHT_GREEN = "#baffd0"
YELLOW = "#ffe45c"
RED = "#ff6666"
DARK_GREEN = "#123c2b"


# ============================================================
# MAIN APPLICATION
# ============================================================

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

        self.show_menu()

    # ========================================================
    # MENU SCREEN
    # ========================================================

    def show_menu(self):

        self.running = False

        for widget in self.root.winfo_children():
            widget.destroy()

        title = tk.Label(
            self.root,
            text="MAZE\nESCAPE",
            font=("Consolas", 42, "bold"),
            fg=LIGHT_GREEN,
            bg=BG,
            justify="center"
        )
        title.pack(pady=(55, 10))

        subtitle = tk.Label(
            self.root,
            text="FIND THE EXIT. ESCAPE THE GRID.",
            font=("Consolas", 15),
            fg=GREEN,
            bg=BG
        )
        subtitle.pack(pady=(0, 35))

        box = tk.Frame(
            self.root,
            bg=BG,
            highlightbackground=GREEN,
            highlightthickness=1
        )
        box.pack(padx=80, fill="both")

        self.create_difficulty_section(
            box,
            "EASY",
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
            "HARD",
            ["COMMANDER", "SHADOW", "PHANTOM"],
            RED
        )

        instructions = tk.Label(
            self.root,
            text="WASD / ARROW KEYS TO NAVIGATE\nREACH [■] TO ESCAPE",
            font=("Consolas", 13),
            fg=GREEN,
            bg=BG,
            justify="center"
        )
        instructions.pack(pady=30)

    # ========================================================
    # DIFFICULTY BUTTONS
    # ========================================================

    def create_difficulty_section(
        self,
        parent,
        section_name,
        difficulties,
        color
    ):

        label = tk.Label(
            parent,
            text=f"── {section_name} ──",
            font=("Consolas", 14, "bold"),
            fg=color,
            bg=BG
        )
        label.pack(pady=(15, 8))

        for difficulty in difficulties:

            size = DIFFICULTIES[difficulty]

            button = tk.Button(
                parent,
                text=f"{difficulty:<12} {size}×{size}",
                font=("Consolas", 13, "bold"),
                fg=color,
                bg=BG,
                activeforeground=BG,
                activebackground=color,
                relief="flat",
                bd=0,
                highlightbackground=color,
                highlightthickness=1,
                width=25,
                command=lambda d=difficulty: self.start_game(d)
            )

            button.pack(pady=5)

    # ========================================================
    # START GAME
    # ========================================================

    def start_game(self, difficulty):

        self.difficulty_name = difficulty
        self.size = DIFFICULTIES[difficulty]

        self.moves = 0
        self.start_time = time.time()
        self.running = True

        self.generate_maze()

        self.show_game()

        self.root.bind("<KeyPress>", self.key_pressed)

        self.update_timer()

    # ========================================================
    # MAZE GENERATOR
    # ========================================================

    def generate_maze(self):

        size = self.size

        # Make everything a wall first
        self.maze = [
            [1 for _ in range(size)]
            for _ in range(size)
        ]

        # Start
        self.maze[1][1] = 0

        stack = [(1, 1)]

        directions = [
            (-2, 0),
            (2, 0),
            (0, -2),
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

            if not found:
                stack.pop()

        # Exit
        self.maze[size - 2][size - 2] = 0

        self.player_row = 1
        self.player_col = 1

    # ========================================================
    # GAME SCREEN
    # ========================================================

    def show_game(self):

        for widget in self.root.winfo_children():
            widget.destroy()

        # ---------------- HEADER ----------------

        header = tk.Frame(
            self.root,
            bg=BG
        )
        header.pack(fill="x", padx=30, pady=15)

        self.difficulty_label = tk.Label(
            header,
            text=f"HARD  •  {self.difficulty_name}",
            font=("Consolas", 15, "bold"),
            fg=RED if self.difficulty_name in
            ["COMMANDER", "SHADOW", "PHANTOM"]
            else GREEN,
            bg=BG
        )
        self.difficulty_label.pack(side="left")

        self.time_label = tk.Label(
            header,
            text="TIME 00:00",
            font=("Consolas", 14, "bold"),
            fg=GREEN,
            bg=BG
        )
        self.time_label.pack(side="left", padx=40)

        self.moves_label = tk.Label(
            header,
            text="MOVES 0",
            font=("Consolas", 14, "bold"),
            fg=GREEN,
            bg=BG
        )
        self.moves_label.pack(side="left")

        abort_button = tk.Button(
            header,
            text="×  ABORT",
            font=("Consolas", 12, "bold"),
            fg=GREEN,
            bg=BG,
            activeforeground=BG,
            activebackground=GREEN,
            relief="flat",
            highlightbackground=GREEN,
            highlightthickness=1,
            command=self.show_menu
        )
        abort_button.pack(side="right")

        # ---------------- MAZE ----------------

        self.canvas = tk.Canvas(
            self.root,
            bg=BG,
            highlightthickness=1,
            highlightbackground=GREEN
        )

        self.canvas.pack(
            padx=40,
            pady=5
        )

        self.draw_maze()

        # ---------------- CONTROLS ----------------

        controls = tk.Frame(
            self.root,
            bg=BG
        )
        controls.pack(pady=15)

        up = tk.Button(
            controls,
            text="▲",
            font=("Consolas", 15, "bold"),
            fg=GREEN,
            bg=BG,
            width=4,
            command=lambda: self.move(-1, 0)
        )
        up.grid(row=0, column=1, padx=3, pady=3)

        left = tk.Button(
            controls,
            text="◀",
            font=("Consolas", 15, "bold"),
            fg=GREEN,
            bg=BG,
            width=4,
            command=lambda: self.move(0, -1)
        )
        left.grid(row=1, column=0, padx=3)

        down = tk.Button(
            controls,
            text="▼",
            font=("Consolas", 15, "bold"),
            fg=GREEN,
            bg=BG,
            width=4,
            command=lambda: self.move(1, 0)
        )
        down.grid(row=1, column=1, padx=3)

        right = tk.Button(
            controls,
            text="▶",
            font=("Consolas", 15, "bold"),
            fg=GREEN,
            bg=BG,
            width=4,
            command=lambda: self.move(0, 1)
        )
        right.grid(row=1, column=2, padx=3)

    # ========================================================
    # DRAW MAZE
    # ========================================================

    def draw_maze(self):

        self.canvas.delete("all")

        size = self.size

        # Adjust cell size depending on maze
        cell_size = max(10, 600 // size)

        canvas_size = cell_size * size

        self.canvas.config(
            width=canvas_size,
            height=canvas_size
        )

        for row in range(size):

            for col in range(size):

                x1 = col * cell_size
                y1 = row * cell_size

                x2 = x1 + cell_size
                y2 = y1 + cell_size

                if self.maze[row][col] == 1:

                    self.canvas.create_rectangle(
                        x1,
                        y1,
                        x2,
                        y2,
                        fill=DARK_GREEN,
                        outline=GREEN
                    )

        # ---------------- START ----------------

        self.canvas.create_oval(
            self.player_col * cell_size + 2,
            self.player_row * cell_size + 2,
            (self.player_col + 1) * cell_size - 2,
            (self.player_row + 1) * cell_size - 2,
            fill=LIGHT_GREEN,
            outline=""
        )

        # ---------------- EXIT ----------------

        exit_row = size - 2
        exit_col = size - 2

        self.canvas.create_rectangle(
            exit_col * cell_size + 2,
            exit_row * cell_size + 2,
            (exit_col + 1) * cell_size - 2,
            (exit_row + 1) * cell_size - 2,
            outline=GREEN,
            width=2
        )

        self.canvas.create_text(
            exit_col * cell_size + cell_size / 2,
            exit_row * cell_size + cell_size / 2,
            text="■",
            fill=GREEN,
            font=("Consolas", max(8, cell_size // 2))
        )

    # ========================================================
    # PLAYER MOVEMENT
    # ========================================================

    def move(self, dr, dc):

        if not self.running:
            return

        new_row = self.player_row + dr
        new_col = self.player_col + dc

        # Check boundaries
        if (
            new_row < 0 or
            new_row >= self.size or
            new_col < 0 or
            new_col >= self.size
        ):
            return

        # Check wall
        if self.maze[new_row][new_col] == 1:
            return

        self.player_row = new_row
        self.player_col = new_col

        self.moves += 1

        self.moves_label.config(
            text=f"MOVES {self.moves}"
        )

        self.draw_maze()

        # Check exit
        if (
            self.player_row == self.size - 2 and
            self.player_col == self.size - 2
        ):
            self.win_game()

    # ========================================================
    # KEYBOARD CONTROLS
    # ========================================================

    def key_pressed(self, event):

        key = event.keysym.lower()

        if key in ["w", "up"]:
            self.move(-1, 0)

        elif key in ["s", "down"]:
            self.move(1, 0)

        elif key in ["a", "left"]:
            self.move(0, -1)

        elif key in ["d", "right"]:
            self.move(0, 1)

    # ========================================================
    # TIMER
    # ========================================================

    def update_timer(self):

        if not self.running:
            return

        elapsed = int(time.time() - self.start_time)

        minutes = elapsed // 60
        seconds = elapsed % 60

        self.time_label.config(
            text=f"TIME {minutes:02d}:{seconds:02d}"
        )

        self.root.after(
            1000,
            self.update_timer
        )

    # ========================================================
    # WIN
    # ========================================================

    def win_game(self):

        self.running = False

        elapsed = int(time.time() - self.start_time)

        minutes = elapsed // 60
        seconds = elapsed % 60

        for widget in self.root.winfo_children():
            widget.destroy()

        tk.Label(
            self.root,
            text="ESCAPED!",
            font=("Consolas", 45, "bold"),
            fg=GREEN,
            bg=BG
        ).pack(pady=(150, 20))

        tk.Label(
            self.root,
            text=f"TIME  {minutes:02d}:{seconds:02d}\n"
                 f"MOVES {self.moves}",
            font=("Consolas", 18),
            fg=LIGHT_GREEN,
            bg=BG,
            justify="center"
        ).pack(pady=20)

        tk.Button(
            self.root,
            text="PLAY AGAIN",
            font=("Consolas", 14, "bold"),
            fg=GREEN,
            bg=BG,
            activebackground=GREEN,
            activeforeground=BG,
            relief="flat",
            highlightbackground=GREEN,
            highlightthickness=1,
            command=self.show_menu
        ).pack(pady=30)


# ============================================================
# RUN PROGRAM
# ============================================================

if __name__ == "__main__":

    root = tk.Tk()

    game = MazeEscape(root)

    root.mainloop()
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
