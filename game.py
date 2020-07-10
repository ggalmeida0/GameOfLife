from automata import CellularAutomaton
import numpy as np
import pygame
from copy import copy, deepcopy


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
        elif clicked_cell.state == 1:
            pygame.draw.rect(cls.screen,(255,255,255),clicked_cell.get_body())
            pygame.draw.rect(cls.screen,(0,0,0),clicked_cell.get_body(),1)
            clicked_cell.state = 0

    @classmethod
    def step(cls):
        old_configuration = cls.copy_configuration()
        for i in range(old_configuration.shape[0]):
            for j in range(old_configuration[i].shape[0]):
                alive_neighbors = 0
                current_cell = cls.grid[i][j]
                for neighbor in old_configuration[i][j].get_neighbors():
                    if neighbor and neighbor.state == 1:
                        alive_neighbors += 1
                # Rules:
                # 1. If the cell is alive and there are 2 or 3 alive neighbors it lives to the next generation
                if(current_cell.state == 1 and (alive_neighbors == 2 or alive_neighbors == 3)):
                    continue
                #2. If a dead cell has exactly 3 alive neighbors it will become a live cell as if by reproduction
                elif (current_cell.state == 0 and alive_neighbors == 3):    
                    current_cell.state = 1
                    pygame.draw.rect(cls.screen,(255,0,0),current_cell.get_body())
                    pygame.draw.rect(cls.screen,(0,0,0),current_cell.get_body(),1)
                # 3. Any live cell with fewer than two live neighbours dies, as if by underpopulation
                elif(current_cell.state == 1 and alive_neighbors < 2):
                    current_cell.state = 0
                    pygame.draw.rect(cls.screen,(255,255,255),current_cell.get_body())
                    pygame.draw.rect(cls.screen,(0,0,0),current_cell.get_body(),1)
                # 4. Any live cell with more than three live neighbours dies, as if by overpopulation.
                elif(current_cell.state == 1 and alive_neighbors > 3):
                    current_cell.state = 0
                    pygame.draw.rect(cls.screen,(255,255,255),current_cell.get_body())
                    pygame.draw.rect(cls.screen,(0,0,0),current_cell.get_body(),1)
        cls.update_neighbors()
                
 
    @classmethod
    def reset_cells(cls):
        for i in range(cls.grid.shape[0]):
            for j in range(cls.grid[i].shape[0]):
                cls.grid[i][j].state = 0
                pygame.draw.rect(cls.screen,(255,255,255),cls.grid[i][j].get_body())
                pygame.draw.rect(cls.screen,(0,0,0),cls.grid[i][j].get_body(),1)

    @classmethod
    def copy_configuration(cls):
        config_copy = np.copy(cls.grid)
        for i in range(config_copy.shape[0]):
            for j in range(config_copy[i].shape[0]):
                config_copy[i][j] = copy(config_copy[i][j])
                for n in range(len(config_copy[i][j].get_neighbors())):
                    config_copy[i][j].get_neighbors()[n] = copy(config_copy[i][j].get_neighbors()[n])
        return config_copy

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

    @classmethod
    def make_gospel_gun(cls,initial_coord):
        x = initial_coord[0]
        y = initial_coord[1]
        cls.grid[x,y].state = 1
        pygame.draw.rect(cls.screen,(255,0,0),cls.grid[x,y].get_body())
        pygame.draw.rect(cls.screen,(0,0,0),cls.grid[x,y].get_body(),1)
        cls.grid[x+1,y].state = 1
        pygame.draw.rect(cls.screen,(255,0,0),cls.grid[x+1,y].get_body())
        pygame.draw.rect(cls.screen,(0,0,0),cls.grid[x+1,y].get_body(),1)
        cls.grid[x+1,y+1].state = 1
        pygame.draw.rect(cls.screen,(255,0,0),cls.grid[x+1,y+1].get_body())
        pygame.draw.rect(cls.screen,(0,0,0),cls.grid[x+1,y+1].get_body(),1)
        cls.grid[x,y+1].state = 1
        pygame.draw.rect(cls.screen,(255,0,0),cls.grid[x,y+1].get_body())
        pygame.draw.rect(cls.screen,(0,0,0),cls.grid[x,y+1].get_body(),1)
        cls.grid[x+10,y].state = 1
        pygame.draw.rect(cls.screen,(255,0,0),cls.grid[x+10,y].get_body())
        pygame.draw.rect(cls.screen,(0,0,0),cls.grid[x+10,y].get_body(),1)
        cls.grid[x+10,y+1].state = 1
        pygame.draw.rect(cls.screen,(255,0,0),cls.grid[x+10,y+1].get_body())
        pygame.draw.rect(cls.screen,(0,0,0),cls.grid[x+10,y+1].get_body(),1)
        cls.grid[x+10,y+2].state = 1
        pygame.draw.rect(cls.screen,(255,0,0),cls.grid[x+10,y+2].get_body())
        pygame.draw.rect(cls.screen,(0,0,0),cls.grid[x+10,y+2].get_body(),1)
        cls.grid[x+11,y-1].state = 1
        pygame.draw.rect(cls.screen,(255,0,0),cls.grid[x+11,y-1].get_body())
        pygame.draw.rect(cls.screen,(0,0,0),cls.grid[x+11,y-1].get_body(),1)
        cls.grid[x+11,y+3].state = 1
        pygame.draw.rect(cls.screen,(255,0,0),cls.grid[x+11,y+3].get_body())
        pygame.draw.rect(cls.screen,(0,0,0),cls.grid[x+11,y+3].get_body(),1)
        cls.grid[x+12,y+4].state = 1
        pygame.draw.rect(cls.screen,(255,0,0),cls.grid[x+12,y+4].get_body())
        pygame.draw.rect(cls.screen,(0,0,0),cls.grid[x+12,y+4].get_body(),1)
        cls.grid[x+13,y+4].state = 1
        pygame.draw.rect(cls.screen,(255,0,0),cls.grid[x+13,y+4].get_body())
        pygame.draw.rect(cls.screen,(0,0,0),cls.grid[x+13,y+4].get_body(),1)

        cls.grid[x+12,y-2].state = 1
        pygame.draw.rect(cls.screen,(255,0,0),cls.grid[x+12,y-2].get_body())
        pygame.draw.rect(cls.screen,(0,0,0),cls.grid[x+12,y-2].get_body(),1)
        cls.grid[x+13,y-2].state = 1
        pygame.draw.rect(cls.screen,(255,0,0),cls.grid[x+13,y-2].get_body())
        pygame.draw.rect(cls.screen,(0,0,0),cls.grid[x+13,y-2].get_body(),1)

        cls.grid[x+14,y+1].state = 1
        pygame.draw.rect(cls.screen,(255,0,0),cls.grid[x+14,y+1].get_body())
        pygame.draw.rect(cls.screen,(0,0,0),cls.grid[x+14,y+1].get_body(),1)
        cls.grid[x+15,y-1].state = 1
        pygame.draw.rect(cls.screen,(255,0,0),cls.grid[x+15,y-1].get_body())
        pygame.draw.rect(cls.screen,(0,0,0),cls.grid[x+15,y-1].get_body(),1)
        cls.grid[x+15,y+3].state = 1
        pygame.draw.rect(cls.screen,(255,0,0),cls.grid[x+15,y+3].get_body())
        pygame.draw.rect(cls.screen,(0,0,0),cls.grid[x+15,y+3].get_body(),1)
        cls.grid[x+16,y+2].state = 1
        pygame.draw.rect(cls.screen,(255,0,0),cls.grid[x+16,y+2].get_body())
        pygame.draw.rect(cls.screen,(0,0,0),cls.grid[x+16,y+2].get_body(),1)
        cls.grid[x+16,y+1].state = 1
        pygame.draw.rect(cls.screen,(255,0,0),cls.grid[x+16,y+1].get_body())
        pygame.draw.rect(cls.screen,(0,0,0),cls.grid[x+16,y+1].get_body(),1)
        cls.grid[x+16,y].state = 1
        pygame.draw.rect(cls.screen,(255,0,0),cls.grid[x+16,y].get_body())
        pygame.draw.rect(cls.screen,(0,0,0),cls.grid[x+16,y].get_body(),1)
        cls.grid[x+17,y+1].state = 1
        pygame.draw.rect(cls.screen,(255,0,0),cls.grid[x+17,y+1].get_body())
        pygame.draw.rect(cls.screen,(0,0,0),cls.grid[x+17,y+1].get_body(),1)
        cls.grid[x+20,y].state = 1
        pygame.draw.rect(cls.screen,(255,0,0),cls.grid[x+20,y].get_body())
        pygame.draw.rect(cls.screen,(0,0,0),cls.grid[x+20,y].get_body(),1)
        cls.grid[x+20,y-1].state = 1
        pygame.draw.rect(cls.screen,(255,0,0),cls.grid[x+20,y-1].get_body())
        pygame.draw.rect(cls.screen,(0,0,0),cls.grid[x+20,y-1].get_body(),1)
        cls.grid[x+20,y-2].state = 1
        pygame.draw.rect(cls.screen,(255,0,0),cls.grid[x+20,y-2].get_body())
        pygame.draw.rect(cls.screen,(0,0,0),cls.grid[x+20,y-2].get_body(),1)
        cls.grid[x+21,y].state = 1
        pygame.draw.rect(cls.screen,(255,0,0),cls.grid[x+21,y].get_body())
        pygame.draw.rect(cls.screen,(0,0,0),cls.grid[x+21,y].get_body(),1)
        cls.grid[x+21,y-1].state = 1
        pygame.draw.rect(cls.screen,(255,0,0),cls.grid[x+21,y-1].get_body())
        pygame.draw.rect(cls.screen,(0,0,0),cls.grid[x+21,y-1].get_body(),1)
        cls.grid[x+21,y-2].state = 1
        pygame.draw.rect(cls.screen,(255,0,0),cls.grid[x+21,y-2].get_body())
        pygame.draw.rect(cls.screen,(0,0,0),cls.grid[x+21,y-2].get_body(),1)
        cls.grid[x+22,y-3].state = 1
        pygame.draw.rect(cls.screen,(255,0,0),cls.grid[x+22,y-3].get_body())
        pygame.draw.rect(cls.screen,(0,0,0),cls.grid[x+22,y-3].get_body(),1)
        cls.grid[x+22,y+1].state = 1
        pygame.draw.rect(cls.screen,(255,0,0),cls.grid[x+22,y+1].get_body())
        pygame.draw.rect(cls.screen,(0,0,0),cls.grid[x+22,y+1].get_body(),1)
        cls.grid[x+24,y+1].state = 1
        pygame.draw.rect(cls.screen,(255,0,0),cls.grid[x+24,y+1].get_body())
        pygame.draw.rect(cls.screen,(0,0,0),cls.grid[x+24,y+1].get_body(),1)
        cls.grid[x+24,y+2].state = 1
        pygame.draw.rect(cls.screen,(255,0,0),cls.grid[x+24,y+2].get_body())
        pygame.draw.rect(cls.screen,(0,0,0),cls.grid[x+24,y+2].get_body(),1)
        cls.grid[x+24,y-3].state = 1
        pygame.draw.rect(cls.screen,(255,0,0),cls.grid[x+24,y-3].get_body())
        pygame.draw.rect(cls.screen,(0,0,0),cls.grid[x+24,y-3].get_body(),1)
        cls.grid[x+24,y-4].state = 1
        pygame.draw.rect(cls.screen,(255,0,0),cls.grid[x+24,y-4].get_body())
        pygame.draw.rect(cls.screen,(0,0,0),cls.grid[x+24,y-4].get_body(),1)
        cls.grid[x+34,y-2].state = 1
        pygame.draw.rect(cls.screen,(255,0,0),cls.grid[x+34,y-2].get_body())
        pygame.draw.rect(cls.screen,(0,0,0),cls.grid[x+34,y-2].get_body(),1)
        cls.grid[x+34,y-1].state = 1
        pygame.draw.rect(cls.screen,(255,0,0),cls.grid[x+34,y-1].get_body())
        pygame.draw.rect(cls.screen,(0,0,0),cls.grid[x+34,y-1].get_body(),1)
        cls.grid[x+35,y-1].state = 1
        pygame.draw.rect(cls.screen,(255,0,0),cls.grid[x+35,y-1].get_body())
        pygame.draw.rect(cls.screen,(0,0,0),cls.grid[x+35,y-1].get_body(),1)
        cls.grid[x+35,y-2].state = 1
        pygame.draw.rect(cls.screen,(255,0,0),cls.grid[x+35,y-2].get_body())
        pygame.draw.rect(cls.screen,(0,0,0),cls.grid[x+35,y-2].get_body(),1)
        
        


        
    
    # It assumes the grid is at least 128x128
    @classmethod
    def setup_NOT(cls):
        cls.make_gospel_gun((6,6))

