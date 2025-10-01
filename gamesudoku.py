import tkinter as tk
from tkinter import messagebox
import random

BOARD_SIZE = 9
CELL_SIZE = 28
FONT = ("Arial", 12, "bold")
WOOD_BG = "#e7c9a9"
WOOD_CELL = "#c49a6c"
WOOD_CELL_EMPTY = "#e7c9a9"
GRID_COLOR = "#b88a5a"
WHITE_GRID_COLOR = "#ffffff"
FIXED_NUM_COLOR = "#ffffff"  # ตัวเลขโจทย์สีขาว
NEW_NUM_COLOR = "#ffffff"    # ตัวเลขใหม่สีขาว
ERROR_NUM_COLOR = "#ff3333"  # สีแดงสำหรับตัวเลขผิด
SELECT_COLOR = "#f7e3c6"
BTN_COLOR = "#c49a6c"
BTN_TEXT_COLOR = "#ffffff"

SAMPLE_BOARD_FULL = [
    [5, 1, 7, 4, 6, 2, 3, 8, 9],
    [4, 2, 3, 8, 9, 5, 1, 7, 6],
    [6, 8, 9, 1, 7, 3, 4, 2, 5],
    [8, 1, 2, 7, 5, 6, 9, 4, 3],
    [5, 3, 6, 4, 8, 7, 9, 1, 2],
    [7, 9, 4, 9, 3, 2, 5, 6, 8],
    [2, 5, 8, 3, 1, 7, 6, 9, 4],
    [8, 6, 1, 5, 4, 9, 2, 3, 7],
    [3, 4, 5, 2, 6, 8, 7, 5, 1]
]

class SudokuGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Sudoku - Wood Style UI")
        self.selected = None
        self.init_board()
        self.cells = []
        self.create_board()
        self.create_keypad()
        self.create_buttons()

    def init_board(self):
        # สุ่มช่องว่าง 10% (ประมาณ 8 ช่อง)
        self.board = [row[:] for row in SAMPLE_BOARD_FULL]
        empty_count = int(BOARD_SIZE * BOARD_SIZE * 0.1)
        empties = set()
        while len(empties) < empty_count:
            i = random.randint(0, BOARD_SIZE-1)
            j = random.randint(0, BOARD_SIZE-1)
            empties.add((i, j))
        for i, j in empties:
            self.board[i][j] = 0
        self.fixed = [[cell != 0 for cell in row] for row in self.board]

    def create_board(self):
        frame = tk.Frame(self.root, bg=WOOD_BG)
        frame.pack(padx=10, pady=10)
        self.cells = []
        for i in range(BOARD_SIZE):
            row_cells = []
            for j in range(BOARD_SIZE):
                cell_bg = WOOD_CELL if self.board[i][j] != 0 else WOOD_CELL_EMPTY
                cell = tk.Canvas(frame, width=CELL_SIZE, height=CELL_SIZE, bg=cell_bg, highlightthickness=0)
                # Draw rounded rectangle effect
                cell.create_rectangle(4, 4, CELL_SIZE-4, CELL_SIZE-4, outline=GRID_COLOR, width=2, fill=cell_bg)
                # Draw 3x3 grid lines (thicker)
                if i % 3 == 0:
                    cell.create_line(0, 0, CELL_SIZE, 0, width=4, fill=GRID_COLOR)
                if j % 3 == 0:
                    cell.create_line(0, 0, 0, CELL_SIZE, width=4, fill=GRID_COLOR)
                if i == BOARD_SIZE-1:
                    cell.create_line(0, CELL_SIZE, CELL_SIZE, CELL_SIZE, width=4, fill=GRID_COLOR)
                if j == BOARD_SIZE-1:
                    cell.create_line(CELL_SIZE, 0, CELL_SIZE, CELL_SIZE, width=4, fill=GRID_COLOR)
                # เพิ่มเส้นสีขาวแบ่ง 3x3
                if i in [2,5]:
                    cell.create_line(0, CELL_SIZE-2, CELL_SIZE, CELL_SIZE-2, width=3, fill=WHITE_GRID_COLOR)
                if j in [2,5]:
                    cell.create_line(CELL_SIZE-2, 0, CELL_SIZE-2, CELL_SIZE, width=3, fill=WHITE_GRID_COLOR)
                num = self.board[i][j]
                if num != 0:
                    cell.create_text(CELL_SIZE//2, CELL_SIZE//2, text=str(num), font=FONT, fill=FIXED_NUM_COLOR)
                cell.bind('<Button-1>', lambda e, x=i, y=j: self.select_cell(x, y))
                cell.grid(row=i, column=j, padx=2, pady=2)
                row_cells.append(cell)
            self.cells.append(row_cells)
        self.selected = None

    def create_keypad(self):
        self.keypad_frame = tk.Frame(self.root, bg=WOOD_BG)
        self.keypad_frame.pack(pady=5)
        self.keypad_buttons = []
        for i in range(1, 10):
            btn = tk.Button(self.keypad_frame, text=str(i), width=4, height=2, font=FONT,
                            bg='white', fg='#333333', command=lambda n=i: self.input_number(n), relief="flat")
            btn.grid(row=0, column=i-1, padx=4, pady=4)
            self.keypad_buttons.append(btn)
        # ปุ่ม NEW, CHECK, DELETE
        new_btn = tk.Button(self.keypad_frame, text="NEW", font=("Arial", 14, "bold"), width=8, bg=BTN_COLOR, fg=BTN_TEXT_COLOR, command=self.new_game, relief="flat")
        new_btn.grid(row=0, column=9, padx=4, pady=4)
        check_btn = tk.Button(self.keypad_frame, text="CHECK", font=("Arial", 14, "bold"), width=8, bg=BTN_COLOR, fg=BTN_TEXT_COLOR, command=self.check_solution, relief="flat")
        check_btn.grid(row=0, column=10, padx=4, pady=4)
        delete_btn = tk.Button(self.keypad_frame, text="DELETE", font=("Arial", 14, "bold"), width=8, bg=BTN_COLOR, fg=BTN_TEXT_COLOR, command=self.delete_wrong_numbers, relief="flat")
        delete_btn.grid(row=0, column=11, padx=4, pady=4)

    def create_buttons(self):
        pass  # ไม่ต้องสร้างปุ่ม MEMO/DELETE/Check ซ้ำ

    def select_cell(self, i, j):
        if self.fixed[i][j]:
            return
        if self.selected:
            x, y = self.selected
            self.cells[x][y].config(bg=WOOD_CELL_EMPTY)
            self.cells[x][y].delete("highlight")
        self.cells[i][j].config(bg=SELECT_COLOR)
        self.selected = (i, j)

    def input_number(self, n):
        if not self.selected:
            return
        i, j = self.selected
        if self.fixed[i][j]:
            return
        self.board[i][j] = n
        cell = self.cells[i][j]
        cell.delete("all")
        cell_bg = WOOD_CELL
        cell.config(bg=cell_bg)
        cell.create_rectangle(4, 4, CELL_SIZE-4, CELL_SIZE-4, outline=GRID_COLOR, width=2, fill=cell_bg)
        if i % 3 == 0:
            cell.create_line(0, 0, CELL_SIZE, 0, width=4, fill=GRID_COLOR)
        if j % 3 == 0:
            cell.create_line(0, 0, 0, CELL_SIZE, width=4, fill=GRID_COLOR)
        if i == BOARD_SIZE-1:
            cell.create_line(0, CELL_SIZE, CELL_SIZE, CELL_SIZE, width=4, fill=GRID_COLOR)
        if j == BOARD_SIZE-1:
            cell.create_line(CELL_SIZE, 0, CELL_SIZE, CELL_SIZE, width=4, fill=GRID_COLOR)
        # เพิ่มเส้นสีขาวแบ่ง 3x3
        if i in [2,5]:
            cell.create_line(0, CELL_SIZE-2, CELL_SIZE, CELL_SIZE-2, width=3, fill=WHITE_GRID_COLOR)
        if j in [2,5]:
            cell.create_line(CELL_SIZE-2, 0, CELL_SIZE-2, CELL_SIZE, width=3, fill=WHITE_GRID_COLOR)
        cell.create_text(CELL_SIZE//2, CELL_SIZE//2, text=str(n), font=FONT, fill=NEW_NUM_COLOR)

    def delete_number(self):
        if not self.selected:
            return
        i, j = self.selected
        if self.fixed[i][j]:
            return
        self.board[i][j] = 0
        cell = self.cells[i][j]
        cell.delete("all")
        cell_bg = WOOD_CELL_EMPTY
        cell.config(bg=cell_bg)
        cell.create_rectangle(4, 4, CELL_SIZE-4, CELL_SIZE-4, outline=GRID_COLOR, width=2, fill=cell_bg)
        if i % 3 == 0:
            cell.create_line(0, 0, CELL_SIZE, 0, width=4, fill=GRID_COLOR)
        if j % 3 == 0:
            cell.create_line(0, 0, 0, CELL_SIZE, width=4, fill=GRID_COLOR)
        if i == BOARD_SIZE-1:
            cell.create_line(0, CELL_SIZE, CELL_SIZE, CELL_SIZE, width=4, fill=GRID_COLOR)
        if j == BOARD_SIZE-1:
            cell.create_line(CELL_SIZE, 0, CELL_SIZE, CELL_SIZE, width=4, fill=GRID_COLOR)
        # เพิ่มเส้นสีขาวแบ่ง 3x3
        if i in [2,5]:
            cell.create_line(0, CELL_SIZE-2, CELL_SIZE, CELL_SIZE-2, width=3, fill=WHITE_GRID_COLOR)
        if j in [2,5]:
            cell.create_line(CELL_SIZE-2, 0, CELL_SIZE-2, CELL_SIZE, width=3, fill=WHITE_GRID_COLOR)

    def check_solution(self):
        board = self.board
        errors = []
        # ตรวจสอบแต่ละช่อง
        for i in range(BOARD_SIZE):
            for j in range(BOARD_SIZE):
                if not self.fixed[i][j] and self.board[i][j] != 0:
                    if not self.is_cell_valid(i, j, self.board[i][j]):
                        errors.append((i, j))
        # แสดงผลลัพธ์
        for i in range(BOARD_SIZE):
            for j in range(BOARD_SIZE):
                cell = self.cells[i][j]
                cell.delete("all")
                cell_bg = WOOD_CELL if self.board[i][j] != 0 else WOOD_CELL_EMPTY
                cell.config(bg=cell_bg)
                cell.create_rectangle(4, 4, CELL_SIZE-4, CELL_SIZE-4, outline=GRID_COLOR, width=2, fill=cell_bg)
                if i % 3 == 0:
                    cell.create_line(0, 0, CELL_SIZE, 0, width=4, fill=GRID_COLOR)
                if j % 3 == 0:
                    cell.create_line(0, 0, 0, CELL_SIZE, width=4, fill=GRID_COLOR)
                if i == BOARD_SIZE-1:
                    cell.create_line(0, CELL_SIZE, CELL_SIZE, CELL_SIZE, width=4, fill=GRID_COLOR)
                if j == BOARD_SIZE-1:
                    cell.create_line(CELL_SIZE, 0, CELL_SIZE, CELL_SIZE, width=4, fill=GRID_COLOR)
                # เพิ่มเส้นสีขาวแบ่ง 3x3
                if i in [2,5]:
                    cell.create_line(0, CELL_SIZE-2, CELL_SIZE, CELL_SIZE-2, width=3, fill=WHITE_GRID_COLOR)
                if j in [2,5]:
                    cell.create_line(CELL_SIZE-2, 0, CELL_SIZE-2, CELL_SIZE, width=3, fill=WHITE_GRID_COLOR)
                num = self.board[i][j]
                if num != 0:
                    if self.fixed[i][j]:
                        cell.create_text(CELL_SIZE//2, CELL_SIZE//2, text=str(num), font=FONT, fill=FIXED_NUM_COLOR)
                    elif (i, j) in errors:
                        cell.create_text(CELL_SIZE//2, CELL_SIZE//2, text=str(num), font=FONT, fill=ERROR_NUM_COLOR)
                    else:
                        cell.create_text(CELL_SIZE//2, CELL_SIZE//2, text=str(num), font=FONT, fill=NEW_NUM_COLOR)
        if errors:
            messagebox.showerror("ผลลัพธ์", "มีตัวเลขผิด!")
        else:
            messagebox.showinfo("ผลลัพธ์", "คำตอบถูกต้องหรือเป็นไปได้!")

    def is_cell_valid(self, row, col, num):
        # ตรวจสอบแถว
        for j in range(BOARD_SIZE):
            if j != col and self.board[row][j] == num:
                return False
        # ตรวจสอบคอลัมน์
        for i in range(BOARD_SIZE):
            if i != row and self.board[i][col] == num:
                return False
        # ตรวจสอบกล่อง 3x3
        box_row = (row // 3) * 3
        box_col = (col // 3) * 3
        for i in range(box_row, box_row + 3):
            for j in range(box_col, box_col + 3):
                if (i != row or j != col) and self.board[i][j] == num:
                    return False
        return True

    def delete_wrong_numbers(self):
        # ลบตัวเลขที่ผิด
        for i in range(BOARD_SIZE):
            for j in range(BOARD_SIZE):
                if not self.fixed[i][j] and self.board[i][j] != 0:
                    if not self.is_cell_valid(i, j, self.board[i][j]):
                        self.board[i][j] = 0
        # รีเฟรชหน้าจอ
        for i in range(BOARD_SIZE):
            for j in range(BOARD_SIZE):
                cell = self.cells[i][j]
                cell.delete("all")
                cell_bg = WOOD_CELL if self.board[i][j] != 0 else WOOD_CELL_EMPTY
                cell.config(bg=cell_bg)
                cell.create_rectangle(4, 4, CELL_SIZE-4, CELL_SIZE-4, outline=GRID_COLOR, width=2, fill=cell_bg)
                if i % 3 == 0:
                    cell.create_line(0, 0, CELL_SIZE, 0, width=4, fill=GRID_COLOR)
                if j % 3 == 0:
                    cell.create_line(0, 0, 0, CELL_SIZE, width=4, fill=GRID_COLOR)
                if i == BOARD_SIZE-1:
                    cell.create_line(0, CELL_SIZE, CELL_SIZE, CELL_SIZE, width=4, fill=GRID_COLOR)
                if j == BOARD_SIZE-1:
                    cell.create_line(CELL_SIZE, 0, CELL_SIZE, CELL_SIZE, width=4, fill=GRID_COLOR)
                # เพิ่มเส้นสีขาวแบ่ง 3x3
                if i in [2,5]:
                    cell.create_line(0, CELL_SIZE-2, CELL_SIZE, CELL_SIZE-2, width=3, fill=WHITE_GRID_COLOR)
                if j in [2,5]:
                    cell.create_line(CELL_SIZE-2, 0, CELL_SIZE-2, CELL_SIZE, width=3, fill=WHITE_GRID_COLOR)
                num = self.board[i][j]
                if num != 0:
                    if self.fixed[i][j]:
                        cell.create_text(CELL_SIZE//2, CELL_SIZE//2, text=str(num), font=FONT, fill=FIXED_NUM_COLOR)
                    else:
                        cell.create_text(CELL_SIZE//2, CELL_SIZE//2, text=str(num), font=FONT, fill=NEW_NUM_COLOR)

    def new_game(self):
        self.init_board()
        for i in range(BOARD_SIZE):
            for j in range(BOARD_SIZE):
                cell = self.cells[i][j]
                cell.delete("all")
                cell_bg = WOOD_CELL if self.board[i][j] != 0 else WOOD_CELL_EMPTY
                cell.config(bg=cell_bg)
                cell.create_rectangle(4, 4, CELL_SIZE-4, CELL_SIZE-4, outline=GRID_COLOR, width=2, fill=cell_bg)
                if i % 3 == 0:
                    cell.create_line(0, 0, CELL_SIZE, 0, width=4, fill=GRID_COLOR)
                if j % 3 == 0:
                    cell.create_line(0, 0, 0, CELL_SIZE, width=4, fill=GRID_COLOR)
                if i == BOARD_SIZE-1:
                    cell.create_line(0, CELL_SIZE, CELL_SIZE, CELL_SIZE, width=4, fill=GRID_COLOR)
                if j == BOARD_SIZE-1:
                    cell.create_line(CELL_SIZE, 0, CELL_SIZE, CELL_SIZE, width=4, fill=GRID_COLOR)
                num = self.board[i][j]
                if num != 0:
                    cell.create_text(CELL_SIZE//2, CELL_SIZE//2, text=str(num), font=FONT, fill=FIXED_NUM_COLOR)

if __name__ == "__main__":
    root = tk.Tk()
    game = SudokuGame(root)
    root.mainloop()
