import tkinter
import tkinter.messagebox

import numpy as np

BLACK = 1
WHITE = 2

class BoardGameCanvas(tkinter.Canvas):

    def __init__(self, board, player1, player2): 
        self.board = board 
        self.player1 = player1
        self.player2 = player2
        
        
        self.top = tkinter.Tk()
        self.player1.top = self.top

        self.stone_num = 1
        self._cellsize = 60
        self._width = self._cellsize * board.width + 40
        self._height = self._cellsize * board.height + 40
        tkinter.Canvas.__init__(self, self.top, width=self._width, height=self._height, bg='#F5CBA7')

        self.pack()
        self.draw_grid()
        self.draw_stones()
        self.bind('<ButtonPress-1>', self.user_move)

    def display_result_message(self, message):
        self.create_text(self._width/2, self._height/2,
                                             text=message, font="Roboto 30 italic bold",
                                             fill="blue")
    def user_move(self, event):
        self.delete(self.initial_message)
        x, y = self.canvasx(event.x), self.canvasy(event.y)
        for j in range(len(self._col_grid)-1):
            if self._col_grid[j] < x < self._col_grid[j+1]:
                for i in range(len(self._row_grid)-1):
                    if self._row_grid[i] < y < self._row_grid[i+1]:
                        print(f"Hit {len(self._row_grid) - 2 - i}, {j}")
                        self.player1.location = [len(self._row_grid) - 2 - i,j]
                        self.player1.location_updated = True
                        # self.game.perform_move()

    def draw_one_stone(self, color, row, col):
        stone_color = {BLACK: 'black', WHITE: 'white'}
        text_color = {BLACK: 'yellow', WHITE: 'green'}
        x0 = self._col_grid[col] + self._cellsize*0.1
        y0 = self._row_grid[self.board.height -1 - row] + self._cellsize*0.1
        x1 = self._col_grid[col+1] - self._cellsize*0.1
        y1 = self._row_grid[self.board.height - row] - self._cellsize*0.1
        self.create_oval(x0, y0, x1, y1, fill=stone_color[color])
        # self.create_text((x0+x1)/2., (y0+y1)/2., text=str(self.stone_num), fill=text_color[color])
        # self.stone_num += 1
        if self.board.last_move == row * self.board.width + col:
            self.create_text((x0+x1)/2., (y0+y1)/2., text=str("x"), fill=text_color[color])
        # self.update_idletasks()

    def draw_stones(self):
        for i in range(self.board.height):
            for j in range(self.board.width):
                loc = i * self.board.width + j
                p = self.board.states.get(loc, -1)
                if p == self.player1.player:
                    self.draw_one_stone(BLACK, i, j)
                elif p == self.player2.player:
                    self.draw_one_stone(WHITE, i, j)

    def draw_grid(self):
        left = 20
        right = self._width - 20
        lower = 20
        upper = self._height - 20
        self._row_grid = np.linspace(lower, upper, self.board.height+1)
        self._col_grid = np.linspace(left, right, self.board.width+1)
        for y in self._row_grid:
            self.create_line(left, y, right, y, fill='#5499C7', width=5)
        for x in self._col_grid:
            self.create_line(x, lower, x, upper, fill='#5499C7', width=5)
