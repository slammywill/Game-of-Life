import pygame
import math
from config import *

class Board:


    def __init__(self, screen_size, scale = BOARD_SCALE):
        """Initializes the board that the automata will run on.
        """
        self.scale = scale
        self.columns = int(screen_size[0] / scale)
        self.rows = int(screen_size[1] / scale)
        self.state = [[0 for _ in range(self.columns)] for _ in range(self.rows)] 
        self.next_state = [[0 for _ in range(self.columns)] for _ in range(self.rows)]
        
        # The "mask" for determining a cell's neighbours.
        self.neighbours = [[-1, -1], [-1, 0], [-1, 1],
                           [0 , -1],         [0 , 1],
                           [1 , -1], [1 , 0], [1 , 1]]


    def on_draw(self, display_surf):
        """Draws the board and all of the cells, by looping through all of the cells and drawing them based on
        their state.
        
        Args:
            display_surf (Surface) The pygame surface to draw to.
        """
        for row_idx in range(self.rows):
            for col_idx in range(self.columns):
                alive = self.state[row_idx][col_idx]
                rect = [self.scale * row_idx, self.scale * col_idx, self.scale, self.scale]
                pygame.draw.rect(display_surf, color = "white" if alive else "black", rect=rect)
                pygame.draw.rect(display_surf, color = (50, 50, 50, 1), rect=rect, width=1)


    def on_loop(self):
        """Does the logic for determining which cells are alive or not.
        """
        for row_idx in range(self.rows):
            for col_idx in range(self.columns):
                
                # Finds the number of alive neighbours of a cell. This depends on whether the board wraps or not.
                alive_cells = 0
                match BOARD_WRAP:
                    case True:
                        for neighbour in self.neighbours:
                            if self.state[(row_idx + neighbour[0]) % self.rows][(col_idx + neighbour[1]) % self.columns] == 1:
                                alive_cells += 1
                    case False:
                        for neighbour in self.neighbours:
                            if row_idx + neighbour[0] in range(self.rows) and col_idx + neighbour[1] in range(self.columns):
                                if self.state[row_idx + neighbour[0]][col_idx + neighbour[1]] == 1:
                                    alive_cells += 1
                
                # Rules for determining whether a cell in the next state is alive or not.
                if self.state[row_idx][col_idx] == 1:
                    if alive_cells < 2:
                        self.next_state[row_idx][col_idx] = 0
                    elif alive_cells in [2, 3]:
                        self.next_state[row_idx][col_idx] = 1
                    else:
                        self.next_state[row_idx][col_idx] = 0
                else:
                    if alive_cells == 3:
                        self.next_state[row_idx][col_idx] = 1
        
        # Swaps the state for the new state.
        self.state = self.next_state.copy()
        self.next_state = [[0 for _ in range(self.columns)] for _ in range(self.rows)]


    def change_state_on_click(self, mouse_pos):
        """Changes the state of the cell that the user clicks on when the simulation is paused.
        
        Args:
            mouse_pos (Tuple) The x and y co-ordinates of the mouse position.
            """
        x, y = mouse_pos
        row = math.floor(x / self.scale)
        column = math.floor(y / self.scale)
        self.state[row][column] = not self.state[row][column]


