import tkinter as tk
from tkinter import messagebox
import numpy as np
import random

# Sudoku board size
N = 9

class SudokuApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sudoku")
        self.board = np.zeros((N, N), dtype=int)
        self.timer_running = False
        self.paused = False
        self.time_elapsed = 0
        self.selected_row, self.selected_col = None, None  # To track selected cell
        # Bind arrow keys for navigation
        self.root.bind("<Up>", self.move_up)
        self.root.bind("<Down>", self.move_down)
        self.root.bind("<Left>", self.move_left)
        self.root.bind("<Right>", self.move_right)
        self.create_widgets()
        self.start_timer()
        self.update_timer()
        self.generate_sudoku()
        


    def create_widgets(self):
        """Create the Sudoku grid with thick lines for 3x3 boxes and thin lines between cells."""
        # Create a canvas to draw the grid

        self.timer_label = tk.Label(self.root, text="Time: 00:00", font=('Arial', 12))
        self.timer_label.grid(row=1, column=0, padx=10, pady=10)

        # Pause Button
        self.pause_button = tk.Button(self.root, text="Pause", command=self.pause_game)
        self.pause_button.grid(row=1, column=1, padx=10)


        self.canvas = tk.Canvas(self.root, width=450, height=450, bg='white')
        self.canvas.grid(row=0, column=0, columnspan=3)


        # Add the grid lines: Thin lines between cells, thick lines for 3x3 boxes
        cell_size = 50
        for i in range(N + 1):
            # Draw thin lines for individual cells
            line_width = 1 if i % 3 != 0 else 3  # Thicker lines for 3x3 boxes
            self.canvas.create_line(i * cell_size, 0, i * cell_size, N * cell_size, width=line_width)
            self.canvas.create_line(0, i * cell_size, N * cell_size, i * cell_size, width=line_width)


        # Bind key presses to the canvas
        self.canvas.bind("<Key>", self.on_key_press)
        self.canvas.focus_set()  # Ensure the canvas is ready to capture key events

                # Create the Resume button but hide it initially
        self.resume_button = tk.Button(self.root, text="Resume", command=self.resume_game)
        self.resume_button.grid(row=2, column=1, padx=10)
        self.resume_button.grid_remove()  # Initially hidden

        # Create a 2D list of Entry widgets
        self.entries = [[None for _ in range(N)] for _ in range(N)]
        for i in range(N):
            for j in range(N):
                x0 = j * cell_size + 5
                y0 = i * cell_size + 5
                entry = tk.Entry(self.root, width=2, font=('Arial', 18), justify='center')
                self.entries[i][j] = entry

                # Create a window for each entry on the canvas
                self.canvas.create_window(x0 + 20, y0 + 20, window=entry, width=40, height=40)

                # Bind validation for each entry
                entry.bind('<FocusOut>', lambda e, x=i, y=j: self.validate_entry(x, y))

        self.solve_button = tk.Button(self.root, text="Solve", command=self.solve_board)
        self.solve_button.grid(row=N, column=0, columnspan=N, pady=10)


    def find_first_open_cell(self):
        """Find the first open (empty) cell to start with."""
        for i in range(9):
            for j in range(9):
                if self.board[i][j] == 0:  # Empty cell
                    self.selected_row, self.selected_col = i, j
                    self.highlight_selected_cell()
                    return



    def redraw_grid(self):
        """Redraw the grid without resetting numbers."""
        # Clear current grid visuals
        self.canvas.delete("highlight")  # Delete only the highlight (not numbers)

        # Draw lines for grid (same as the function that draws the grid lines)
        for i in range(10):
            width = 3 if i % 3 == 0 else 1  # Bold lines for the 3x3 blocks
            self.canvas.create_line(50 * i, 0, 50 * i, 450, fill="black", width=width)
            self.canvas.create_line(0, 50 * i, 450, 50 * i, fill="black", width=width)

        # Highlight selected cell
        if self.selected_row is not None and self.selected_col is not None:
            self.canvas.create_rectangle(self.selected_col * 50, self.selected_row * 50,
                                         (self.selected_col + 1) * 50, (self.selected_row + 1) * 50,
                                         outline="red", width=3, tags="highlight")



    def on_key_press(self, event):
        """Handle key press event to input numbers into the grid."""
        # Check if a number key is pressed (1-9)
        if event.char.isdigit() and 1 <= int(event.char) <= 9:
            # Ensure a cell is selected and not part of the pre-populated grid
            if self.selected_row is not None and self.selected_col is not None:
                # Get the current position of the highlighted cell
                row, col = self.selected_row, self.selected_col

                # Check if the cell is not pre-filled (allow input in empty cells only)
                if self.grid[row][col] == 0:  # Assuming 0 represents an empty cell
                    self.grid[row][col] = int(event.char)  # Set the cell value to the pressed number
                    self.redraw_grid()  # Update the display with the new value




    def highlight_selected_cell(self):
        """Highlight the currently selected cell."""
        # Redraw the board to clear previous highlights
        #self.draw_board()
        self.redraw_grid()

        # Highlight the selected cell (make sure it's within bounds)
        """
        if self.selected_row is not None and self.selected_col is not None:
            self.canvas.create_rectangle(self.selected_col * 50, self.selected_row * 50,
                                         (self.selected_col + 1) * 50, (self.selected_row + 1) * 50,
                                         outline="red", width=3)
        """

    def move_up(self, event):
        """Move the selection up."""
        if self.selected_row is not None:
            next_row = (self.selected_row - 1) % 9  # Loop back to bottom if at the top
            while self.board[next_row][self.selected_col] != 0:
                next_row = (next_row - 1) % 9
            self.selected_row = next_row
            self.highlight_selected_cell()

    def move_down(self, event):
        """Move the selection down."""
        if self.selected_row is not None:
            next_row = (self.selected_row + 1) % 9  # Loop back to top if at the bottom
            while self.board[next_row][self.selected_col] != 0:
                next_row = (next_row + 1) % 9
            self.selected_row = next_row
            self.highlight_selected_cell()

    def move_left(self, event):
        """Move the selection left."""
        if self.selected_col is not None:
            next_col = (self.selected_col - 1) % 9  # Loop back to the rightmost column if at the left
            while self.board[self.selected_row][next_col] != 0:
                next_col = (next_col - 1) % 9
            self.selected_col = next_col
            self.highlight_selected_cell()

    def move_right(self, event):
        """Move the selection right."""
        if self.selected_col is not None:
            next_col = (self.selected_col + 1) % 9  # Loop back to the leftmost column if at the right
            while self.board[self.selected_row][next_col] != 0:
                next_col = (next_col + 1) % 9
            self.selected_col = next_col
            self.highlight_selected_cell()



    def update_timer(self):
        """Update the timer if the game is running."""
        if self.timer_running and not self.paused:
            self.time_elapsed += 1
            minutes = self.time_elapsed // 60
            seconds = self.time_elapsed % 60
            self.timer_label.config(text=f"Time: {minutes:02d}:{seconds:02d}")
        self.root.after(1000, self.update_timer)



    def start_timer(self):
        """Start the game timer."""
        self.timer_running = True


    def pause_game(self):
        """Pause the game, turn the screen gray, and show only the 'Resume' button."""
        # Set the paused flag
        self.paused = True

        # Hide all widgets (canvas, timer, pause button)
        self.canvas.grid_remove()
        self.timer_label.grid_remove()
        self.pause_button.grid_remove()

        # Create a full-screen gray frame for pausing, covering the game window entirely
        self.pause_overlay = tk.Canvas(self.root, bg='gray', width=self.canvas.winfo_width(), height=self.canvas.winfo_height())
        self.pause_overlay.grid(row=0, column=0, columnspan=3)

        # Add the resume button to the gray overlay, centered
        self.resume_button = tk.Button(self.root, text="Resume", bg='white', fg='black', font=('Arial', 14), command=self.resume_game)
        self.resume_button.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

    def resume_game(self):
        """Resume the game, restore all widgets, and remove the gray screen."""
        # Unset the paused flag
        self.paused = False

        # Remove the gray overlay
        self.pause_overlay.grid_remove()

        # Show the game widgets again
        self.canvas.grid(row=0, column=0, columnspan=3)
        self.timer_label.grid(row=1, column=0, padx=10, pady=10)
        self.pause_button.grid(row=1, column=1, padx=10)

        # Hide the resume button
        self.resume_button.place_forget()







    def generate_sudoku(self):
        """Generate and display a Sudoku board."""
        self.board = self.generate_board()
        self.update_grid()

    def generate_board(self):
        """Generate a Sudoku board with a valid solution."""
        board = np.zeros((N, N), dtype=int)
        self.fill_board(board)
        
        # Remove cells for the puzzle
        num_cells_to_remove = random.randint(35, 40)  # Adjust for difficulty
        cells = [(i, j) for i in range(N) for j in range(N)]
        random.shuffle(cells)
        for i in range(num_cells_to_remove):
            row, col = cells[i]
            board[row, col] = 0

        self.find_first_open_cell()
            
        return board

    def fill_board(self, board):
        """Fill the Sudoku board with a valid solution."""
        numbers = list(range(1, 10))
        def fill_box(row_start, col_start):
            """Fill a 3x3 box with random valid numbers."""
            numbers_copy = numbers[:]
            random.shuffle(numbers_copy)
            for i in range(3):
                for j in range(3):
                    num = numbers_copy.pop()
                    while not self.is_valid(board, row_start + i, col_start + j, num):
                        if not numbers_copy:
                            numbers_copy = numbers[:]
                            random.shuffle(numbers_copy)
                        num = numbers_copy.pop()
                    board[row_start + i, col_start + j] = num

        # Fill the diagonal 3x3 boxes
        for i in range(0, N, 3):
            fill_box(i, i)
        
        # Solve the filled board
        self.solve_sudoku(board)

    def update_grid(self):
        """Update the grid with the current board state."""
        for i in range(N):
            for j in range(N):
                value = self.board[i, j]
                self.entries[i][j].delete(0, tk.END)
                if value != 0:
                    self.entries[i][j].insert(0, str(value))
                    self.entries[i][j].config(state='readonly')

    def validate_entry(self, row, col):
        """Validate the entry in the given cell."""
        entry = self.entries[row][col]
        value = entry.get()
        if value.isdigit() and 1 <= int(value) <= 9:
            num = int(value)
            if not self.is_valid(self.board, row, col, num):
                messagebox.showerror("Invalid Move", "This number is not valid in this position!")
                entry.delete(0, tk.END)
        else:
            if value:
                messagebox.showerror("Invalid Entry", "Please enter a number between 1 and 9!")
                entry.delete(0, tk.END)

    def is_valid(self, board, row, col, num):
        """Check if placing num in board[row][col] is valid."""
        if num in board[row]:
            return False
        if num in board[:, col]:
            return False
        start_row, start_col = 3 * (row // 3), 3 * (col // 3)
        if num in board[start_row:start_row + 3, start_col:start_col + 3]:
            return False
        return True

    def solve_board(self):
        """Solve the Sudoku board and update the grid."""
        if self.solve_sudoku(self.board):
            self.update_grid()
            messagebox.showinfo("Sudoku Solver", "The board has been solved!")
        else:
            messagebox.showerror("Solver Error", "The board could not be solved.")

    def solve_sudoku(self, board):
        """Solve the Sudoku board using backtracking."""
        empty = self.find_empty_location(board)
        if not empty:
            return True  # Puzzle solved
        row, col = empty
        for num in range(1, N + 1):
            if self.is_valid(board, row, col, num):
                board[row, col] = num
                if self.solve_sudoku(board):
                    return True
                board[row, col] = 0  # Undo placement
        return False

    def find_empty_location(self, board):
        """Find an empty location on the board."""
        for row in range(N):
            for col in range(N):
                if board[row, col] == 0:
                    return row, col
        return None

if __name__ == "__main__":
    root = tk.Tk()
    app = SudokuApp(root)
    root.mainloop()
