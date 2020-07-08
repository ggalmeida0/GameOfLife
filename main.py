import pygame
from game import Game
from pygame.locals import QUIT,MOUSEBUTTONDOWN


if __name__ == "__main__":
    Game.start()
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit()
            if event.type == MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0]:
                Game.handle_click(pygame.mouse.get_pos())
            if event.type == MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[2]:
                Game.step()
        pygame.display.update()