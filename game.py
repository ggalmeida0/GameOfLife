from automata import CellularAutomaton
import numpy as np
import pygame
import pickle
import resource
import sys

class Game:

    @classmethod
    def start(cls,grid_size):
        cls.GRID_SIZE = grid_size
        cls.WINDOW_SIZE = 1024
        cls.CELL_SIZE = cls.WINDOW_SIZE // cls.GRID_SIZE
        pygame.init()
        cls.screen = pygame.display.set_mode((cls.WINDOW_SIZE,cls.WINDOW_SIZE))
        pygame.display.set_caption("Game of Life")
        cls.grid = np.array([[None] * cls.GRID_SIZE]*cls.GRID_SIZE)
        cls.render_cells()
        cls.lives = []
    
    @classmethod
    def load(cls,filename):
       cls.grid = np.load("saves/"+filename,allow_pickle=True)
       cls.WINDOW_SIZE = 1024
       cls.GRID_SIZE = cls.grid.shape[0]
       cls.CELL_SIZE = cls.WINDOW_SIZE // cls.GRID_SIZE
       pygame.init()
       cls.screen = pygame.display.set_mode((cls.WINDOW_SIZE,cls.WINDOW_SIZE))
       pygame.display.set_caption("Game of Life")
       cls.lives = []
       cls.load_live_cells()
       cls.display_cells()

    @classmethod
    def save(cls):
        name = input("Input file name: ")
        max_rec = 0x100000
        resource.setrlimit(resource.RLIMIT_STACK, [0x100 * max_rec, resource.RLIM_INFINITY])
        sys.setrecursionlimit(max_rec)
        print("Saving...")
        np.save("saves/"+name,cls.grid)
        print("File Saved")

    @classmethod
    def display_cells(cls):
        for col in cls.grid:
            for cell in col:
                if cell.state == 1:
                    pygame.draw.rect(cls.screen,(255,0,0),cell.get_body())
                    pygame.draw.rect(cls.screen,(0,0,0),cell.get_body(),1)
                else:
                    pygame.draw.rect(cls.screen,(255,255,255),cell.get_body())
                    pygame.draw.rect(cls.screen,(0,0,0),cell.get_body(),1)

    @classmethod
    def load_live_cells(cls):
        for i in range(cls.grid.shape[0]):
            for j in range(cls.grid.shape[1]):
                if cls.grid[i,j].state == 1:
                  cls.lives.append(cls.grid[i,j])


    @classmethod
    def render_cells(cls):
        current_position = np.array([0,0])
        for i in range(cls.grid.shape[0]):
            for j in range(cls.grid[i].shape[0]):
                cls.grid[i,j] = CellularAutomaton(cls.screen,tuple(current_position), (cls.CELL_SIZE,cls.CELL_SIZE))
                current_position += [0,cls.CELL_SIZE]
            current_position[1] = 0
            current_position += [cls.CELL_SIZE,0]
        cls.update_neighbors()
        

    
    @classmethod
    def handle_click(cls,coordinates):
        clicked_coord = (coordinates[0] // cls.CELL_SIZE,coordinates[1] //cls.CELL_SIZE)
        if clicked_coord[0] > cls.grid.shape[0] or clicked_coord[1] > cls.grid.shape[0]:
            return
        clicked_cell = cls.grid[clicked_coord[0],clicked_coord[1]]
        if clicked_cell.state == 0:
            pygame.draw.rect(cls.screen,(255,0,0),clicked_cell.get_body())
            pygame.draw.rect(cls.screen,(0,0,0),clicked_cell.get_body(),1)
            clicked_cell.state = 1
            cls.lives.append(clicked_cell)
        elif clicked_cell.state == 1:
            pygame.draw.rect(cls.screen,(255,255,255),clicked_cell.get_body())
            pygame.draw.rect(cls.screen,(0,0,0),clicked_cell.get_body(),1)
            clicked_cell.state = 0
            cls.lives.remove(clicked_cell)

    @classmethod
    def step(cls):
        # First put live cells and its neighbors inside a list for evaluation
        evaluated_cells = cls.lives.copy()
        for i in range(len(cls.lives)):
            for j in range(len(cls.lives[i].get_neighbors())):
                if cls.lives[i].get_neighbors()[j] not in evaluated_cells:
                    evaluated_cells.append(cls.lives[i].get_neighbors()[j])
        for cell in evaluated_cells:
            if cell:
                cell.step()
        for i in range(len(evaluated_cells)):
            if evaluated_cells[i] and evaluated_cells[i].will_live:
                evaluated_cells[i].state = 1
                if evaluated_cells[i] not in cls. lives:
                    cls.lives.append(evaluated_cells[i])
                pygame.draw.rect(cls.screen,(255,0,0),evaluated_cells[i].get_body())
                pygame.draw.rect(cls.screen,(0,0,0),evaluated_cells[i].get_body(),1)
            elif evaluated_cells[i]:
                evaluated_cells[i].state = 0
                if evaluated_cells[i] in cls.lives:
                    cls.lives.remove(evaluated_cells[i])
                pygame.draw.rect(cls.screen,(255,255,255),evaluated_cells[i].get_body())
                pygame.draw.rect(cls.screen,(0,0,0),evaluated_cells[i].get_body(),1)
        

    @classmethod
    def reset_cells(cls):
        for i in range(cls.grid.shape[0]):
            for j in range(cls.grid[i].shape[0]):
                cls.grid[i][j].state = 0
                pygame.draw.rect(cls.screen,(255,255,255),cls.grid[i][j].get_body())
                pygame.draw.rect(cls.screen,(0,0,0),cls.grid[i][j].get_body(),1)

    @classmethod
    def update_neighbors(cls):
        for i in range(cls.grid.shape[0]):
            for j in range(cls.grid[i].shape[0]):
                possible_neighbors =    [(i-1,j-1), (i,j-1), (i+1,j-1),(i-1,j),
                                        (i+1,j), (i-1,j+1),(i,j+1), (i+1,j+1)]
                neighbors = []
                for coordinate in possible_neighbors:
                    if(coordinate[0] < 0 or coordinate[1] < 0 or coordinate[0]
                        >= cls.GRID_SIZE or coordinate[1] >= cls.GRID_SIZE):
                        neighbors.append(None)
                    else:
                        neighbors.append(cls.grid[coordinate[0]][coordinate[1]])
                cls.grid[i][j].set_neighbors(np.array(neighbors))

    # This method will make a gospel glider gun at the coord, it assumes the grid is big enough for it
    @classmethod
    def _make_gospel_gun(cls,initial_coord,fire_right=True):
        x = initial_coord[0]
        y = initial_coord[1]
        x_change = 0
        y_change = 0
        cls.grid[x,y+ y_change].state = 1
        cls.lives.append(cls.grid[x,y+ y_change])
        pygame.draw.rect(cls.screen,(255,0,0),cls.grid[x,y+ y_change].get_body())
        pygame.draw.rect(cls.screen,(0,0,0),cls.grid[x,y+ y_change].get_body(),1)
        cls.lives.append(cls.grid[x + x_change,y + y_change])
        cls.grid[x + x_change,y + y_change].state = 1
        x_change = 1
        y_change = 0
        if not fire_right:
            x_change = -x_change
            y_change = y_change
        pygame.draw.rect(cls.screen,(255,0,0),cls.grid[x + x_change,y+ y_change].get_body())
        pygame.draw.rect(cls.screen,(0,0,0),cls.grid[x + x_change,y+ y_change].get_body(),1)
        cls.lives.append(cls.grid[x + x_change,y+ y_change])
        cls.grid[x + x_change,y+ y_change].state = 1
        x_change = 1
        y_change = 1
        if not fire_right:
            x_change = -x_change
            y_change = y_change
        pygame.draw.rect(cls.screen,(255,0,0),cls.grid[x + x_change,y+ y_change].get_body())
        pygame.draw.rect(cls.screen,(0,0,0),cls.grid[x + x_change,y+ y_change].get_body(),1)
        cls.lives.append(cls.grid[x,y+ y_change])
        cls.grid[x,y+ y_change].state = 1
        x_change = 0
        y_change = 1
        if not fire_right:
            x_change = -x_change
            y_change = y_change
        pygame.draw.rect(cls.screen,(255,0,0),cls.grid[x,y+ y_change].get_body())
        pygame.draw.rect(cls.screen,(0,0,0),cls.grid[x,y+ y_change].get_body(),1)
        cls.lives.append(cls.grid[x + x_change,y+ y_change])
        cls.grid[x + x_change,y+ y_change].state = 1
        x_change = 10
        y_change = 0
        if not fire_right:
            x_change = -x_change
            y_change = y_change
        pygame.draw.rect(cls.screen,(255,0,0),cls.grid[x + x_change,y+ y_change].get_body())
        pygame.draw.rect(cls.screen,(0,0,0),cls.grid[x + x_change,y+ y_change].get_body(),1)
        cls.lives.append(cls.grid[x + x_change,y+ y_change])
        cls.grid[x + x_change,y+ y_change].state = 1
        x_change = 10
        y_change = 1
        if not fire_right:
            x_change = -x_change
            y_change = y_change
        pygame.draw.rect(cls.screen,(255,0,0),cls.grid[x + x_change,y+ y_change].get_body())
        pygame.draw.rect(cls.screen,(0,0,0),cls.grid[x + x_change,y+ y_change].get_body(),1)
        cls.lives.append(cls.grid[x + x_change,y+ y_change])
        cls.grid[x + x_change,y+ y_change].state = 1
        x_change = 10
        y_change = 2
        if not fire_right:
            x_change = -x_change
            y_change = y_change
        pygame.draw.rect(cls.screen,(255,0,0),cls.grid[x + x_change,y+ y_change].get_body())
        pygame.draw.rect(cls.screen,(0,0,0),cls.grid[x + x_change,y+ y_change].get_body(),1)
        cls.lives.append(cls.grid[x + x_change,y+ y_change])
        cls.grid[x + x_change,y+ y_change].state = 1
        x_change = 11
        y_change = -1
        if not fire_right:
            x_change = -x_change
            y_change = y_change
        pygame.draw.rect(cls.screen,(255,0,0),cls.grid[x + x_change,y+ y_change].get_body())
        pygame.draw.rect(cls.screen,(0,0,0),cls.grid[x + x_change,y+ y_change].get_body(),1)
        cls.lives.append(cls.grid[x + x_change,y+ y_change])
        cls.grid[x + x_change,y+ y_change].state = 1
        x_change = 11
        y_change = 3
        if not fire_right:
            x_change = -x_change
            y_change = y_change
        pygame.draw.rect(cls.screen,(255,0,0),cls.grid[x + x_change,y+ y_change].get_body())
        pygame.draw.rect(cls.screen,(0,0,0),cls.grid[x + x_change,y+ y_change].get_body(),1)
        cls.lives.append(cls.grid[x + x_change,y+ y_change])
        cls.grid[x + x_change,y+ y_change].state = 1
        x_change = 12
        y_change = 4
        if not fire_right:
            x_change = -x_change
            y_change = y_change
        pygame.draw.rect(cls.screen,(255,0,0),cls.grid[x + x_change,y+ y_change].get_body())
        pygame.draw.rect(cls.screen,(0,0,0),cls.grid[x + x_change,y+ y_change].get_body(),1)
        cls.lives.append(cls.grid[x + x_change,y+ y_change])
        cls.grid[x + x_change,y+ y_change].state = 1
        x_change = 13
        y_change = 4
        if not fire_right:
            x_change = -x_change
            y_change = y_change
        pygame.draw.rect(cls.screen,(255,0,0),cls.grid[x + x_change,y+ y_change].get_body())
        pygame.draw.rect(cls.screen,(0,0,0),cls.grid[x + x_change,y+ y_change].get_body(),1)
        cls.lives.append(cls.grid[x + x_change,y+ y_change])
        cls.grid[x + x_change,y+ y_change].state = 1
        x_change = 12
        y_change = -2
        if not fire_right:
            x_change = -x_change
            y_change = y_change
        pygame.draw.rect(cls.screen,(255,0,0),cls.grid[x + x_change,y+ y_change].get_body())
        pygame.draw.rect(cls.screen,(0,0,0),cls.grid[x + x_change,y+ y_change].get_body(),1)
        cls.lives.append(cls.grid[x + x_change,y+ y_change])
        cls.grid[x + x_change,y+ y_change].state = 1
        x_change = 13
        y_change = -2
        if not fire_right:
            x_change = -x_change
            y_change = y_change
        pygame.draw.rect(cls.screen,(255,0,0),cls.grid[x + x_change,y+ y_change].get_body())
        pygame.draw.rect(cls.screen,(0,0,0),cls.grid[x + x_change,y+ y_change].get_body(),1)
        cls.lives.append(cls.grid[x + x_change,y+ y_change])
        cls.grid[x + x_change,y+ y_change].state = 1
        x_change = 14
        y_change = 1
        if not fire_right:
            x_change = -x_change
            y_change = y_change
        pygame.draw.rect(cls.screen,(255,0,0),cls.grid[x + x_change,y+ y_change].get_body())
        pygame.draw.rect(cls.screen,(0,0,0),cls.grid[x + x_change,y+ y_change].get_body(),1)
        cls.lives.append(cls.grid[x + x_change,y+ y_change])
        cls.grid[x + x_change,y+ y_change].state = 1
        x_change = 15
        y_change = -1
        if not fire_right:
            x_change = -x_change
            y_change = y_change
        pygame.draw.rect(cls.screen,(255,0,0),cls.grid[x + x_change,y+ y_change].get_body())
        pygame.draw.rect(cls.screen,(0,0,0),cls.grid[x + x_change,y+ y_change].get_body(),1)
        cls.lives.append(cls.grid[x + x_change,y+ y_change])
        cls.grid[x + x_change,y+ y_change].state = 1
        x_change = 15
        y_change = 3
        if not fire_right:
            x_change = -x_change
            y_change = y_change
        pygame.draw.rect(cls.screen,(255,0,0),cls.grid[x + x_change,y+ y_change].get_body())
        pygame.draw.rect(cls.screen,(0,0,0),cls.grid[x + x_change,y+ y_change].get_body(),1)
        cls.lives.append(cls.grid[x + x_change,y+ y_change])
        cls.grid[x + x_change,y+ y_change].state = 1
        x_change = 16
        y_change = 2
        if not fire_right:
            x_change = -x_change
            y_change = y_change
        pygame.draw.rect(cls.screen,(255,0,0),cls.grid[x + x_change,y+ y_change].get_body())
        pygame.draw.rect(cls.screen,(0,0,0),cls.grid[x + x_change,y+ y_change].get_body(),1)
        cls.lives.append(cls.grid[x + x_change,y+ y_change])
        cls.grid[x + x_change,y+ y_change].state = 1
        x_change = 16
        y_change = 1
        if not fire_right:
            x_change = -x_change
            y_change = y_change
        pygame.draw.rect(cls.screen,(255,0,0),cls.grid[x + x_change,y+ y_change].get_body())
        pygame.draw.rect(cls.screen,(0,0,0),cls.grid[x + x_change,y+ y_change].get_body(),1)
        cls.lives.append(cls.grid[x + x_change,y+ y_change])
        cls.grid[x + x_change,y+ y_change].state = 1
        x_change = 16
        y_change = 0
        if not fire_right:
            x_change = -x_change
            y_change = y_change
        pygame.draw.rect(cls.screen,(255,0,0),cls.grid[x + x_change,y+ y_change].get_body())
        pygame.draw.rect(cls.screen,(0,0,0),cls.grid[x + x_change,y+ y_change].get_body(),1)
        cls.lives.append(cls.grid[x + x_change,y+ y_change])
        cls.grid[x + x_change,y+ y_change].state = 1
        x_change = 17
        y_change = 1
        if not fire_right:
            x_change = -x_change
            y_change = y_change
        pygame.draw.rect(cls.screen,(255,0,0),cls.grid[x + x_change,y+ y_change].get_body())
        pygame.draw.rect(cls.screen,(0,0,0),cls.grid[x + x_change,y+ y_change].get_body(),1)
        cls.lives.append(cls.grid[x + x_change,y+ y_change])
        cls.grid[x + x_change,y+ y_change].state = 1
        x_change = 20
        y_change = 0
        if not fire_right:
            x_change = -x_change
            y_change = y_change
        pygame.draw.rect(cls.screen,(255,0,0),cls.grid[x + x_change,y+ y_change].get_body())
        pygame.draw.rect(cls.screen,(0,0,0),cls.grid[x + x_change,y+ y_change].get_body(),1)
        cls.lives.append(cls.grid[x + x_change,y+ y_change])
        cls.grid[x + x_change,y+ y_change].state = 1
        x_change = 20
        y_change = -1
        if not fire_right:
            x_change = -x_change
            y_change = y_change
        pygame.draw.rect(cls.screen,(255,0,0),cls.grid[x + x_change,y+ y_change].get_body())
        pygame.draw.rect(cls.screen,(0,0,0),cls.grid[x + x_change,y+ y_change].get_body(),1)
        cls.lives.append(cls.grid[x + x_change,y+ y_change])
        cls.grid[x + x_change,y+ y_change].state = 1
        x_change = 20
        y_change = -2
        if not fire_right:
            x_change = -x_change
            y_change = y_change
        pygame.draw.rect(cls.screen,(255,0,0),cls.grid[x + x_change,y+ y_change].get_body())
        pygame.draw.rect(cls.screen,(0,0,0),cls.grid[x + x_change,y+ y_change].get_body(),1)
        cls.lives.append(cls.grid[x + x_change,y+ y_change])
        cls.grid[x + x_change,y+ y_change].state = 1
        x_change = 21
        y_change = 0
        if not fire_right:
            x_change = -x_change
            y_change = y_change
        pygame.draw.rect(cls.screen,(255,0,0),cls.grid[x + x_change,y+ y_change].get_body())
        pygame.draw.rect(cls.screen,(0,0,0),cls.grid[x + x_change,y+ y_change].get_body(),1)
        cls.lives.append(cls.grid[x + x_change,y+ y_change])
        cls.grid[x + x_change,y+ y_change].state = 1
        x_change = 21
        y_change = -1
        if not fire_right:
            x_change = -x_change
            y_change = y_change
        pygame.draw.rect(cls.screen,(255,0,0),cls.grid[x + x_change,y+ y_change].get_body())
        pygame.draw.rect(cls.screen,(0,0,0),cls.grid[x + x_change,y+ y_change].get_body(),1)
        cls.lives.append(cls.grid[x + x_change,y+ y_change])
        cls.grid[x + x_change,y+ y_change].state = 1
        x_change = 21
        y_change = -2
        if not fire_right:
            x_change = -x_change
            y_change = y_change
        pygame.draw.rect(cls.screen,(255,0,0),cls.grid[x + x_change,y+ y_change].get_body())
        pygame.draw.rect(cls.screen,(0,0,0),cls.grid[x + x_change,y+ y_change].get_body(),1)
        cls.lives.append(cls.grid[x + x_change,y+ y_change])
        cls.grid[x + x_change,y+ y_change].state = 1
        x_change = 22
        y_change = -3
        if not fire_right:
            x_change = -x_change
            y_change = y_change
        pygame.draw.rect(cls.screen,(255,0,0),cls.grid[x + x_change,y+ y_change].get_body())
        pygame.draw.rect(cls.screen,(0,0,0),cls.grid[x + x_change,y+ y_change].get_body(),1)
        cls.lives.append(cls.grid[x + x_change,y+ y_change])
        cls.grid[x + x_change,y+ y_change].state = 1
        x_change = 22
        y_change = 1
        if not fire_right:
            x_change = -x_change
            y_change = y_change
        pygame.draw.rect(cls.screen,(255,0,0),cls.grid[x + x_change,y+ y_change].get_body())
        pygame.draw.rect(cls.screen,(0,0,0),cls.grid[x + x_change,y+ y_change].get_body(),1)
        cls.lives.append(cls.grid[x + x_change,y+ y_change])
        cls.grid[x + x_change,y+ y_change].state = 1
        x_change = 24
        y_change = 1
        if not fire_right:
            x_change = -x_change
            y_change = y_change
        pygame.draw.rect(cls.screen,(255,0,0),cls.grid[x + x_change,y+ y_change].get_body())
        pygame.draw.rect(cls.screen,(0,0,0),cls.grid[x + x_change,y+ y_change].get_body(),1)
        cls.lives.append(cls.grid[x + x_change,y+ y_change])
        cls.grid[x + x_change,y+ y_change].state = 1
        x_change = 24
        y_change = 2
        if not fire_right:
            x_change = -x_change
            y_change = y_change
        pygame.draw.rect(cls.screen,(255,0,0),cls.grid[x + x_change,y+ y_change].get_body())
        pygame.draw.rect(cls.screen,(0,0,0),cls.grid[x + x_change,y+ y_change].get_body(),1)
        cls.lives.append(cls.grid[x + x_change,y+ y_change])
        cls.grid[x + x_change,y+ y_change].state = 1
        x_change = 24
        y_change = -3
        if not fire_right:
            x_change = -x_change
            y_change = y_change
        pygame.draw.rect(cls.screen,(255,0,0),cls.grid[x + x_change,y+ y_change].get_body())
        pygame.draw.rect(cls.screen,(0,0,0),cls.grid[x + x_change,y+ y_change].get_body(),1)
        cls.lives.append(cls.grid[x + x_change,y+ y_change])
        cls.grid[x + x_change,y+ y_change].state = 1
        x_change = 24
        y_change = -4
        if not fire_right:
            x_change = -x_change
            y_change = y_change
        pygame.draw.rect(cls.screen,(255,0,0),cls.grid[x + x_change,y+ y_change].get_body())
        pygame.draw.rect(cls.screen,(0,0,0),cls.grid[x + x_change,y+ y_change].get_body(),1)
        cls.lives.append(cls.grid[x + x_change,y+ y_change])
        cls.grid[x + x_change,y+ y_change].state = 1
        x_change = 34
        y_change = -2
        if not fire_right:
            x_change = -x_change
            y_change = y_change
        pygame.draw.rect(cls.screen,(255,0,0),cls.grid[x + x_change,y+ y_change].get_body())
        pygame.draw.rect(cls.screen,(0,0,0),cls.grid[x + x_change,y+ y_change].get_body(),1)
        cls.lives.append(cls.grid[x + x_change,y+ y_change])
        cls.grid[x + x_change,y+ y_change].state = 1
        x_change = 34
        y_change = -1
        if not fire_right:
            x_change = -x_change
            y_change = y_change
        pygame.draw.rect(cls.screen,(255,0,0),cls.grid[x + x_change,y+ y_change].get_body())
        pygame.draw.rect(cls.screen,(0,0,0),cls.grid[x + x_change,y+ y_change].get_body(),1)
        cls.lives.append(cls.grid[x + x_change,y+ y_change])
        cls.grid[x + x_change,y+ y_change].state = 1
        x_change = 35
        y_change = -1
        if not fire_right:
            x_change = -x_change
            y_change = y_change
        pygame.draw.rect(cls.screen,(255,0,0),cls.grid[x + x_change,y+ y_change].get_body())
        pygame.draw.rect(cls.screen,(0,0,0),cls.grid[x + x_change,y+ y_change].get_body(),1)
        cls.lives.append(cls.grid[x + x_change,y+ y_change])
        cls.grid[x + x_change,y+ y_change].state = 1
        x_change = 35
        y_change = -2
        if not fire_right:
            x_change = -x_change
            y_change = y_change
        pygame.draw.rect(cls.screen,(255,0,0),cls.grid[x + x_change,y+ y_change].get_body())
        pygame.draw.rect(cls.screen,(0,0,0),cls.grid[x + x_change,y+ y_change].get_body(),1)
        
        


        
    
    # It assumes the grid is at least 128x128
    @classmethod
    def setup_NOT(cls):
        cls._make_gospel_gun((1,30))
        cls._make_gospel_gun((127,28),fire_right=False)
        cls._make_gospel_gun((45,4))
        cls._make_gospel_gun((5,4))



