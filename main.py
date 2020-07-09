import pygame
from game import Game
from pygame.locals import QUIT,MOUSEBUTTONDOWN, KEYDOWN

# Controls:
# Left click: place and remove a live cell
# Right click: step one generation
# Space bar: reset the board

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
            if event.type  == KEYDOWN and event.key == pygame.K_SPACE:
                Game.reset_cells()
        pygame.display.update()