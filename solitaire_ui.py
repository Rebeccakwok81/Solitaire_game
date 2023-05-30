# need to move away from import os, playing cards asset folder in project itself. -- changed to relative path
# verify best way to load assets.
# current issue with defining the card to match those in asset folder.
# tried swapping so rank is before suit, for example Ad would be ace of diamonds.
# coordinates are approximate, will adjust when we can get it to compile.
# still require a background asset, set to green for now.

# edit on 5/30:
# line 64-70: load empty image for foundation pile and talon pile
# line 92-99: comment-out for now, please feel free to change
# line 106-113: draw empty holder images for foundation pile and talon pile

import pygame
import os
from pygame.locals import *
from game import Game
from talonpile import TalonPile
from pile import Pile
from tableau import TableauPile
import sys

class SolitaireUI:
    def __init__(self, game):
        pygame.init()
        pygame.init()
        self.game = game
        self.talonpile = TalonPile()
        self.tableau_piles = TableauPile()
        self.window_surface = pygame.display.set_mode((1200, 750))
        self.card_images = self.load_card_images()
        self.selected_pile = None
        self.left_right_margin = 100
        self.column_width = (1200 - 2*self.left_right_margin) // 7
        self.card_width = 115
        self.card_height = 175
        self.top_row_y = 50
        self.bottom_row_y = 300

    def load_card_images(self):
        CARDS_PATH = f"Playing Cards Asset\Cards\Modern"
        card_images = {}
        card_width, card_height = 115, 175

        for suit in ('c', 'd', 'h', 's'):
            for rank in ('A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K'):
                card_name = f"{rank}{suit}"
                if rank == '10':
                    filename = f"{rank}{suit}.png"
                else:
                    filename = f"{rank}{suit}.png"
                # filepath = os.path.join(CARDS_PATH, filename)
                filepath = f"{CARDS_PATH}\{filename}"
            
                try:
                    image = pygame.image.load(filepath)
                    image = pygame.transform.scale(image, (card_width, card_height))
                    card_images[card_name] = image
                except pygame.error:
                    print(f"Error loading image: {filepath}")

        # load the back image, going with 03
        back_image_path = f"Playing Cards Asset\Backs\Card-Back-03.png"
        try:
            back_image = pygame.image.load(back_image_path)
            back_image = pygame.transform.scale(back_image, (card_width, card_height))
            card_images['back.png'] = back_image
        except pygame.error:
            print(f"Error loading back image: {back_image_path}")

        # load empty image for foundation pile and talon pile
        empty_holder = f"Playing Cards Asset\empty_holder.png"
        try:
            e_image = pygame.image.load(empty_holder)
            e_image = pygame.transform.scale(e_image, (card_width, card_height))
            card_images['empty_holder.png'] = e_image
        except pygame.error:
            print(f"Error loading back image: {empty_holder}")

        return card_images

    def draw(self):
        self.window_surface.fill((0, 100, 0))  # green background

    # margins from left and right window borders
        left_right_margin = 100

    # calculate new column width
        column_width = (1200 - 2*left_right_margin) // 7

    # calculate the card width and height
        card_width = 115
        card_height = 175

    # Y-coordinates for the rows
        top_row_y = 50  
        bottom_row_y = 300  

    # Draw rectangles for stockpile, talonpile, and foundation piles
        # for i in range(7):
        #     x_coordinate = left_right_margin + i*column_width
        #     if i == 0:
        #         pygame.draw.rect(self.window_surface, (0, 200, 0), pygame.Rect(x_coordinate, top_row_y, card_width, card_height))  # Stockpile
        #     elif i == 1:
        #         pygame.draw.rect(self.window_surface, (0, 200, 0), pygame.Rect(x_coordinate, top_row_y, card_width, card_height))  # Talonpile
        #     elif i >= 3:
        #         pygame.draw.rect(self.window_surface, (0, 200, 0), pygame.Rect(x_coordinate, top_row_y, card_width, card_height))  # Foundation piles

    # calculate the position of the stockpile
        stockpile_x = left_right_margin + column_width // 2 - card_width // 2
        stockpile_y = top_row_y
    
    # draw empty holder images for foundation pile and talon pile
        empty_holder_image = self.card_images['empty_holder.png']

        foundation_pile_positions = [(left_right_margin + (i + 3) * column_width, top_row_y) for i in range(4)]
        for position in foundation_pile_positions:
            self.window_surface.blit(empty_holder_image, position)

        talon_pile_position = (left_right_margin + column_width, top_row_y)
        self.window_surface.blit(empty_holder_image, talon_pile_position)

    # draw tableau piles
        for i, pile in enumerate(self.game.tableau):
            self.draw_pile_cards(pile, (left_right_margin + i*column_width, bottom_row_y))

    # draw foundation, talon, and stockpile cards
        for i, pile in enumerate(self.game.foundation):
            self.draw_pile_cards(pile, (left_right_margin + (i+3)*column_width, top_row_y))

            self.draw_pile_cards(self.game.talonpile, (left_right_margin + column_width, top_row_y))
            self.draw_pile_cards(self.game.stockpile, (stockpile_x, stockpile_y), face_up=False)

        pygame.display.flip()

    def draw_pile_cards(self, pile, position, face_up=False):
        x, y = position
        column_width = 800 // 7 
        top_row_y = 50  
        bottom_row_y = 300  
        card_width = 115
        card_height = 175

        deck_x = x + card_width // 2
        deck_y = top_row_y + card_height // 2

        if pile == self.game.stockpile:
            if not face_up:
                back_image = self.card_images['back.png']
                back_rect = back_image.get_rect(center=(deck_x, deck_y))
                self.window_surface.blit(back_image, back_rect)
            else:
                return
        else:
            for i, card in enumerate(pile.cards):
                if pile == self.game.stockpile and not face_up and i != len(pile.cards) - 1:
                    continue

                if card.face_up == face_up:
                    image = self.card_images[f'{card.rank}{card.suit}']
                else:
                    image = self.card_images['back.png']
                
                card_x = x
                
                if pile == self.game.talonpile:
                    card_y = y
                else:
                    card_y = y + i * 15

                self.window_surface.blit(image, (card_x, card_y))

    def handle_click(self, position):
        x, y = position

        for i, pile in enumerate(self.game.tableau):
            pile_x = self.left_right_margin + i * self.column_width
            pile_y = self.bottom_row_y

            # check if the click occurred within the bounding box of the tableau pile
            if pile_x <= x < pile_x + self.card_width and pile_y <= y < pile_y + len(pile.cards) * 30:
                # if a tableau pile was clicked
                if self.selected_pile is None:
                    # select the clicked pile as the selected pile
                    self.selected_pile = pile
                    self.selected_cards = pile.get_selected_cards(position)
                else:
                    # move the selected cards from the selected pile to the clicked pile
                    if pile.is_valid_move(self.selected_pile.peek_top_card()):
                        pile.add_cards(self.selected_cards)
                        self.selected_pile.remove_selected_cards()
                    else:
                        print("Invalid move. Cannot move cards to this pile.")
                
                break
        else:
            # handle the click-and-drag movement of cards
            if self.selected_pile is not None:
                dx = position[0] - self.click_position[0]
                dy = position[1] - self.click_position[1]
                self.selected_pile.move_selected_cards(dx, dy)

        # set the coordinates for the deck and the size of a card
        stockpile_x = self.left_right_margin + self.column_width // 2 - self.card_width // 2
        stockpile_y = self.top_row_y
        card_width = 115
        card_height = 175

        # define the bounding box for the deck
        deck_left = stockpile_x
        deck_right = stockpile_x + card_width
        deck_top = stockpile_y
        deck_bottom = stockpile_y + card_height

        # check if the click occurred within the bounding box of the deck
        if deck_left <= x <= deck_right and deck_top <= y <= deck_bottom:
            # The deck was clicked
            if not self.game.stockpile.is_empty():
                # move the top card from the stockpile to the talonpile (waste pile)
                card = self.game.stockpile.deal_card()
                card.flip()
                self.game.talonpile.add_card(card)
                print("Deck clicked, card moved to waste pile.")  # debug message
            else:
                print("Deck clicked but it's empty.")  # debug message
        

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == MOUSEBUTTONDOWN:
                    self.handle_click(event.pos)
            self.draw()
            pygame.display.flip()


if __name__ == '__main__':
    # better way to do this, but for now, create instance of the UI
    ui = SolitaireUI()

    # run the game. 
    ui.run()