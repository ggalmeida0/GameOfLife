import pygame
import numpy as np

class CellularAutomaton:
    def __init__(self,world,coordinates,size=(64,64)):
        self.state = 0 # 0 = dead,   1 = alive
        self.world = world
        self.coordinates = coordinates
        self.size = size
        self.body = pygame.Rect((coordinates,self.size))
        pygame.draw.rect(self.world,(255,255,255),self.body)
        pygame.draw.rect(self.world,(0,0,0),self.body,2)
        self.neighbors = []
    
    def set_neighbors(self,neighbors): #neighbors should be a list of 8 automata
         self.neighbors = neighbors
    
    def get_neighbors(self):
        return self.neighbors