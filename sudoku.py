import numpy as np
import random
import time

# Sudoku board size
N = 9

def print_board(board):
    """Print the Sudoku board in a readable format."""
    for i in range(N):
        if i % 3 == 0 and i != 0:
            print("-" * 21)
        for j in range(N):
            if j % 3 == 0 and j != 0:
                print("| ", end="")
            print(board[i, j] if board[i, j] != 0 else "_", end=" ")
        print()

def is_valid(board, row, col, num):
    """Check if placing num in board[row][col] is valid."""
    if num in board[row]:
        return False
    if num in board[:, col]:
        return False
    start_row, start_col = 3 * (row // 3), 3 * (col // 3)
    if num in board[start_row:start_row + 3, start_col:start_col + 3]:
        return False
    return True

def find_empty_location(board):
    """Find an empty location on the board."""
    for row in range(N):
        for col in range(N):
            if board[row, col] == 0:
                return row, col
    return None

def solve_sudoku(board):
    """Solve the Sudoku board using backtracking."""
    empty = find_empty_location(board)
    if not empty:
        return True  # Puzzle solved
    row, col = empty
    for num in range(1, N + 1):
        if is_valid(board, row, col, num):
            board[row, col] = num
            if solve_sudoku(board):
                return True
            board[row, col] = 0  # Undo placement
    return False

def fill_board(board):
    """Fill the Sudoku board with a valid solution."""
    numbers = list(range(1, 10))
    def fill_box(row_start, col_start):
        """Fill a 3x3 box with random valid numbers."""
        numbers_copy = numbers[:]
        random.shuffle(numbers_copy)
        for i in range(3):
            for j in range(3):
                num = numbers_copy.pop()
                while not is_valid(board, row_start + i, col_start + j, num):
                    if not numbers_copy:
                        numbers_copy = numbers[:]
                        random.shuffle(numbers_copy)
                    num = numbers_copy.pop()
                board[row_start + i, col_start + j] = num

    # Fill the diagonal 3x3 boxes
    for i in range(0, N, 3):
        fill_box(i, i)
    
    # Solve the filled board
    solve_sudoku(board)

def generate_sudoku(difficulty='easy'):
    """Generate a Sudoku board with the specified difficulty and then remove cells."""
    board = np.zeros((N, N), dtype=int)
    fill_board(board)
    
    # Difficulty levels
    if difficulty == 'easy':
        num_cells_to_remove = random.randint(35, 40)
    elif difficulty == 'medium':
        num_cells_to_remove = random.randint(45, 50)
    elif difficulty == 'hard':
        num_cells_to_remove = random.randint(55, 60)
    else:
        raise ValueError("Difficulty must be 'easy', 'medium', or 'hard'.")
    
    cells = [(i, j) for i in range(N) for j in range(N)]
    random.shuffle(cells)
    for i in range(num_cells_to_remove):
        row, col = cells[i]
        board[row, col] = 0
        
    return board

if __name__ == "__main__":
    # User input for difficulty
    difficulty = input("Enter difficulty level ('easy', 'medium', 'hard'): ").strip().lower()
    
    # Generate and print a Sudoku board
    sudoku_board = generate_sudoku(difficulty)
    print("\nGenerated Sudoku Board:")
    print_board(sudoku_board)
    
    # Measure time to solve the Sudoku board
    start_time = time.time()
    solved_board = sudoku_board.copy()
    solve_sudoku(solved_board)
    end_time = time.time()
    
    print("\nSolved Sudoku Board:")
    print_board(solved_board)
    
    print(f"\nTime taken to solve: {end_time - start_time:.2f} seconds")


