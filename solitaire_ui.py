# need to move away from import os, playing cards asset folder in project itself. -- changed to relative path
# verify best way to load assets.
# current issue with defining the card to match those in asset folder.
# tried swapping so rank is before suit, for example Ad would be ace of diamonds.
# coordinates are approximate, will adjust when we can get it to compile.
# still require a background asset, set to green for now.

import pygame
import os
from pygame.locals import *
from game import Game
from talonpile import TalonPile
from pile import Pile
from tableau import TableauPile
import sys

class SolitaireUI:
    def __init__(self):
        pygame.init()
        self.game = Game()
        self.talonpile = TalonPile()
        self.tableau_piles = TableauPile()
        self.window_surface = pygame.display.set_mode((900, 600))
        self.card_images = self.load_card_images()
        self.selected_pile = None

    def load_card_images(self):
        CARDS_PATH = f"Playing Cards Asset\Cards\Modern"
        card_images = {}
        card_width, card_height = 100, 200

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

        return card_images

    def draw(self):
        self.window_surface.fill((0, 128, 0))  # green background

        # need to draw tableau piles
        for i, pile in enumerate(self.game.tableau):
            # print("Card Rank:", card.rank, "Card Suit:", card.suit)
            self.draw_pile_cards(pile, (100 + 100*i, 400))

        # need to draw foundation piles
        for i, pile in enumerate(self.game.foundation):
            self.draw_pile_cards(pile, (500 + 80*i, 50))

        # need to draw the talon pile
        self.draw_pile_cards(self.game.talonpile, (150, 50))

        # need to draw the stockpile
        self.draw_pile_cards(self.game.stockpile, (50, 50), face_up=False)

        pygame.display.flip()

    def draw_pile_cards(self, pile, position, face_up=True):
        x, y = position
        for i, card in enumerate(pile.cards):
            if card.face_up == face_up:
                # print("Card Rank:", card.rank, "Card Suit:", card.suit)
                image = self.card_images[f'{card.rank}{card.suit}']
            else:
                image = self.card_images['back.png']
            self.window_surface.blit(image, (x, y + 20 * i))

    def handle_click(self, position):
        x, y = position

        # need to check if tableau pile was clicked
        # section below tries to enforce some of the game rules, still needs a lot of work.
        if y >= 300:
            pile_index = (x - 100) // 80
            if 0 <= pile_index < len(self.game.tableau_piles):
                # handles tableau pile click
                if self.selected_pile is None:
                    # section based on the rules that you can only select the bottom card or a pile of face-up cards from tableau pile.
                    # will check if the pile at pile_index has any face up cards. 
                    face_up_cards = [card for card in self.game.tableau_piles[pile_index].cards if card.face_up]
                    if face_up_cards:
                        # need to create new pile with face-up cards and select it. 
                        self.selected_pile = Pile()
                        for card in face_up_cards:
                            self.selected_pile.add_card(card)
                else:
                    if self.game.tableau_piles[pile_index].is_valid_move(self.selected_pile):
                        # need to move cards from selected pile to tableau pile.
                        self.game.tableau_piles[pile_index].add_cards(self.selected_pile.cards)
                        # need to remove the moved cards from original pile.
                        for card in self.selected_pile.cards:
                            self.selected_pile.remove_card(card)
                    self.selected_pile = None

        # here we check if foundation pile was clicked. 
        elif y <= 50 and x >= 500:
            pile_index = (x - 500) // 80
            if 0 <= pile_index < len(self.game.foundation_piles):
                # below code handles if it is clicked
                # as per the rules, you can't move a pile of cards to the foundations, only a card at a time. 
                if self.selected_pile is not None and len(self.selected_pile.cards) == 1:
                    if self.game.foundation_piles[pile_index].is_valid_move(self.selected_pile):
                        self.game.foundation_piles[pile_index].add_card(self.selected_pile.remove_card())
                    self.selected_pile = None

        # here we check if stockpile was clicked. 
        elif y <= 50 and x <= 50:
            if not self.game.stockpile.is_empty():
                card = self.game.stockpile.remove_card()
                self.game.talonpile.add_card(card)

        # here we check if talon pile was clicked. 
        elif y <= 50 and x <= 150:
            if not self.game.talonpile.is_empty():
                # as per game rules, can't move a pile of cards from talon pile, only a card at a time.
                if self.selected_pile is None:
                    self.selected_pile = Pile()
                    self.selected_pile.add_card(self.game.talonpile.remove_card())
                else:
                    # can't move cards to talon, deselect the selected pile. 
                    self.selected_pile = None

        # here we check if empty tableau spot was clicked. 
        elif y >= 300:
            pile_index = (x - 100) // 80
            if 0 <= pile_index < len(self.game.tableau_piles) and self.game.tableau_piles[pile_index].is_empty():
                if self.selected_pile is not None and self.selected_pile.peek().rank == Rank.KING:
                    # Move the King to the empty spot
                    self.game.tableau_piles[pile_index].add_cards(self.selected_pile.cards)
                    self.selected_pile.clear()
                    self.selected_pile = None
        
        if self.game.is_won():
            print("Congratulations! You have won the game!")

        if self.game.is_lost():
            print("Game Over! You have lost the game.")

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