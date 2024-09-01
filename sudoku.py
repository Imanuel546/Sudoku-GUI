import tkinter as tk
from tkinter import messagebox, simpledialog
import random


class SudokuGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Sudoku Game")
        self.grid_solved = [
            [7, 8, 5, 4, 3, 9, 1, 2, 6],
            [6, 1, 2, 8, 7, 5, 3, 4, 9],
            [4, 9, 3, 6, 2, 1, 5, 7, 8],
            [8, 5, 7, 9, 4, 3, 2, 6, 1],
            [2, 6, 1, 7, 5, 8, 9, 3, 4],
            [9, 3, 4, 1, 6, 2, 7, 8, 5],
            [5, 7, 8, 3, 9, 4, 6, 1, 2],
            [1, 2, 6, 5, 8, 7, 4, 9, 3],
            [3, 4, 9, 2, 1, 6, 8, 5, 7]
        ]
        self.grid = [row[:] for row in self.grid_solved]
        self.cells = [[None for _ in range(9)] for _ in range(9)]
        self.create_widgets()
        self.choose_difficulty()

    def create_widgets(self):
        self.frame = tk.Frame(self.root)
        self.frame.pack()
        for i in range(9):
            for j in range(9):
                cell = tk.Entry(self.frame, width=3, font=("Arial", 18), justify="center", relief="ridge")

                # Set the background color for the cells
                cell.config(bg="#ccffcc")

                # Add thicker borders for separating 3x3 blocks
                if (i % 3 == 0 and i != 0):
                    cell.grid(row=i, column=j, padx=(5, 1), pady=(5, 1))
                elif (j % 3 == 0 and j != 0):
                    cell.grid(row=i, column=j, padx=(5, 1), pady=(1, 1))
                else:
                    cell.grid(row=i, column=j, padx=1, pady=1)

                self.cells[i][j] = cell

        self.solve_button = tk.Button(self.root, text="Solve", command=self.check_and_solve)
        self.solve_button.pack(pady=10)

        self.footer_label = tk.Label(self.root, text="Sudoku made by Imanuel Moiseev", font=("Arial", 12))
        self.footer_label.pack(pady=10)

    def choose_difficulty(self):
        difficulty = simpledialog.askinteger("Difficulty", "Enter difficulty level (1=Easy, 2=Medium, 3=Hard):")
        if difficulty:
            for _ in range(difficulty * 10):
                row, column = random.randint(0, 8), random.randint(0, 8)
                self.grid[row][column] = 0
            self.update_grid()

    def update_grid(self):
        for i in range(9):
            for j in range(9):
                self.cells[i][j].delete(0, tk.END)  # Clear the cell before inserting new value
                if self.grid[i][j] != 0:
                    self.cells[i][j].insert(0, str(self.grid[i][j]))
                    self.cells[i][j].config(state="readonly", disabledbackground="#aaffaa")
                else:
                    self.cells[i][j].config(state="normal")

    def check_and_solve(self):
        if self.validate_grid():
            if self.solve_sudoku():
                self.update_grid()
                messagebox.showinfo("Sudoku", "Puzzle solved!")
            else:
                messagebox.showerror("Sudoku", "This puzzle can't be solved.")
        else:
            messagebox.showerror("Sudoku", "Invalid input detected. Please correct the grid and try again.")

    def validate_grid(self):
        for i in range(9):
            row = []
            col = []
            square = []
            for j in range(9):
                if self.cells[i][j].get():
                    num = int(self.cells[i][j].get())
                    self.grid[i][j] = num
                    if num in row or num < 1 or num > 9:
                        return False
                    row.append(num)
                if self.cells[j][i].get():
                    num = int(self.cells[j][i].get())
                    if num in col:
                        return False
                    col.append(num)

                start_row, start_col = 3 * (i // 3), 3 * (i % 3)
                num = int(self.cells[start_row + j // 3][start_col + j % 3].get()) if self.cells[start_row + j // 3][
                    start_col + j % 3].get() else 0
                if num in square:
                    return False
                if num != 0:
                    square.append(num)
        return True

    def solve_sudoku(self):
        for i in range(9):
            for j in range(9):
                if self.grid[i][j] == 0:
                    for num in range(1, 10):
                        if self.is_safe(i, j, num):
                            self.grid[i][j] = num
                            if self.solve_sudoku():
                                return True
                            self.grid[i][j] = 0
                    return False
        return True

    def is_safe(self, row, col, num):
        for i in range(9):
            if self.grid[row][i] == num or self.grid[i][col] == num:
                return False

        start_row, start_col = 3 * (row // 3), 3 * (col // 3)
        for i in range(3):
            for j in range(3):
                if self.grid[start_row + i][start_col + j] == num:
                    return False
        return True


def main():
    root = tk.Tk()
    game = SudokuGame(root)
    root.mainloop()


if __name__ == "__main__":
    main()
