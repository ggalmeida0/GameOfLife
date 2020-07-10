import pygame
import numpy as np

class CellularAutomaton:
    def __init__(self,world,coordinates,size):
        self.state = 0 # 0 = dead,   1 = alive
        self._world = world
        self._coordinates = coordinates
        self._square_position = tuple(np.array(coordinates) // 64) # This data member is only for debuging reference
        self._size = size
        self._body = pygame.Rect((coordinates,self._size))
        pygame.draw.rect(self._world,(255,255,255),self._body)
        pygame.draw.rect(self._world,(0,0,0),self._body,1)
        self._neighbors = []
    
    def set_neighbors(self,neighbors): #neighbors should be a list of 8 automata
         self._neighbors = neighbors
    
    def get_neighbors(self):
        return self._neighbors

    def get_body(self):
        return self._body