import pygame
from pygame.locals import *

from solitaire_ui import SolitaireUI 
from game import Game  

def main():
    pygame.init()
    game = Game()
    ui = SolitaireUI(game)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            elif event.type == MOUSEBUTTONUP:
                ui.handle_click(pygame.mouse.get_pos())
        ui.draw()
        pygame.display.update()

    pygame.quit()

if __name__ == "__main__":
    main()