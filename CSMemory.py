import tkinter as tk
from tkinter import Button, Label
import random

class MemoryGame:
    def __init__(self, root, grid_size=4):
        self.root = root
        self.root.title("Memory Game")
        self.grid_size = grid_size
        self.score = 0
        self.reset_game()

    def reset_game(self, grid_size=None):
        if grid_size:
            self.grid_size = grid_size
        
        # Clear all existing widgets
        for widget in self.root.winfo_children():
            widget.destroy()

        self.score_label = Label(self.root, text=f'Score: {self.score}')
        self.score_label.grid(row=self.grid_size + 1, column=0, columnspan=self.grid_size)
        
        max_num = (self.grid_size * self.grid_size) // 2
        numbers = [str(i) for i in range(1, max_num + 1)]
        numbers *= 2  # Create pairs
        random.shuffle(numbers)  # Shuffle numbers

        self.buttons = [[None for _ in range(self.grid_size)] for _ in range(self.grid_size)]
        self.revealed = [[False for _ in range(self.grid_size)] for _ in range(self.grid_size)]
        self.matched = [[False for _ in range(self.grid_size)] for _ in range(self.grid_size)]
        self.previous_button = None

        for i in range(self.grid_size):
            for j in range(self.grid_size):
                number = numbers.pop()
                btn = Button(self.root, text='', width=5, height=2, command=lambda i=i, j=j, number=number: self.reveal(i, j, number))
                btn.grid(row=i, column=j)
                self.buttons[i][j] = (btn, number)

        reset_button = Button(self.root, text='Reset', command=self.reset_game)
        reset_button.grid(row=self.grid_size, column=0, columnspan=self.grid_size//2)

        difficulty_button = Button(self.root, text='Change Difficulty', command=self.change_difficulty)
        difficulty_button.grid(row=self.grid_size, column=self.grid_size//2, columnspan=self.grid_size//2)

    def change_difficulty(self):
        new_size = {4: 6, 6: 8, 8: 4}.get(self.grid_size, 4)
        self.reset_game(grid_size=new_size)

    def reveal(self, i, j, number):
        btn, original_number = self.buttons[i][j]

        if not self.revealed[i][j] and not self.matched[i][j]:
            btn.config(text=number, bg='light grey')
            self.revealed[i][j] = True

            if self.previous_button:
                prev_i, prev_j = self.previous_button
                if original_number == self.buttons[prev_i][prev_j][1]:
                    print("Match found!")
                    self.matched[i][j] = True
                    self.matched[prev_i][prev_j] = True
                    btn.config(bg='light green')
                    self.buttons[prev_i][prev_j][0].config(bg='light green')
                    self.previous_button = None

                    # Increment and update score
                    self.score += 2
                    self.score_label.config(text=f'Score: {self.score}')
                else:
                    self.root.after(1000, self.hide, i, j, prev_i, prev_j)
                    self.previous_button = None
            else:
                self.previous_button = (i, j)

    def hide(self, i1, j1, i2, j2):
        if not self.matched[i1][j1]:
            self.buttons[i1][j1][0].config(text='', bg='white')
            self.revealed[i1][j1] = False
        if not self.matched[i2][j2]:
            self.buttons[i2][j2][0].config(text='', bg='white')
            self.revealed[i2][j2] = False

if __name__ == "__main__":
    root = tk.Tk()
    game = MemoryGame(root)
    root.mainloop()
