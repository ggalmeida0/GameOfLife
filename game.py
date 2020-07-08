from automata import CellularAutomaton
import numpy as np
import pygame


class Game:
    GRID_SIZE = 16

    @classmethod
    def start(cls):
        pygame.init()
        cls.screen = pygame.display.set_mode((1024,1024))
        pygame.display.set_caption("Game of Life")
        cls.grid = np.array([[None] * cls.GRID_SIZE]*cls.GRID_SIZE)
        cls.render_cells()
        
    
    @classmethod
    def render_cells(cls):
        current_position = np.array([0,0])
        for i in range(cls.grid.shape[0]):
            for j in range(cls.grid[i].shape[0]):
                cls.grid[i,j] = CellularAutomaton(cls.screen,tuple(current_position))
                current_position += [0,64]
            current_position[1] = 0
            current_position += [64,0]
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
    def handle_click(cls,coordinates):
        clicked_coord = (coordinates[0] // 64,coordinates[1] //64)
        clicked_cell = cls.grid[clicked_coord[0],clicked_coord[1]]
        if clicked_cell.state == 0:
            pygame.draw.rect(cls.screen,(255,0,0),clicked_cell.body)
            pygame.draw.rect(cls.screen,(0,0,0),clicked_cell.body,2)
            clicked_cell.state = 1
        elif clicked_cell.state == 1:
            pygame.draw.rect(cls.screen,(255,255,255),clicked_cell.body)
            pygame.draw.rect(cls.screen,(0,0,0),clicked_cell.body,2)
            clicked_cell.state = 0

    @classmethod
    def step(cls):
        old_configuration = cls.grid.copy()
        for i in range(old_configuration.shape[0]):
            for j in range(old_configuration[i].shape[0]):
                alive_neighbors = 0
                current_cell = cls.grid[i][j]
                for neighbor in old_configuration[i][j].get_neighbors():
                    if neighbor and neighbor.state:
                        alive_neighbors += 1
                if(alive_neighbors == 2 or alive_neighbors == 3):
                    if not current_cell.state:
                        current_cell.state = 1
                        pygame.draw.rect(cls.screen,(255,0,0),current_cell.body)
                        pygame.draw.rect(cls.screen,(0,0,0),current_cell.body,2)
                else:
                    if current_cell.state:
                        current_cell.state = 0
                        pygame.draw.rect(cls.screen,(255,225,225),current_cell.body)
                        pygame.draw.rect(cls.screen,(0,0,0),current_cell.body,2)
