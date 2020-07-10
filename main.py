import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame
from game import Game
from pygame.locals import QUIT,MOUSEBUTTONDOWN, KEYDOWN

# Controls:
# Left click: place and remove a live cell
# Right click: step one generation
# Space bar: reset the board
# Enter: play the game continuously or pause

if __name__ == "__main__":
    print("\nWelcome the the Game of Life (Golly) Simulator\n")
    while(True):
        command = input("Type a command or 'help' to see a list of commands: ")
        if(command == "help"):
            print("\nThe possible commands are:")
            print("playground  It will provide you with a n x n grid of the game of life to play around with")
            print("showNOT     It will show a configuration of a logic NOT gate in the game of life")
            print("showAND     It will show a configuration of a logic AND gate in the game of life")
            print("showOR      It will show a configuration of a logic OR gate in the game of life")
            print("exit        It will exit this program")
        elif(command == "playground" or command == "showNOT"):
            print("\nControls:\n-Left click: place and remove a live cell\n-Right click: step one generation\n-Space bar: reset the board\n-Enter: will play the simulation continuously click again to pause")
            if(command == "playground"):
                grid_size = None
                while(type(grid_size) != int):
                    grid_size = int(input("Give the size n, the grid will be n x n: "))
                Game.start(grid_size)
            elif(command == "showNOT"):
                Game.start(128)
                Game.setup_NOT()
            game_paused = True
            end_simulation = False
            while True:
                for event in pygame.event.get():
                    if event.type == QUIT:
                        pygame.quit()
                        end_simulation = True
                    if event.type == MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0]:
                        Game.handle_click(pygame.mouse.get_pos())
                    if event.type == MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[2]:
                        Game.step()
                    if event.type  == KEYDOWN and event.key == pygame.K_SPACE:
                        Game.reset_cells()
                        game_paused = True
                    if event.type == KEYDOWN and event.key == pygame.K_RETURN:
                        if game_paused:
                            game_paused = False
                        else:
                            game_paused = True
                if end_simulation:
                    break
                if not game_paused:
                    Game.step()
                pygame.display.update()
        elif(command == "exit"):
            exit()
    
    
    
    
    