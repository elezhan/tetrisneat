# import kivy
# from kivy.app import App
# from kivy.core.window import Window
# from kivy.uix.widget import Widget
# from kivy.clock import Clock

import numpy as np
import random as random
from keypoller import *

tetris_shapes = [
    [[1, 1, 1],
     [0, 1, 0]],
    
    [[0, 1, 1],
     [1, 1, 0]],
    
    [[1, 1, 0],
     [0, 1, 1]],
    
    [[1, 0, 0],
     [1, 1, 1]],
    
    [[0, 0, 1],
     [1, 1, 1]],
    
    [[1, 1, 1, 1]],
    
    [[1, 1],
     [1, 1]]
]
tetris_shapes = np.array(tetris_shapes)

grid_height = 22
grid_width = 10

class GameGrid(object):
    def __init__(self):
        super(GameGrid, self).__init__()
        self.grid = []
        for i in range(grid_height):
            x = [0] * grid_width
            # if i == 21:
            #     x = [1] * grid_width
            self.grid.append(x)
        self.grid = np.array(self.grid)



    def print_grid(self):
        for i in range(len(self.grid)-3,-1,-1):
            string = ""
            for element in self.grid[i]:
                string += str(element) + "  "
            print string

    def check_and_clear_rows(self):
        delete_indices = []
        for row_index in range(len(self.grid)-1,-1,-1):
            row = self.grid[row_index]
            bool_row = row.astype(bool)
            should_delete = np.all(bool_row)
            if should_delete:
                delete_indices.append(row_index)

        for index in delete_indices:
            self.grid = self.grid.tolist()
            del self.grid[index]
            self.grid.append([0] * grid_width)
            self.grid = np.array(self.grid)


    # returns true if dropping the shape does not max out the grid.
    # if this returns false, the game is over.
    def drop_shape(self, shape, col):
        temp_shape = []
        for i in range(len(shape)-1,-1,-1):
            temp_shape.append(shape[i])
        shape = temp_shape
        width = len(shape[0])
        height = len(shape)
        assert width + col <= grid_width
        max_height = 0
        prev_sub_grid = None
        for j in range(len(self.grid)-1,height-2,-1):
            sub_grid = self.grid[j-(height-1):j+1,col:col+width]
            product_array = np.multiply(shape,sub_grid)
            did_collide = np.any(product_array)
            if did_collide:
                break
            prev_sub_grid = sub_grid
        if prev_sub_grid is None:
            return False
        else:
            prev_sub_grid += shape
        self.check_and_clear_rows()
        return True



class GameHandler(object):
    def __init__(self):
        super(GameHandler, self).__init__()
        self.grid = GameGrid()
        self.current_piece = None
        self.get_piece()
        self.reset_val = 4
        self.col = self.reset_val
        self.still_playing = True

    #gets a random piece, TODO change to grab bag
    def get_piece(self):
        index = random.randint(0,len(tetris_shapes)-1)
        self.current_piece = tetris_shapes[index]

    def rotate_current_piece(self):
        shape = self.current_piece
        self.current_piece = [ [ shape[y][x]
                for y in xrange(len(shape)) ]
            for x in xrange(len(shape[0]) - 1, -1, -1) ]
        self.adjust_col_ends()


    def adjust_col_ends(self):
        if self.col < 0:
            self.col = 0
        if self.col + len(self.current_piece[0]) > grid_width:
            self.col = grid_width-len(self.current_piece[0])

    def move_right(self):
        self.col += 1
        self.adjust_col_ends()

    def move_left(self):
        self.col -= 1
        self.adjust_col_ends()

    def drop_piece(self):
        self.still_playing = self.grid.drop_shape(self.current_piece,self.col)
        self.col = self.reset_val
        self.get_piece()
        return self.still_playing

    def print_game(self):
        for row in self.current_piece:
            string = "   " * self.col
            for element in row:
                additional_string = ""
                if element == 0:
                    additional_string = " "
                else:
                    additional_string = str(element)
                string += str(additional_string) + "  "
            print string
        self.grid.print_grid()

game = GameHandler()
game.print_game()

with KeyPoller() as keyPoller:
    while True:
        c = keyPoller.poll()
        if not c is None:
            keep_playing = True
            if c == "w":
                game.rotate_current_piece()
                game.print_game()
            if c == "a":
                game.move_left()
                game.print_game()
            if c == "d":
                game.move_right()
                game.print_game()
            if c == " ":
                keep_playing = game.drop_piece()
                game.print_game()
            if c == "c":
                keep_playing = False
            if not keep_playing:
                break





            # height_top_one = -1
            # for j in range(grid_height-1,-1,-1):
            #     if self.grid == 1:
            #         height_top_one = j
            #         break


# grid = GameGrid()
# grid.print_grid()
# grid.drop_shape(tetris_shapes[0],2)
# grid.print_grid()
