import pygame
import numpy as np

class CellularAutomaton:
    def __init__(self,world,coordinates,size):
        self.state = 0 # 0 = dead,   1 = alive
        self._square_position = tuple(np.array(coordinates) // 64) # This data member is only for debuging reference
        self._body = pygame.Rect((coordinates,size))
        pygame.draw.rect(world,(255,255,255),self._body)
        pygame.draw.rect(world,(0,0,0),self._body,1)
        self._neighbors = []
        self.will_live = None
    
    def set_neighbors(self,neighbors): #neighbors should be a list of 8 automata
         self._neighbors = neighbors
    
    def get_neighbors(self):
        return self._neighbors

    def get_body(self):
        return self._body
    
    # It advances the state of the automaton 1 generation
    def step(self):
        alive_neighbors = 0
        for neighbor in self._neighbors:
            if neighbor and neighbor.state == 1:
                alive_neighbors += 1
        # Rules:
        # 1. Any live cell with fewer than two live neighbours dies, as if by underpopulation
        if self.state == 1 and alive_neighbors < 2:
            self.will_live = False
        # 2. Any live cell with two or three live neighbours lives on to the next generation
        elif self.state == 1 and (alive_neighbors == 2 or alive_neighbors == 3):
            self.will_live = True
        # 3. Any live cell with more than three live neighbours dies, as if by overpopulation.
        elif self.state == 1 and alive_neighbors > 3:
            self.will_live = False
        # 4. Any dead cell with exactly three live neighbours becomes a live cell, as if by reproduction.
        elif self.state == 0 and alive_neighbors == 3:
            self.will_live = True
